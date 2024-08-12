import typing

from ....Fill import distribute_items_restrictive

from ..config import make_config
from worlds.metroidprime.data.AreaNames import MetroidPrimeArea
from worlds.metroidprime.data.RoomNames import RoomName
from ..data.StartRoomData import StartRoomData, StartRoomDifficulty
from ..data.Transports import get_random_elevator_mapping, transport_names_to_room_names
from . import MetroidPrimeTestBase

if typing.TYPE_CHECKING:
    from .. import MetroidPrimeWorld


class TestNoDoorRando(MetroidPrimeTestBase):
    run_default_tests = False
    options = {
        "door_color_randomization": "none",
        "starting_room": 'normal'
    }

    def test_all_door_types_are_not_randomized_and_start_beam_is_power(self):
        self.world.generate_early()
        world: 'MetroidPrimeWorld' = self.world
        world.options.door_color_mapping = None

    def test_starting_beam_is_power(self):
        self.world.generate_early()
        world: 'MetroidPrimeWorld' = self.world
        distribute_items_restrictive(world.multiworld)
        config = make_config(world)
        assert config["gameConfig"]["startingItems"]["powerBeam"] == 1
