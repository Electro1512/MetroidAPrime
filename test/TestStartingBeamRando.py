
import typing

from ..config import make_config

from Fill import distribute_items_restrictive

from ..Items import SuitUpgrade

from .. import MetroidPrimeWorld
from . import MetroidPrimeTestBase

if typing.TYPE_CHECKING:
    from .. import MetroidPrimeWorld


class TestStartingBeamRandomization(MetroidPrimeTestBase):
    auto_construct = False
    options = {
        "randomize_starting_beam": True,
    }

    def test_power_beam_is_not_the_starting_weapon_when_randomized(self):
        self.world.generate_early()
        world: 'MetroidPrimeWorld' = self.world
        world.create_items()
        self.assertGreater(len(world.multiworld.precollected_items[world.player]), 0)
        self.assertNotIn(SuitUpgrade.Power_Beam.value, world.multiworld.precollected_items[world.player])
        # Need to still verify this works
        self.assertTrue(False)

    def test_hive_mecha_is_disabled_if_starting_at_landing_site_and_power_beam_is_not_starting_weapon(self):
        self.world_setup()
        world: 'MetroidPrimeWorld' = self.world
        distribute_items_restrictive(self.multiworld)
        config = make_config(world)
        self.assertEqual(config["gameConfig"]["removeHiveMecha"], True)
        self.assertTrue(False)
