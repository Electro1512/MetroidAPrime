import asyncio
import json
import multiprocessing
import os
import subprocess
import traceback
from typing import List, Optional
import zipfile
import py_randomprime

from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, logger, server_loop, gui_enabled
from NetUtils import ClientStatus, NetworkItem
import Utils
from .Items import suit_upgrade_table
from .ClientReceiveItems import handle_receive_items
from .NotificationManager import NotificationManager
from .Container import construct_hook_patch
from .DolphinClient import DolphinException, assert_no_running_dolphin, get_num_dolphin_instances
from .Locations import METROID_PRIME_LOCATION_BASE, every_location
from .MetroidPrimeInterface import HUD_MESSAGE_DURATION, ConnectionState, InventoryItemData, MetroidPrimeInterface, MetroidPrimeLevel, MetroidPrimeSuit


class MetroidPrimeCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_test_hud(self, *args):
        """Send a message to the game interface."""
        self.ctx.notification_manager.queue_notification(' '.join(map(str, args)))

    def _cmd_status(self, *args):
        """Display the current dolphin connection status."""
        logger.info(f"Connection status: {status_messages[self.ctx.connection_state]}")

    def _cmd_deathlink(self):
        """Toggle deathlink from client. Overrides default setting."""
        if isinstance(self.ctx, MetroidPrimeContext):
            self.ctx.death_link_enabled = not self.ctx.death_link_enabled
            Utils.async_start(self.ctx.update_death_link(
                self.ctx.death_link_enabled), name="Update Deathlink")
            message = f"Deathlink {'enabled' if self.ctx.death_link_enabled else 'disabled'}"
            logger.info(message)
            self.ctx.notification_manager.queue_notification(message)

    def _cmd_toggle_gravity_suit(self):
        """Toggles the gravity suit functionality on/off if the player has received it. Note that this will not change the player's current suit they are wearing but disables the functionality of the gravity suit."""
        if isinstance(self.ctx, MetroidPrimeContext):
            self.ctx.gravity_suit_enabled = not self.ctx.gravity_suit_enabled
            self.ctx.notification_manager.queue_notification(f"{'Enabling' if self.ctx.gravity_suit_enabled else 'Disabling'} Gravity Suit...")

    def _cmd_set_cosmetic_suit(self, input):
        """Set the cosmetic suit of the player. This will not affect the player's current suit but will change the appearance of the suit in the game. Note that if you start a new seed without closing the client, the option will persist. If you close the client and get a new suit, you may need to re set this."""
        if isinstance(self.ctx, MetroidPrimeContext):
            if input == "None":
                logger.info("Removing cosmetic suit")
                self.ctx.cosmetic_suit = None
                suit = self.ctx.game_interface.get_highest_owned_suit()
                self.ctx.game_interface.set_cosmetic_suit_by_id(suit_upgrade_table[suit.value].id)
                self.ctx.game_interface.set_current_suit(self.ctx.game_interface.get_current_cosmetic_suit())
                return
            suit = MetroidPrimeSuit.get_by_key(input)
            if suit is None:
                options = ", ".join([suit.name for suit in MetroidPrimeSuit if "Fusion" not in suit.name] + ["None"])
                logger.warning(f"Invalid cosmetic suit: {suit}. Valid options are: {options}")
                return
            logger.info(f"Setting cosmetic suit to: {suit.name} Suit")
            self.ctx.cosmetic_suit = suit


status_messages = {
    ConnectionState.IN_GAME: "Connected to Metroid Prime",
    ConnectionState.IN_MENU: "Connected to game, waiting for game to start",
    ConnectionState.DISCONNECTED: "Unable to connect to the Dolphin instance, attempting to reconnect...",
    ConnectionState.MULTIPLE_DOLPHIN_INSTANCES: "Warning: Multiple Dolphin instances detected, client may not function correctly."
}


