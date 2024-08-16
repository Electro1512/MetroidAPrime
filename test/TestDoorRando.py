import typing

from Fill import distribute_items_restrictive
from ..DoorRando import DoorLockType

from ..config import make_config
from worlds.metroidprime.data.AreaNames import MetroidPrimeArea
from worlds.metroidprime.data.RoomNames import RoomName
from ..data.StartRoomData import StartRoomData, StartRoomDifficulty
from ..data.Transports import get_random_elevator_mapping, transport_names_to_room_names
from . import MetroidPrimeTestBase

if typing.TYPE_CHECKING:
    from .. import MetroidPrimeWorld


class TestNoDoorRando(MetroidPrimeTestBase):
    options = {
        "door_color_randomization": "none",
    }

    def test_all_door_types_are_not_randomized(self):
        self.world.generate_early()
        world: 'MetroidPrimeWorld' = self.world
        self.assertEqual(world.door_color_mapping, None)

    def test_starting_beam_is_power(self):
        self.world.generate_early()
        world: 'MetroidPrimeWorld' = self.world
        distribute_items_restrictive(world.multiworld)
        config = make_config(world)
        self.assertTrue(config["gameConfig"]["startingItems"]["powerBeam"] == 1)
        self.assertEqual(config["gameConfig"]["startingBeam"], "Power", "Starting beam should be Power")


class TestGlobalDoorRando(MetroidPrimeTestBase):
    options = {
        "door_color_randomization": "global",
    }

    def test_all_door_types_are_randomized_globally(self):
        self.world.generate_early()
        world: 'MetroidPrimeWorld' = self.world
        first_mapping = None
        self.assertTrue(len(world.door_color_mapping) > 0, "Door color mapping should not be empty")
        for area in MetroidPrimeArea:
            if world.door_color_mapping[area.value].type_mapping is None:
                continue
            if first_mapping is None:
                first_mapping = world.door_color_mapping[area.value].type_mapping
                for original, new in first_mapping.items():
                    self.assertNotEqual(original, new, "Door color should be randomized")
            else:
                self.assertEqual(first_mapping, world.door_color_mapping[area.value].type_mapping, "Door color should be the same for all areas")

    def test_door_colors_are_updated_in_config(self):
        self.world.generate_early()
        world: 'MetroidPrimeWorld' = self.world
        distribute_items_restrictive(world.multiworld)
        config = make_config(world)
        self.assertNotEqual(config["levelData"]["Chozo Ruins"]["rooms"]["Ruined Shrine"]["doors"]["0"]["shieldType"], DoorLockType.Wave.value)


class TestRegionalDoorRando(MetroidPrimeTestBase):
    options = {
        "door_color_randomization": "regional",
    }

    def test_all_door_types_are_randomized_across_a_region(self):
        self.world.generate_early()
        world: 'MetroidPrimeWorld' = self.world
        first_mapping = None
        self.assertTrue(len(world.door_color_mapping) > 0, "Door color mapping should not be empty")
        same_areas = []
        for area in MetroidPrimeArea:
            if world.door_color_mapping[area.value].type_mapping is None or area == MetroidPrimeArea.Impact_Crater:
                continue
            if first_mapping is None:
                first_mapping = world.door_color_mapping[area.value].type_mapping
                for original, new in first_mapping.items():
                    self.assertNotEqual(original, new, "Door color should be randomized")
            elif first_mapping == world.door_color_mapping[area.value].type_mapping:
                same_areas.append(area)
        self.assertTrue(len(same_areas) < 3, "Door color should be different for each area generally")

    def test_door_colors_are_updated_in_config(self):
        self.world.generate_early()
        world: 'MetroidPrimeWorld' = self.world
        distribute_items_restrictive(world.multiworld)
        config = make_config(world)
        self.assertNotEqual(config["levelData"]["Chozo Ruins"]["rooms"]["Ruined Shrine"]["doors"]["0"]["shieldType"], DoorLockType.Wave.value)


class TestDoorRandoWithDifferentStartRoomNonRequiredBeam(MetroidPrimeTestBase):
    options = {
        "door_color_randomization": "global",
        "starting_room_name": RoomName.Tower_Chamber.value,
    }

    def test_starting_beam_is_not_wave(self):
        self.world.generate_early()
        world: 'MetroidPrimeWorld' = self.world
        distribute_items_restrictive(world.multiworld)
        config = make_config(world)
        self.assertTrue(config["gameConfig"]["startingItems"]["wave"] == 0)
        self.assertTrue(config["gameConfig"]["startingItems"]["ice"] == 1)
        self.assertEqual(config["gameConfig"]["startingBeam"], "Ice", "Starting beam should be Ice")


class TestDoorRandoWithDifferentStartRoomWithRequiredBeam(MetroidPrimeTestBase):
    options = {
        "door_color_randomization": "global",
        "starting_room_name": RoomName.Save_Station_B.value,
    }

    def test_starting_beam_is_not_wave(self):
        self.world.generate_early()
        world: 'MetroidPrimeWorld' = self.world
        distribute_items_restrictive(world.multiworld)
        config = make_config(world)
        self.assertTrue(config["gameConfig"]["startingItems"]["plasma"] == 1)
        self.assertEqual(config["gameConfig"]["startingBeam"], "Plasma", "Starting beam should be Plasm")


class TestDoorPlando(MetroidPrimeTestBase):
    options = {
        "door_color_randomization": "global",
        "door_color_mapping": {
            "Chozo Ruins": {
                "Wave Beam": "Ice Beam",
                "Ice Beam": "Plasma Beam",
                "Plasma Beam": "Wave Beam"
            },
            "Magmoor Caverns": {
                "Wave Beam": "Plasma Beam",
                "Ice Beam": "Wave Beam",
                "Plasma Beam": "Ice Beam"
            },
            "Phendrana Drifts": {
                "Wave Beam": "Plasma Beam",
                "Ice Beam": "Wave Beam",
                "Plasma Beam": "Ice Beam"
            },
            "Tallon Overworld": {
                "Wave Beam": "Plasma Beam",
                "Ice Beam": "Wave Beam",
                "Plasma Beam": "Ice Beam"
            },
            "Phazon Mines": {
                "Wave Beam": "Plasma Beam",
                "Ice Beam": "Wave Beam",
                "Plasma Beam": "Ice Beam"
            }
        }
    }

    def test_door_mapping_gets_set_from_plando(self):
        self.world.generate_early()
        world: 'MetroidPrimeWorld' = self.world
        self.assertTrue(len(world.door_color_mapping) > 0, "Door color mapping should not be empty")
        for area in MetroidPrimeArea:
            if area == MetroidPrimeArea.Impact_Crater:
                continue
            self.assertEqual(world.door_color_mapping[area.value].type_mapping, world.options.door_color_mapping.get(area.value), "Door color mapping should be set from plando")
