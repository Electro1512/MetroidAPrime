import os

import pytest

from BaseClasses import MultiWorld
from Fill import distribute_items_restrictive
from ..config import make_config
from ..data.StartRoomData import all_start_rooms
from . import MetroidPrimeTestBase

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'test_output')


class TestStartingRoomsGenerate(MetroidPrimeTestBase):
    auto_construct = False

    def test_starting_room_rando_no_missile_launcher(self):
        for room_name in all_start_rooms:
            with self.subTest(f"Starting Room: {room_name}", room_name=room_name):
                self.options = {
                    "starting_room_name": room_name
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
                      "missile_launcher": 1
                  }
                  try:
                      self.world_setup()
                      distribute_items_restrictive(self.multiworld)
                      self.assertBeatable(True)
                      self.multiworld = None
                      self.world = None
                  except Exception as e:
                      self.fail(f"Failed to generate beatable game with start room: {room_name}. ")

