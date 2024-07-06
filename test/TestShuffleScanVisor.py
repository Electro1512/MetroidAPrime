from ..Items import SuitUpgrade
from ..data.Tricks import TrickDifficulty
from . import MetroidPrimeTestBase


class TestScanVisorShuffled(MetroidPrimeTestBase):
    run_default_tests = False
    options = {
        "trick_difficulty": TrickDifficulty.Easy.value,
        "shuffle_scan_visor": True
    }

    def test_cannot_reach_alcove_with_tricks_enabled(self):
        assert self.can_reach_location("Tallon Overworld: Alcove") == False

    def test_do_not_start_with_scan_visor(self):
        assert SuitUpgrade.Scan_Visor.value not in [item.name for item in self.multiworld.precollected_items[self.player]]

    def test_scan_visor_not_in_item_pool(self):
        assert SuitUpgrade.Scan_Visor.value in [item.name for item in self.multiworld.itempool]


class TestScanVisorNotShuffled(MetroidPrimeTestBase):
    run_default_tests = False
    options = {
        "trick_difficulty": TrickDifficulty.Easy.value,
        "shuffle_scan_visor": False
    }

    def test_can_reach_alcove_with_tricks_enabled(self):
        assert self.can_reach_location("Tallon Overworld: Alcove") == True

    def test_start_with_scan_visor(self):
        assert SuitUpgrade.Scan_Visor.value in [item.name for item in self.multiworld.precollected_items[self.player]]

    def test_scan_visor_in_item_pool(self):
        assert SuitUpgrade.Scan_Visor.value not in [item.name for item in self.multiworld.itempool]
