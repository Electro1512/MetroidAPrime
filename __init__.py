from typing import Any, Dict, List, Optional
import os
import typing
from BaseClasses import Item, Tutorial, ItemClassification
from worlds.generic.Rules import add_item_rule, forbid_item
from .Container import MetroidPrimeContainer
from .data.RoomNames import RoomName
from .data.StartRoomData import StartRoomData, init_starting_room_data
from .Items import MetroidPrimeItem, SuitUpgrade, suit_upgrade_table, artifact_table, item_table
from .PrimeOptions import MetroidPrimeOptions, VariaSuitColorOverride
from .Locations import every_location
from .Regions import create_regions
from .config import make_config
from .data.Transports import default_elevator_mappings
from worlds.AutoWorld import World, WebWorld
import settings
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess


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
ALWAYS_START_INVENTORY = [SuitUpgrade.Scan_Visor.value, SuitUpgrade.Power_Suit.value, SuitUpgrade.Combat_Visor.value]


class MetroidPrimeWorld(World):
    """
    Metroid Prime is a first-person action-adventure game originally for the Gamecube. Play as
    the bounty hunter Samus Aran as she traverses the planet Tallon IV and uncovers the plans
    of the Space Pirates.
    """
    game = "Metroid Prime"
    web = MetroidPrimeWeb()
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

    def get_filler_item_name(self) -> str:
        return SuitUpgrade.Missile_Expansion.value

    def generate_early(self) -> None:
        init_starting_room_data(self)

    def create_regions(self) -> None:
        boss_selection = int(self.options.final_bosses)
        create_regions(self, boss_selection)

    def create_item(self, name: str, override: bool = False) -> "Item":
        createdthing = item_table[name]
        if override:
            return MetroidPrimeItem(name, ItemClassification.progression, createdthing.code, self.player)
        return MetroidPrimeItem(name, createdthing.classification, createdthing.code, self.player)

    def pre_fill(self) -> None:
        for location_name, item_name in self.prefilled_item_map.items():
            location = self.get_location(location_name)
            item = self.create_item(item_name, True)
            location.place_locked_item(item)

    def create_items(self) -> None:
        # add artifacts
        items_added = 0
        for i in artifact_table.keys():
            self.multiworld.itempool += [self.create_item(i)]
            items_added += 1

        excluded = self.options.exclude_items

        # Create initial inventory from yaml and starting room
        start_inventory = []
        start_inventory += ALWAYS_START_INVENTORY
        start_inventory += [item.value for item in self.starting_room_data.selected_loadout.loadout]
        start_inventory += [item.name for item in self.multiworld.precollected_items[self.player]]

        if "Beam" not in "".join(start_inventory):
            start_inventory += [SuitUpgrade.Power_Beam.value]

        for i in start_inventory:
            self.multiworld.push_precollected(self.create_item(i))

        for i in {*suit_upgrade_table}:
            # Don't add items that are already placed locally via start room logic or starting loadout to the multiworld pool.
            # Missile expansions should still be added since there are multiple
            if i in self.prefilled_item_map.values() and i != SuitUpgrade.Missile_Expansion.value:
                items_added += 1
                continue
            elif i in start_inventory:
                continue

            if i in excluded.keys():
                continue
            elif i == "Missile Expansion":
                for j in range(0, 8):
                    self.multiworld.itempool += [
                        self.create_item('Missile Expansion', True)]
                items_added += 8
            elif i == "Energy Tank":
                for j in range(0, 8):
                    self.multiworld.itempool += [
                        self.create_item("Energy Tank", True)]
                for j in range(0, 6):
                    self.multiworld.itempool += [
                        self.create_item("Energy Tank")]
                items_added += 14
                continue
            elif i == "Power Bomb Expansion":
                self.multiworld.itempool += [self.create_item('Power Bomb Expansion', True)]
                for j in range(0, 4):
                    self.multiworld.itempool += [
                        self.create_item("Power Bomb Expansion")]
                items_added += 5
            else:
                self.multiworld.itempool += [self.create_item(i)]
                items_added += 1

        if self.options.missile_launcher.value:
            if SuitUpgrade.Missile_Launcher.value not in start_inventory:
                items_added += 1
                if SuitUpgrade.Missile_Launcher.value not in self.prefilled_item_map.values():
                    self.multiworld.itempool += [self.create_item(SuitUpgrade.Missile_Launcher.value)]

        if self.options.main_power_bomb.value:
            if SuitUpgrade.Main_Power_Bomb.value not in start_inventory:
                items_added += 1
                if SuitUpgrade.Main_Power_Bomb.value not in self.prefilled_item_map.values():
                    self.multiworld.itempool += [self.create_item(SuitUpgrade.Main_Power_Bomb.value)]

        # add missiles in whatever slots we have left
        remain = 100 - items_added
        for i in range(0, remain):
            self.multiworld.itempool += [self.create_item("Missile Expansion")]

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: (
            state.can_reach("Mission Complete", "Region", self.player))

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

        # convert configjson to json

        outfile_name = self.multiworld.get_out_file_name_base(self.player)
        apmp1 = MetroidPrimeContainer(configjsons, outfile_name, output_directory, player=self.player, player_name=self.multiworld.get_player_name(self.player))
        apmp1.write()

    def fill_slot_data(self) -> Dict[str, Any]:

        slot_data: Dict[str, Any] = {
            "spring_ball": self.options.spring_ball.value,
            "death_link": self.options.death_link.value,
            "required_artifacts": self.options.required_artifacts.value,
            "missile_launcher": self.options.missile_launcher.value,
            "main_power_bomb": self.options.main_power_bomb.value,
            "non_varia_heat_damage": self.options.non_varia_heat_damage.value,
            "exclude_items": self.options.exclude_items.value,
            "final_bosses": self.options.final_bosses.value,
        }

        return slot_data

    def post_fill(self) -> None:
        if self.options.artifact_hints.value:
            start_hints: typing.Set[str] = self.options.start_hints.value
            for i in artifact_table.keys():
                start_hints.add(i)