class MetroidPrimeContext(CommonContext):
    current_level_id = 0
    previous_level_id = 0
    is_pending_death_link_reset = False
    command_processor = MetroidPrimeCommandProcessor
    game_interface: MetroidPrimeInterface
    notification_manager: NotificationManager
    game = "Metroid Prime"
    items_handling = 0b111
    dolphin_sync_task = None
    connection_state = ConnectionState.DISCONNECTED
    slot_data: dict[str, Utils.Any] = None
    death_link_enabled = False
    gravity_suit_enabled: bool = True
    previous_location_str: str = ""
    cosmetic_suit: Optional[MetroidPrimeSuit] = None

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.game_interface = MetroidPrimeInterface(logger)
        self.notification_manager = NotificationManager(HUD_MESSAGE_DURATION, self.game_interface.send_hud_message)

    def on_deathlink(self, data: Utils.Dict[str, Utils.Any]) -> None:
        super().on_deathlink(data)
        self.game_interface.set_alive(False)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(MetroidPrimeContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.slot_data = args["slot_data"]
            if "death_link" in args["slot_data"]:
                self.death_link_enabled = bool(args["slot_data"]["death_link"])
                Utils.async_start(self.update_death_link(
                    bool(args["slot_data"]["death_link"])))

    def run_gui(self):
        from kvui import GameManager

        class MetroidPrimeManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Metroid Prime Client"

        self.ui = MetroidPrimeManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


def update_connection_status(ctx: MetroidPrimeContext, status):
    if ctx.connection_state == status:
        return
    else:
        logger.info(status_messages[status])
        if get_num_dolphin_instances() > 1:
            logger.info(status_messages[ConnectionState.MULTIPLE_DOLPHIN_INSTANCES])
        ctx.connection_state = status


async def dolphin_sync_task(ctx: MetroidPrimeContext):
    logger.info("Starting Dolphin Connector, attempting to connect to emulator...")
    while not ctx.exit_event.is_set():
        try:
            connection_state = ctx.game_interface.get_connection_state()
            update_connection_status(ctx, connection_state)
            if connection_state == ConnectionState.IN_MENU:
                await handle_check_goal_complete(ctx)  # It will say the player is in menu sometimes
            if connection_state == ConnectionState.IN_GAME:
                await _handle_game_ready(ctx)
            else:
                await _handle_game_not_ready(ctx)
                await asyncio.sleep(1)
        except Exception as e:
            if isinstance(e, DolphinException):
                logger.error(str(e))
            else:
                logger.error(traceback.format_exc())
            await asyncio.sleep(3)
            continue


def __int_to_reversed_bits(value: int, bit_length: int) -> str:
    """
    Converts an integer to a binary string of a specified length and reverses it.

    :param value: The integer to convert.
    :param bit_length: The length of the resulting binary string.
    :return: A reversed binary string representation of the integer.
    """
    binary_string = format(value, f'0{bit_length}b')
    return binary_string[::-1]


async def handle_checked_location(ctx: MetroidPrimeContext, current_inventory: dict[str, InventoryItemData]):
    """Uses the current amount of UnknownItem1 in inventory as an indicator of which location was checked. This will break if the player collects more than one pickup without having the AP client hooked to the game and server"""
    unknown_item1 = current_inventory["UnknownItem1"]
    unknown_item2 = current_inventory["UnknownItem2"]
    health_refill = current_inventory["HealthRefill"]

    flag_ints = [unknown_item1.current_amount, unknown_item2.current_amount, unknown_item2.current_capacity, health_refill.current_capacity]
    flags_str = "".join([__int_to_reversed_bits(flag_int, 32) for flag_int in flag_ints])
    if (flags_str == ctx.previous_location_str):
        return
    checked_locations = []
    for index, char in enumerate(flags_str):
        if char == "1":
            checked_locations.append(index + METROID_PRIME_LOCATION_BASE)

    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": checked_locations}])
    ctx.previous_location_str = flags_str


async def handle_check_goal_complete(ctx: MetroidPrimeContext):
    if ctx.game_interface.current_game is not None:
        current_level = ctx.game_interface.get_current_level()
        if current_level == MetroidPrimeLevel.End_of_Game:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])


async def handle_check_deathlink(ctx: MetroidPrimeContext):
    health = ctx.game_interface.get_current_health()
    if health <= 0 and ctx.is_pending_death_link_reset == False:
        await ctx.send_death(ctx.player_names[ctx.slot] + " ran out of energy.")
        ctx.is_pending_death_link_reset = True
    elif health > 0 and ctx.is_pending_death_link_reset == True:
        ctx.is_pending_death_link_reset = False


async def _handle_game_ready(ctx: MetroidPrimeContext):
    if ctx.server:
        if not ctx.slot:
            await asyncio.sleep(1)
            return
        current_inventory = ctx.game_interface.get_current_inventory()
        await handle_receive_items(ctx, current_inventory)
        ctx.notification_manager.handle_notifications()
        await handle_checked_location(ctx, current_inventory)
        await handle_check_goal_complete(ctx)

        if ctx.death_link_enabled:
            await handle_check_deathlink(ctx)
        await asyncio.sleep(0.5)
    else:
        logger.info("Waiting for player to connect to server")
        await asyncio.sleep(1)


