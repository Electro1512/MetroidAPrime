import os

from Fill import distribute_items_restrictive
from worlds.metroidprime.Items import SuitUpgrade
from worlds.metroidprime.data.RoomNames import RoomName
from ..data.StartRoomData import StartRoomDifficulty, all_start_rooms
from . import MetroidPrimeTestBase
from .. import MetroidPrimeWorld


class TestStartingRoomsGenerate(MetroidPrimeTestBase):
    auto_construct = False

    def test_starting_room_rando_no_missile_launcher(self):
        for room_name in all_start_rooms:
            with self.subTest(f"Starting Room: {room_name}", room_name=room_name):
                self.options = {
                    "starting_room_name": room_name,
                    "elevator_randomization": False,
                    "missile_launcher": 0,
                }
                try:
                    self.world_setup()
                    distribute_items_restrictive(self.multiworld)
                    self.assertBeatable(True)
                except Exception as e:
                    self.fail(f"Failed to generate beatable game with start room: {room_name}. ")

    def test_starting_room_rando_with_missile_launcher(self):
        for room_name in all_start_rooms:
            with self.subTest(f"Starting Room: {room_name}", room_name=room_name):
                self.options = {
                    "starting_room_name": room_name,
                    "elevator_randomization": False,
                    "missile_launcher": 1,
                }
                try:
                    self.world_setup()
                    distribute_items_restrictive(self.multiworld)
                    self.assertBeatable(True)
                    self.multiworld = None
                    self.world = None
                except Exception as e:
                    self.fail(f"Failed to generate beatable game with start room: {room_name}. ")


class TestStartingRoomsGenerateWithElevatorRando(MetroidPrimeTestBase):
    auto_construct = False

    def test_starting_room_rando_with_elevator_rando(self):
        failures = []
        for room_name in all_start_rooms:
            # Landing site is not viable for elevator randomization w/o tricks
            if room_name == RoomName.Landing_Site.value:
                continue
            with self.subTest(f"Starting Room: {room_name}", room_name=room_name):
                self.options = {
                    "starting_room_name": room_name,
                    "elevator_randomization": True,
                    "missile_launcher": 1
                }
                try:
                    self.world_setup()
                    distribute_items_restrictive(self.multiworld)
                    self.assertBeatable(True)
                    self.multiworld = None
                    self.world = None
                except Exception as e:
                    failures.append(room_name)
        if len(failures):
            self.fail("Failed to generate beatable game with start rooms: " + ", ".join(failures))


class TestStartRoomBKPreventionDisabled(MetroidPrimeTestBase):
    run_default_tests = False
    options = {
        "starting_room_name": RoomName.Save_Station_B.value,
        "elevator_randomization": False,
        "disable_starting_room_bk_prevention": True
    }

    def test_disabling_bk_prevention_does_not_give_items_or_pre_fill(self):
        self.world.generate_early()
        world: MetroidPrimeWorld = self.world
        # Normally you'd also have the misssile launcher
        assert world.starting_room_data.selected_loadout.loadout == [SuitUpgrade.Plasma_Beam]
        assert len(world.prefilled_item_map.keys()) == 0


class TestStartRoomBKPreventionEnabled(MetroidPrimeTestBase):
    run_default_tests = False
    options = {
        "starting_room_name": RoomName.Save_Station_B.value,
        "elevator_randomization": False,
        "disable_starting_room_bk_prevention": False
    }

    def test_enabling_bk_prevention_gives_items_and_pre_fills_locations(self):
        self.world.generate_early()
        world: MetroidPrimeWorld = self.world
        # Normally you'd also have the misssile launcher
        assert world.starting_room_data.selected_loadout.loadout == [SuitUpgrade.Plasma_Beam, SuitUpgrade.Missile_Expansion]
        assert len(world.prefilled_item_map.keys()) == 1


class TestBuckleUpStartingRoom(MetroidPrimeTestBase):
    run_default_tests = False
    options = {
        "starting_room": StartRoomDifficulty.Buckle_Up.value
    }

    def test_buckle_up(self):
        available_room_names = [name for name, room in all_start_rooms.items() if room.difficulty.value == StartRoomDifficulty.Buckle_Up.value]
        self.assertTrue(self.world.options.starting_room_name.value in available_room_names)


class TestNormalStartingRoom(MetroidPrimeTestBase):
    run_default_tests = False
    options = {
        "starting_room": StartRoomDifficulty.Normal.value
    }

    def test_buckle_up(self):
        self.assertTrue(self.world.options.starting_room_name.value == RoomName.Landing_Site.value)
