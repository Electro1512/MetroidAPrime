import asyncio
import json
import multiprocessing
import os
import subprocess
import traceback
from typing import List
import zipfile
import py_randomprime

from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, logger, server_loop, gui_enabled
from NetUtils import ClientStatus, NetworkItem
import Utils
from worlds.metroidprime.NotificationManager import NotificationManager
from worlds.metroidprime.Container import construct_hud_message_patch
from .DolphinClient import DolphinException
from .Locations import METROID_PRIME_LOCATION_BASE, every_location
from .MetroidPrimeInterface import HUD_MESSAGE_DURATION, ConnectionState, InventoryItemData, MetroidPrimeInterface, MetroidPrimeLevel


class MetroidPrimeCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_deathlink(self):
        """Toggle deathlink from client. Overrides default setting."""
        if isinstance(self.ctx, MetroidPrimeContext):
            new_value = True
            if (self.tags["DeathLink"]):
                new_value = False
            Utils.async_start(self.ctx.update_death_link(
                new_value), name="Update Deathlink")


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
            if "death_link" in args["slot_data"]:
                Utils.async_start(self.update_death_link(
                    bool(args["slot_data"]["death_link"])))


def update_connection_status(ctx: MetroidPrimeContext, status):
    if ctx.connection_state == status:
        return
    elif status == ConnectionState.IN_GAME:
        logger.info("Connected to Metroid Prime")
    elif status == ConnectionState.IN_MENU:
        logger.info("Connected to Metroid Prime, waiting for game to start")
    elif status == ConnectionState.DISCONNECTED:
        logger.info("Disconnected from Metroid Prime, attempting to reconnect...")

    ctx.connection_state = status


async def dolphin_sync_task(ctx: MetroidPrimeContext):
    logger.info("Starting Dolphin Connector, attempting to connect to emulator...")
    while not ctx.exit_event.is_set():
        if not ctx.slot:
            await asyncio.sleep(3)
            continue
        else:
            try:
                connection_state = ctx.game_interface.get_connection_state()
                update_connection_status(ctx, connection_state)
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


def inventory_item_by_network_id(network_id: int, current_inventory: dict[str, InventoryItemData]) -> InventoryItemData:
    for item in current_inventory.values():
        if item.code == network_id:
            return item
    return None


def get_total_count_of_item_received(network_id: int, items: list[NetworkItem]) -> int:
    count = 0
    for network_item in items:
        if network_item.item == network_id:
            count += 1
    return count


async def handle_checked_location(ctx: MetroidPrimeContext, current_inventory: dict[str, InventoryItemData]):
    """Uses the current amount of UnknownItem1 in inventory as an indicator of which location was checked. This will break if the player collects more than one pickup without having the AP client hooked to the game and server"""
    unknown_item1 = current_inventory["UnknownItem1"]
    if (unknown_item1.current_capacity == 0):
        return
    checked_location_id = METROID_PRIME_LOCATION_BASE + \
        unknown_item1.current_capacity - 1
    logger.debug(
        f"Checked location: {checked_location_id} with amount: {unknown_item1.current_capacity} ")
    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [checked_location_id]}])
    ctx.game_interface.give_item_to_player(unknown_item1.id, 0, 0)


