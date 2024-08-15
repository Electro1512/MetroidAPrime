# Setup local dependencies if running in an apworld
from .data.PhazonMines import PhazonMinesAreaData
from .data.PhendranaDrifts import PhendranaDriftsAreaData
from .data.MagmoorCaverns import MagmoorCavernsAreaData
from .data.ChozoRuins import ChozoRuinsAreaData
from .data.TallonOverworld import TallonOverworldAreaData
from .data.RoomData import AreaData
from .data.AreaNames import MetroidPrimeArea
from .DoorRando import AreaDoorTypeMapping, get_world_door_mapping
from .PrimeUtils import setup_lib_path
setup_lib_path()  # NOTE: This MUST be called before importing any other metroidprime modules (other than PrimeUtils)

from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess
import settings
from worlds.AutoWorld import World, WebWorld
from .data.Transports import default_elevator_mappings, get_random_elevator_mapping
from .config import make_config
from .Regions import create_regions
from .Locations import every_location
from .PrimeOptions import MetroidPrimeOptions, VariaSuitColorOverride
from .Items import PROGRESSIVE_ITEM_MAPPING, MetroidPrimeItem, ProgressiveUpgrade, SuitUpgrade, get_item_for_options, get_progressive_upgrade_for_item, suit_upgrade_table, artifact_table, item_table
from .data.StartRoomData import StartRoomData, init_starting_room_data
from .Container import MetroidPrimeContainer
from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
import typing
import os
from typing import Any, Dict, List, Optional
from logging import info


def run_client(url: Optional[str] = None):
    from .MetroidPrimeClient import launch
    launch_subprocess(launch, name="MetroidPrimeClient")


components.append(
    Component("Metroid Prime Client", func=run_client, component_type=Type.CLIENT,
              file_identifier=SuffixIdentifier(".apmp1"))
)


class MetroidPrimeSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Metroid Prime ISO"""
        description = "Metroid Prime GC ISO file"
        copy_to = "Metroid_Prime.iso"

    class RomStart(str):
        """
        Set this to false to never autostart a rom (such as after patching),
        Set it to true to have the operating system default program open the iso
        Alternatively, set it to a path to a program to open the .iso file with (like Dolplhin)
        """

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: typing.Union[RomStart, bool] = False


class MetroidPrimeWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Metroid Prime for Archipelago",
        "English",
        "setup.md",
        "setup/en",
        ["Electro15", "hesto2"]
    )]


# These items will always be given at start
ALWAYS_START_INVENTORY = [SuitUpgrade.Power_Suit.value, SuitUpgrade.Combat_Visor.value]


class MetroidPrimeWorld(World):
    """
    Metroid Prime is a first-person action-adventure game originally for the Gamecube. Play as
    the bounty hunter Samus Aran as she traverses the planet Tallon IV and uncovers the plans
    of the Space Pirates.
    """
    game = "Metroid Prime"
    web = MetroidPrimeWeb()
    required_client_version = (0, 5, 0)
    options_dataclass = MetroidPrimeOptions
    options: MetroidPrimeOptions
    topology_present = True
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = every_location
    settings: MetroidPrimeSettings
    item_name_groups = {
        "Artifacts": set(artifact_table.keys())
    }
    starting_room_data: Optional[StartRoomData] = None
    prefilled_item_map: Dict[str, str] = {}  # Dict of location name to item name
    elevator_mapping: Dict[str, Dict[str, str]] = default_elevator_mappings
    door_color_mapping: Optional[Dict[MetroidPrimeArea, AreaDoorTypeMapping]] = None
    game_region_data: Dict[MetroidPrimeArea, AreaData]

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.game_region_data = {
            MetroidPrimeArea.Tallon_Overworld: TallonOverworldAreaData(),
            MetroidPrimeArea.Chozo_Ruins: ChozoRuinsAreaData(),
            MetroidPrimeArea.Magmoor_Caverns: MagmoorCavernsAreaData(),
            MetroidPrimeArea.Phendrana_Drifts: PhendranaDriftsAreaData(),
            MetroidPrimeArea.Phazon_Mines: PhazonMinesAreaData()
        }

    def get_filler_item_name(self) -> str:
        return SuitUpgrade.Missile_Expansion.value

    def init_tracker_options(self):
        # Universal tracker stuff, shouldn't do anything in standard gen
        if self.game in self.multiworld.re_gen_passthrough:
            info("Setting options for tracker")
            passthrough = self.multiworld.re_gen_passthrough[self.game]
            for key, value in passthrough.items():
                option = getattr(self.options, key, None)
                if option is not None:
                    # These get interpreted as lists but the tracker expects them to be sets
                    if key in ["non_local_items", "local_items", "local_early_items", "priority_locations", "exclude_locations"]:
                        option.value = set(value)
                    else:
                        option.value = value

    def generate_early(self) -> None:
        skip_randomization_mapping = False
        if hasattr(self.multiworld, "re_gen_passthrough"):
            self.init_tracker_options()
            skip_randomization_mapping = True

        if self.options.door_color_randomization != "none" and not skip_randomization_mapping:
            self.options.door_color_mapping.value = get_world_door_mapping(self)

        init_starting_room_data(self)
        if self.options.elevator_randomization.value and not skip_randomization_mapping:
            self.elevator_mapping = get_random_elevator_mapping(self)

        self.options.elevator_mapping.value = self.elevator_mapping

    def create_regions(self) -> None:
        boss_selection = int(self.options.final_bosses)
        create_regions(self, boss_selection)

    def create_item(self, name: str, override: Optional[ItemClassification] = None) -> "Item":
        createdthing = item_table[name]
        if override:
            return MetroidPrimeItem(name, override, createdthing.code, self.player)
        return MetroidPrimeItem(name, createdthing.classification, createdthing.code, self.player)

    def pre_fill(self) -> None:
        for location_name, item_name in self.prefilled_item_map.items():
            location = self.get_location(location_name)
            item = self.create_item(item_name, ItemClassification.progression)
            location.place_locked_item(item)

    def create_items(self) -> None:
        # add artifacts
        local_itempool = []
        items_added = 0
        for start_item in artifact_table:
            local_itempool += [self.create_item(start_item)]
            items_added += 1

        excluded = self.options.exclude_items

        # Create initial inventory from yaml and starting room
        start_inventory = []
        start_inventory += ALWAYS_START_INVENTORY
        start_inventory += [item.value for item in self.starting_room_data.selected_loadout.loadout]
        # start_inventory += [item.name for item in self.multiworld.precollected_items[self.player]]
        if not self.options.shuffle_scan_visor.value:
            start_inventory += [SuitUpgrade.Scan_Visor.value]

        if "Beam" not in "".join(start_inventory):
            start_inventory += [get_item_for_options(self, SuitUpgrade.Power_Beam).value]

        for start_item in start_inventory:
            # Pre collect the ones that start room loadout adds in
            item = self.create_item(start_item)
            if item not in self.multiworld.precollected_items[self.player]:
                self.multiworld.push_precollected(item)

        items_with_multiple = [SuitUpgrade.Missile_Expansion.value, SuitUpgrade.Power_Bomb_Expansion.value, SuitUpgrade.Energy_Tank.value]
        for start_item in {*suit_upgrade_table}:
            # get suitupgrade by string value

            if self.options.progressive_beam_upgrades.value and get_progressive_upgrade_for_item(SuitUpgrade.get_by_value(start_item)) is not None:
                continue

            # Don't add items that are already placed locally via start room logic or starting loadout to the multiworld pool.
            # Missile expansions, PB expansions, and energy tanks are added still since there are multiple of them.
            if start_item in self.prefilled_item_map.values() and start_item not in items_with_multiple:
                items_added += 1
                continue
            if start_item in start_inventory and start_item not in items_with_multiple:
                continue
            if start_item in excluded:
                continue
            if start_item == "Missile Expansion":
                for new_item in range(0, 8):
                    local_itempool += [self.create_item('Missile Expansion', ItemClassification.progression)]
                items_added += 8
            elif start_item == "Energy Tank":
                max_tanks = 14
                progression_tanks = 8
                for new_item in range(0, progression_tanks):
                    local_itempool += [self.create_item("Energy Tank", ItemClassification.progression)]
                for new_item in range(0, max_tanks - progression_tanks):
                    local_itempool += [self.create_item("Energy Tank")]
                items_added += max_tanks
            elif start_item == "Power Bomb Expansion":
                local_itempool += [self.create_item('Power Bomb Expansion', ItemClassification.progression)]
                for new_item in range(0, 4):
                    local_itempool += [self.create_item("Power Bomb Expansion")]
                items_added += 5
            else:
                local_itempool += [self.create_item(start_item)]
                items_added += 1

        if self.options.missile_launcher.value:
            if SuitUpgrade.Missile_Launcher.value not in start_inventory:
                items_added += 1
                if SuitUpgrade.Missile_Launcher.value not in self.prefilled_item_map.values():
                    local_itempool += [self.create_item(SuitUpgrade.Missile_Launcher.value)]

        if self.options.main_power_bomb.value:
            if SuitUpgrade.Main_Power_Bomb.value not in start_inventory:
                items_added += 1
                if SuitUpgrade.Main_Power_Bomb.value not in self.prefilled_item_map.values():
                    local_itempool += [self.create_item(SuitUpgrade.Main_Power_Bomb.value)]

        # Add progressive items if enabled
        if self.options.progressive_beam_upgrades.value:
            def quantity_in_start_inventory(item: ProgressiveUpgrade) -> int:
                return start_inventory.count(item.value)
            for progressive_item in PROGRESSIVE_ITEM_MAPPING:
                progression_per_item = 3
                to_make = progression_per_item - quantity_in_start_inventory(progressive_item)
                for i in range(to_make):
                    # Last item in the progression is useful (except power beam/super missile), the rest are progression
                    classification = ItemClassification.progression if i < to_make - 1 else ItemClassification.useful
                    if progressive_item == ProgressiveUpgrade.Progressive_Power_Beam:
                        classification = ItemClassification.progression  # Super missile is always progression
                    local_itempool += [self.create_item(progressive_item.value, classification)]
                    items_added += 1

        # add missiles in whatever slots we have left
        remain = 100 - items_added
        for start_item in range(0, remain):
            local_itempool += [self.create_item("Missile Expansion")]

        self.multiworld.itempool += local_itempool

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: (
            state.can_reach("Mission Complete", "Region", self.player))

    def post_fill(self) -> None:
        if self.options.artifact_hints.value:
            start_hints: typing.Set[str] = self.options.start_hints.value
            for i in artifact_table:
                start_hints.add(i)

    def generate_output(self, output_directory: str) -> None:
        if self.options.randomize_suit_colors:
            options: List[VariaSuitColorOverride] = [self.options.power_suit_color, self.options.varia_suit_color, self.options.gravity_suit_color, self.options.phazon_suit_color]
            for option in options:
                if option.value == 0:
                    option.value = self.random.randint(1, 35) * 10

        import json
        configjson = make_config(self)
        configjsons = json.dumps(configjson, indent=4)
        # Check if the environment variable 'DEBUG' is set to 'True'
        if os.environ.get('DEBUG') == 'True':
            with open("test_config.json", "w") as f:
                f.write(configjsons)

        options_dict = {
            "progressive_beam_upgrades": self.options.progressive_beam_upgrades.value,
            "player_name": self.player_name,
        }

        options_json = json.dumps(options_dict, indent=4)

        outfile_name = self.multiworld.get_out_file_name_base(self.player)
        apmp1 = MetroidPrimeContainer(configjsons, options_json, outfile_name, output_directory, player=self.player, player_name=self.multiworld.get_player_name(self.player))
        apmp1.write()

    def fill_slot_data(self) -> Dict[str, Any]:
        exclude_options = ["fusion_suit", "show_suit_index_on_pause_menu", "as_dict", "artifact_hints", "staggered_suit_damage", "start_hints"]
        non_cosmetic_options = [o for o in dir(self.options) if "color" not in o and o not in exclude_options and not o.startswith("__")]
        slot_data: Dict[str, Any] = self.options.as_dict(*non_cosmetic_options)

        return slot_data

        # for the universal tracker, doesn't get called in standard gen
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        # returning slot_data so it regens, giving it back in multiworld.re_gen_passthrough
        info("Regenerating world for tracker")
        return slot_data
