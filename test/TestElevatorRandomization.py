from worlds.metroidprime.data.Transports import get_random_elevator_mapping
from worlds.metroidprime.test import MetroidPrimeTestBase


class TestStartingRoomsGenerate(MetroidPrimeTestBase):
    auto_construct = True
    options = {
        "elevator_randomization": True
    }

    def test_elevator_randomization(self):
      mapping = get_random_elevator_mapping(self.world)
      pass