async def handle_receive_items(ctx: MetroidPrimeContext, current_items: dict[str, InventoryItemData]):
    # Handle Single Item Upgrades
    for network_item in ctx.items_received:
        item_data = inventory_item_by_network_id(
            network_item.item, current_items)
        if item_data is None:
            logger.debug(
                f"Item with network id {network_item.item} not found in inventory. {network_item}")
            continue
        if item_data.max_capacity == 1 and item_data.current_amount == 0:
            logger.debug(f"Giving item {item_data.name} to player")
            ctx.game_interface.give_item_to_player(item_data.id, 1, 1)
            ctx.notification_manager.queue_notification(f"{item_data.name} online ({ctx.player_names[network_item.player]})")

    # Handle Missile Expansions
    amount_of_missiles_given_per_item = 5
    missile_item = current_items["Missile Expansion"]
    num_missile_expansions_received = get_total_count_of_item_received(
        missile_item.code, ctx.items_received)
    diff = num_missile_expansions_received * \
        amount_of_missiles_given_per_item - missile_item.current_capacity
    if diff > 0 and missile_item.current_capacity < missile_item.max_capacity:
        new_capacity = min(num_missile_expansions_received *
                           amount_of_missiles_given_per_item, missile_item.max_capacity)
        new_amount = min(missile_item.current_amount + diff, new_capacity)
        logger.debug(
            f"Setting missile expansion to {new_amount}/{new_capacity} from {missile_item.current_amount}/{missile_item.current_capacity}")
        ctx.game_interface.give_item_to_player(
            missile_item.id, new_amount, new_capacity)
        ctx.notification_manager.queue_notification(f"Missile capactiy increased by {diff}")

    # Handle Power Bomb Expansions
    power_bomb_item = current_items["Power Bomb Expansion"]
    num_power_bombs_received = get_total_count_of_item_received(
        power_bomb_item.code, ctx.items_received)
    diff = num_power_bombs_received - power_bomb_item.current_capacity
    if diff > 0 and power_bomb_item.current_capacity < power_bomb_item.max_capacity:
        new_capacity = min(3 + num_power_bombs_received,
                           power_bomb_item.max_capacity)
        new_amount = min(power_bomb_item.current_amount + diff, new_capacity)
        logger.debug(
            f"Setting power bomb expansions to {new_capacity} from {power_bomb_item.current_capacity}")
        ctx.game_interface.give_item_to_player(
            power_bomb_item.id, new_capacity, new_capacity)
        ctx.notification_manager.queue_notification(f"Power Bomb capactiy increased by {diff}")

    # Handle Energy Tanks
    energy_tank_item = current_items["Energy Tank"]
    num_energy_tanks_received = get_total_count_of_item_received(
        energy_tank_item.code, ctx.items_received)
    diff = num_energy_tanks_received - energy_tank_item.current_capacity
    if diff > 0 and energy_tank_item.current_capacity < energy_tank_item.max_capacity:
        new_capacity = min(num_energy_tanks_received,
                           energy_tank_item.max_capacity)
        logger.debug(
            f"Setting energy tanks to {new_capacity} from {energy_tank_item.current_capacity}")
        ctx.game_interface.give_item_to_player(
            energy_tank_item.id, new_capacity, new_capacity)

        # Heal player when they receive a new energy tank
        # Player starts with 99 health and each energy tank adds 100 additional
        ctx.game_interface.set_current_health(new_capacity * 100.0 + 99)

    # Handle Artifacts
    ctx.game_interface.sync_artifact_layers()


async def handle_check_goal_complete(ctx: MetroidPrimeContext):
    current_level = ctx.game_interface.get_current_level()
    if current_level == MetroidPrimeLevel.End_of_Game:
        logger.debug("Sending Goal Complete")
        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])


async def handle_check_deathlink(ctx: MetroidPrimeContext):
    health = ctx.game_interface.get_current_health()
    if health <= 0 and ctx.is_pending_death_link_reset == False:
        await ctx.send_death(ctx.player_names[ctx.slot] + " ran out of energy.")
        ctx.is_pending_death_link_reset
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

        if "DeathLink" in ctx.tags:
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
    if auto_start is True:
        import webbrowser
        webbrowser.open(romfile)
    elif os.path.isfile(auto_start):
        subprocess.Popen([auto_start, romfile],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


async def patch_and_run_game(apmp1_file: str):
    apmp1_file = os.path.abspath(apmp1_file)
    input_iso_path = Utils.get_options()["metroidprime_options"]["rom_file"]
    base_name = os.path.splitext(apmp1_file)[0]
    output_path = base_name + '.iso'

    config_json_file = None
    if zipfile.is_zipfile(apmp1_file):
        for name in zipfile.ZipFile(apmp1_file).namelist():
            if name == 'config.json':
                config_json_file = name
                break

    config_json = None
    with zipfile.ZipFile(apmp1_file) as zip_file:
        with zip_file.open(config_json_file) as file:
            config_json = file.read().decode("utf-8")
            config_json = json.loads(config_json)

    config_json["gameConfig"]["updateHintStateReplacement"] = construct_hud_message_patch()
    notifier = py_randomprime.ProgressNotifier(
        lambda progress, message: print("Generating ISO: ", progress, message))
    py_randomprime.patch_iso(input_iso_path, output_path, config_json, notifier)


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
