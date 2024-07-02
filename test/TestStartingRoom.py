import os

from Fill import distribute_items_restrictive
from worlds.metroidprime.data.RoomNames import RoomName
from ..data.StartRoomData import all_start_rooms
from . import MetroidPrimeTestBase

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'test_output')


# class TestStartingRoomsGenerate(MetroidPrimeTestBase):
#     auto_construct = False

#     def test_starting_room_rando_no_missile_launcher(self):
#         for room_name in all_start_rooms:
#             with self.subTest(f"Starting Room: {room_name}", room_name=room_name):
#                 self.options = {
#                     "starting_room_name": room_name,
#                     "elevator_randomization": False,
#                     "missile_launcher": 0,
#                 }
#                 try:
#                     self.world_setup()
#                     distribute_items_restrictive(self.multiworld)
#                     self.assertBeatable(True)
#                 except Exception as e:
#                     self.fail(f"Failed to generate beatable game with start room: {room_name}. ")

#     def test_starting_room_rando_with_missile_launcher(self):
#         for room_name in all_start_rooms:
#             with self.subTest(f"Starting Room: {room_name}", room_name=room_name):
#                 self.options = {
#                     "starting_room_name": room_name,
#                     "elevator_randomization": False,
#                     "missile_launcher": 1,
#                 }
#                 try:
#                     self.world_setup()
#                     distribute_items_restrictive(self.multiworld)
#                     self.assertBeatable(True)
#                     self.multiworld = None
#                     self.world = None
#                 except Exception as e:
#                     self.fail(f"Failed to generate beatable game with start room: {room_name}. ")


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
