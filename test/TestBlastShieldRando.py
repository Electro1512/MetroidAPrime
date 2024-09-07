import math
import typing
from unittest import TestCase

from Fill import distribute_items_restrictive
from ..data.DoorData import get_door_data_by_room_names
from ..data.BlastShieldRegions import get_blast_shield_regions_by_area
from ..data.RoomData import AreaData
from ..data.AreaNames import MetroidPrimeArea
from ..BlastShieldRando import MAX_BEAM_COMBO_DOORS_PER_AREA, AreaBlastShieldMapping, BlastShieldType
from ..DoorRando import DoorLockType
from ..config import make_config
from ..data.RoomNames import RoomName
from ..Items import ProgressiveUpgrade, SuitUpgrade
from . import MetroidPrimeTestBase
if typing.TYPE_CHECKING:
    from .. import MetroidPrimeWorld
from ..data.PhazonMines import PhazonMinesAreaData
from ..data.PhendranaDrifts import PhendranaDriftsAreaData
from ..data.MagmoorCaverns import MagmoorCavernsAreaData
from ..data.ChozoRuins import ChozoRuinsAreaData
from ..data.TallonOverworld import TallonOverworldAreaData


def _get_default_area_data(area: MetroidPrimeArea) -> AreaData:
    mapping = {MetroidPrimeArea.Tallon_Overworld: TallonOverworldAreaData,
               MetroidPrimeArea.Chozo_Ruins: ChozoRuinsAreaData,
               MetroidPrimeArea.Magmoor_Caverns: MagmoorCavernsAreaData,
               MetroidPrimeArea.Phendrana_Drifts: PhendranaDriftsAreaData,
               MetroidPrimeArea.Phazon_Mines: PhazonMinesAreaData
               }

    return mapping[area]()


beam_combo_items = [BlastShieldType.Flamethrower, BlastShieldType.Ice_Spreader, BlastShieldType.Wavebuster]


class TestNoBlastShieldRando(MetroidPrimeTestBase):
    options = {
        "blast_shield_randomization": "none",
    }

    def test_all_blast_shields_are_not_randomized(self):
        """Verify that the blast shield to ruined shrine access is still there and not randomized"""
        test_region = RoomName.Ruined_Shrine_Access.value
        self.assertFalse(self.can_reach_region(test_region))
        self.collect_by_name(SuitUpgrade.Missile_Expansion.value)
        self.assertTrue(self.can_reach_region(test_region))

    def test_output_generates_correctly_with_paired_blast_shields(self):
        world: 'MetroidPrimeWorld' = self.world
        distribute_items_restrictive(self.multiworld)
        config = make_config(world)
        level_key = config["levelData"]["Chozo Ruins"]["rooms"]
        self.assertTrue(level_key[RoomName.Main_Plaza.value]["doors"]["2"]["blastShieldType"] == BlastShieldType.Missile.value)
        self.assertTrue(level_key[RoomName.Ruined_Shrine_Access.value]["doors"]["1"]["blastShieldType"] == BlastShieldType.Missile.value)

        self.assertTrue(level_key[RoomName.Reflecting_Pool.value]["doors"]["3"]["blastShieldType"] == BlastShieldType.Missile.value)
        self.assertTrue(level_key[RoomName.Antechamber.value]["doors"]["0"]["blastShieldType"] == BlastShieldType.Missile.value, "Paired mapping is not set")
        self.assertTrue(level_key[RoomName.Antechamber.value]["doors"]["0"]["shieldType"] == DoorLockType.Blue.value, "Existing shield type override is not preserved")


class TestReplaceBlastShieldRando(MetroidPrimeTestBase):
    options = {
        "blast_shield_randomization": "replace_existing"
    }

    def test_blast_shield_mapping_is_generated_for_each_vanilla_door(self):
        world: 'MetroidPrimeWorld' = self.world
        for area, mapping in world.blast_shield_mapping.items():
            blast_shield_doors = [door_id for room in _get_default_area_data(MetroidPrimeArea(area)).rooms.values() for door_id, door_data in room.doors.items() if door_data.blast_shield]
            mapped_doors = [door for room in mapping.type_mapping.values() for door in room.keys()]
            self.assertCountEqual(blast_shield_doors, mapped_doors, f"Missing doors in mapping for {area}")
            for room in mapping.type_mapping.values():
                for shield_type in room.values():
                    self.assertIn(shield_type, [shield for shield in BlastShieldType], "Invalid shield type")
                    self.assertNotEqual(shield_type, BlastShieldType.Missile, "Missile should not be included in mapping for replace_existing")

    def test_blast_shields_are_replaced_in_config(self):
        """Verify that the blast shield to ruined shrine access is replaced"""
        world: 'MetroidPrimeWorld' = self.world
        distribute_items_restrictive(self.multiworld)

        config = make_config(world)
        level_key = config["levelData"]["Chozo Ruins"]["rooms"]
        self.assertTrue(level_key[RoomName.Reflecting_Pool.value]["doors"]["3"]["blastShieldType"] != BlastShieldType.Missile.value)
        self.assertTrue(level_key[RoomName.Antechamber.value]["doors"]["0"]["blastShieldType"] != BlastShieldType.Missile.value, "Paired mapping is not set")
        self.assertTrue(level_key[RoomName.Antechamber.value]["doors"]["0"]["shieldType"] == DoorLockType.Blue.value, "Existing shield type override is not preserved")

    def test_beam_combos_are_not_included_in_mapping_by_default(self):
        world: 'MetroidPrimeWorld' = self.world
        for mapping in world.blast_shield_mapping.values():
            for room in mapping.type_mapping.values():
                for door in room.values():
                    self.assertNotIn(door, beam_combo_items)


