import typing

from Fill import distribute_items_restrictive

from ..DoorRando import BlastShieldType, DoorLockType

from ..config import make_config

from ..data.RoomNames import RoomName

from ..Items import SuitUpgrade

from . import MetroidPrimeTestBase

if typing.TYPE_CHECKING:
    from .. import MetroidPrimeWorld


class TestNoBlastShieldRando(MetroidPrimeTestBase):
    options = {
        "blast_shield_randomization": "none",
    }

    def test_all_blast_shields_are_not_randomized(self):
        """Verify that the blast shield to ruined shrine access is still there and not randomized"""
        test_region = RoomName.Ruined_Shrine_Access.value
        self.assertFalse(self.can_reach_region(test_region))
        self.collect(self.get_item_by_name(SuitUpgrade.Missile_Expansion.value))
        self.assertTrue(self.can_reach_region(test_region))

    def test_output_generates_correctly(self):
        world: 'MetroidPrimeWorld' = self.world
        distribute_items_restrictive(self.multiworld)
        config = make_config(world)
        level_key = config["levelData"]["Chozo Ruins"]["rooms"]
        self.assertTrue(level_key[RoomName.Main_Plaza.value]["doors"]["2"]["blastShieldType"] == BlastShieldType.Missile.value)
        self.assertTrue(level_key[RoomName.Ruined_Shrine_Access.value]["doors"]["1"]["blastShieldType"] == BlastShieldType.Missile.value)

        self.assertTrue(level_key[RoomName.Reflecting_Pool.value]["doors"]["3"]["blastShieldType"] == BlastShieldType.Missile.value)
        self.assertTrue(level_key[RoomName.Antechamber.value]["doors"]["0"]["blastShieldType"] == BlastShieldType.Missile.value, "Paired mapping is not set")
        self.assertTrue(level_key[RoomName.Antechamber.value]["doors"]["0"]["shieldType"] == DoorLockType.Blue.value, "Existing shield type override is not preserved")


# class TestReplaceBlastShieldRando(MetroidPrimeTestBase):
#     options = {
#         "blast_shield_randomization": "replace_existing"
#     }

#     def test_blast_shields_are_replaced(self):
#         """Verify that the blast shield to ruined shrine access is replaced"""
#         test_region = RoomName.Ruined_Shrine_Access.value
#         self.collect(self.get_item_by_name(SuitUpgrade.Missile_Expansion.value))
#         self.assertFalse(self.can_reach_region(test_region))
#       def test_blast_shields_are_paired(self):