async def _handle_game_not_ready(ctx: MetroidPrimeContext):
    """If the game is not connected or not in a playable state, this will attempt to retry connecting to the game."""
    if ctx.connection_state == ConnectionState.DISCONNECTED:
        ctx.game_interface.connect_to_game()
    elif ctx.connection_state == ConnectionState.IN_MENU:
        await asyncio.sleep(3)


async def run_game(romfile):
    auto_start = Utils.get_options()["metroidprime_options"].get("rom_start", True)

    if auto_start is True and assert_no_running_dolphin():
        import webbrowser
        webbrowser.open(romfile)
    elif os.path.isfile(auto_start) and assert_no_running_dolphin():
        subprocess.Popen([auto_start, romfile],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def get_version_from_iso(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Couldn't get version for iso {path}!")
    with open(path, "rb") as f:
        game_id = f.read(6).decode("utf-8")
        f.read(1)
        game_rev = f.read(1)[0]
        if game_id[:3] != "GM8":
            raise Exception("This is not Metroid Prime GC")
        match game_id[3]:
            case "E":
                match game_rev:
                    case 0:
                        return "0-00"
                    case 1:
                        return "0-01"
                    case 2:
                        return "0-02"
                    case 48:
                        return "kor"
                    case _rev:
                        raise Exception(f"Unknown revision of Metroid Prime GC US (game_rev : {_rev})")
            case "J":
                match game_rev:
                    case 0:
                        return "jpn"
                    case _rev:
                        raise Exception(f"Unknown revision of Metroid Prime GC JPN (game_rev : {_rev})")
            case "P":
                match game_rev:
                    case 0:
                        return "pal"
                    case _rev:
                        raise Exception(f"Unknown revision of Metroid Prime GC PAL (game_rev : {_rev})")
            case _id:
                raise Exception(f"Unknown version of Metroid Prime GC (game_id : {game_id} | game_rev : {game_rev})")


async def patch_and_run_game(apmp1_file: str):
    apmp1_file = os.path.abspath(apmp1_file)
    input_iso_path = Utils.get_options()["metroidprime_options"]["rom_file"]
    game_version = get_version_from_iso(input_iso_path)
    base_name = os.path.splitext(apmp1_file)[0]
    output_path = base_name + '.iso'

    if not os.path.exists(output_path):

        config_json_file = None
        options_json_file = None
        if zipfile.is_zipfile(apmp1_file):
            for name in zipfile.ZipFile(apmp1_file).namelist():
                if name == 'config.json':
                    config_json_file = name
                elif name == 'options.json':
                    options_json_file = name

        config_json = None
        options_json = None

        with zipfile.ZipFile(apmp1_file) as zip_file:
            with zip_file.open(config_json_file) as file:
                config_json = file.read().decode("utf-8")
                config_json = json.loads(config_json)

            if options_json_file:
                with zip_file.open(options_json_file) as file:
                    options_json = file.read().decode("utf-8")
                    options_json = json.loads(options_json)

        build_progressive_beam_patch = False
        if options_json:
            build_progressive_beam_patch = options_json["progressive_beam_upgrades"]

        config_json["gameConfig"]["updateHintStateReplacement"] = construct_hook_patch(game_version, build_progressive_beam_patch)
        notifier = py_randomprime.ProgressNotifier(
            lambda progress, message: print("Generating ISO: ", progress, message))
        py_randomprime.patch_iso(input_iso_path, output_path, config_json, notifier)

    Utils.async_start(run_game(output_path))


def launch():
    Utils.init_logging("MetroidPrime Client")

    async def main():
        multiprocessing.freeze_support()
        logger.info("main")
        parser = get_base_parser()
        parser.add_argument('apmp1_file', default="", type=str, nargs="?",
                            help='Path to an apmp1 file')
        args = parser.parse_args()

        if args.apmp1_file:
            logger.info("APMP1 file supplied, beginning patching process...")
            Utils.async_start(patch_and_run_game(args.apmp1_file))

        ctx = MetroidPrimeContext(args.connect, args.password)
        logger.info("Connecting to server...")
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        logger.info("Running game...")
        ctx.dolphin_sync_task = asyncio.create_task(dolphin_sync_task(ctx), name="Dolphin Sync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.dolphin_sync_task:
            await asyncio.sleep(3)
            await ctx.dolphin_sync_task

    import colorama

    colorama.init()

    asyncio.run(main())
    colorama.deinit()


if __name__ == '__main__':
    launch()