class TestBlastShieldMapping(MetroidPrimeTestBase):
    run_default_tests = False
    options = {
        "blast_shield_randomization": "replace_existing",
        "blast_shield_available_types": "all",
        "blast_shield_mapping": {
            "Tallon Overworld": {
                "area": "Tallon Overworld",
                "type_mapping": {
                    "Landing Site": {
                        1: "Bomb",
                        2: "Flamethrower"
                    }
                }
            }
        }
    }

    def test_blast_shield_mapping_passed_as_option_applies_to_logic(self):
        test_region = RoomName.Canyon_Cavern.value
        world: 'MetroidPrimeWorld' = self.world
        self.assertEqual(
            world.blast_shield_mapping[MetroidPrimeArea.Tallon_Overworld.value],
            AreaBlastShieldMapping(MetroidPrimeArea.Tallon_Overworld.value, {"Landing Site": {1: BlastShieldType.Bomb, 2: BlastShieldType.Flamethrower}})
        )
        self.assertFalse(self.can_reach_region(test_region))
        self.collect_by_name([SuitUpgrade.Morph_Ball_Bomb.value, SuitUpgrade.Morph_Ball.value])
        self.assertTrue(self.can_reach_region(test_region))

    def test_beam_combos_are_included_in_logic_without_progressive_beams(self):
        test_region = RoomName.Temple_Hall.value
        self.assertFalse(self.can_reach_region(test_region))

        self.collect_by_name([SuitUpgrade.Flamethrower.value])
        self.assertFalse(self.can_reach_region(test_region))

        self.collect_by_name([
            SuitUpgrade.Plasma_Beam.value,
            SuitUpgrade.Charge_Beam.value,
            SuitUpgrade.Missile_Expansion.value,
        ])
        self.assertTrue(self.can_reach_region(test_region))


class TestBlastShieldMappingWithProgressiveBeams(MetroidPrimeTestBase):
    run_default_tests = False
    options = {
        "blast_shield_randomization": "replace_existing",
        "blast_shield_available_types": "all",
        "progressive_beam_upgrades": True,
        "blast_shield_mapping": {
            "Tallon Overworld": {
                "area": "Tallon Overworld",
                "type_mapping": {
                    "Landing Site": {
                        1: "Bomb",
                        2: "Flamethrower"
                    }
                }
            }
        }
    }

    def test_beam_combos_are_included_in_logic_with_progressive_beams(self):
        test_region = RoomName.Temple_Hall.value
        self.assertFalse(self.can_reach_region(test_region))
        self.collect_by_name([
            SuitUpgrade.Missile_Expansion.value,
            ProgressiveUpgrade.Progressive_Plasma_Beam.value,
            ProgressiveUpgrade.Progressive_Plasma_Beam.value,
            ProgressiveUpgrade.Progressive_Plasma_Beam.value,
        ])
        self.assertTrue(self.can_reach_region(test_region))


class TestIncludeBeamCombos(MetroidPrimeTestBase):
    options = {
        "blast_shield_randomization": "replace_existing",
        "blast_shield_available_types": "all",
    }

    def test_beam_combos_are_included_within_limits(self):
        world: 'MetroidPrimeWorld' = self.world
        for area, mapping in world.blast_shield_mapping.items():
            beam_combo_count = 0
            for room in mapping.type_mapping.values():
                for shieldType in room.values():
                    if shieldType in beam_combo_items:
                        beam_combo_count += 1
            self.assertLessEqual(beam_combo_count, MAX_BEAM_COMBO_DOORS_PER_AREA, f"Too many beam combos in {area}, {beam_combo_count} found")


class TestMixItUpBlastShieldRando(MetroidPrimeTestBase):
    options = {
        "blast_shield_randomization": "mix_it_up",
        "blast_shield_frequency": "medium",
        "trick_difficulty": "easy"
    }

    def test_blast_shields_are_placed_in_regions_with_appropriate_quantities(self):
        world: 'MetroidPrimeWorld' = self.world
        for area, mapping in world.blast_shield_mapping.items():
            blast_shield_count = 0
            total_available_blast_shield_options = len(get_blast_shield_regions_by_area(MetroidPrimeArea(area)).regions)
            for room in mapping.type_mapping.values():
                blast_shield_count += len(room.values())
            self.assertGreater(blast_shield_count, 0, f"No blast shields found in {area}")
            self.assertEqual(blast_shield_count, math.ceil(total_available_blast_shield_options * world.options.blast_shield_frequency * .1), f"Invalid number of blast shields in {area}, {blast_shield_count} found")


class TestBlastShieldRegionMapping(MetroidPrimeTestBase):
    """These mappings are manually entered, so we need to verify that they are valid"""
    run_default_tests = False

    def test_each_room_is_paired_to_a_valid_room(self):
        invalid_rooms = []
        for area in MetroidPrimeArea:
            blast_shield_mapping = get_blast_shield_regions_by_area(area)
            for region in blast_shield_mapping.regions:
                for source_room, target_room in region.doors.items():
                    door_data = get_door_data_by_room_names(source_room, target_room, area, self.world)
                    if not door_data:
                        invalid_rooms.append((source_room, target_room, area))
        self.assertFalse(invalid_rooms, f"Invalid room pairings found: {invalid_rooms}")
