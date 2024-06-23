from enum import Enum
from BaseClasses import Item, ItemClassification

AP_METROID_PRIME_ITEM_ID_BASE = 5031000


class ItemData:
    name: str
    code: int
    classification: ItemClassification
    max_capacity: int
    id: int

    def __init__(self, name: str, id: int, progression: ItemClassification, max_capacity: int = 1) -> None:
        self.name = name
        self.id = id
        self.code = id + AP_METROID_PRIME_ITEM_ID_BASE
        self.classification = progression
        self.max_capacity = max_capacity


class MetroidPrimeItem(Item):
    game: str = "Metroid Prime"


class SuitUpgrade(Enum):
    Power_Beam = "Power Beam"
    Ice_Beam = "Ice Beam"
    Wave_Beam = "Wave Beam"
    Plasma_Beam = "Plasma Beam"
    Missile_Expansion = "Missile Expansion"
    Scan_Visor = "Scan Visor"
    Morph_Ball_Bomb = "Morph Ball Bomb"
    Power_Bomb_Expansion = "Power Bomb Expansion"
    Flamethrower = "Flamethrower"
    Thermal_Visor = "Thermal Visor"
    Charge_Beam = "Charge Beam"
    Super_Missile = "Super Missile"
    Grapple_Beam = "Grapple Beam"
    X_Ray_Visor = "X-Ray Visor"
    Ice_Spreader = "Ice Spreader"
    Space_Jump_Boots = "Space Jump Boots"
    Morph_Ball = "Morph Ball"
    Combat_Visor = "Combat Visor"
    Boost_Ball = "Boost Ball"
    Spider_Ball = "Spider Ball"
    Power_Suit = "Power Suit"
    Gravity_Suit = "Gravity Suit"
    Varia_Suit = "Varia Suit"
    Phazon_Suit = "Phazon Suit"
    Energy_Tank = "Energy Tank"
    Wavebuster = "Wavebuster"
    Missile_Launcher = "Missile Launcher"
    Main_Power_Bomb = "Power Bomb (Main)"


suit_upgrade_table: dict[str, ItemData] = {
    SuitUpgrade.Power_Beam.value: ItemData(SuitUpgrade.Power_Beam.value, 0, ItemClassification.progression),
    SuitUpgrade.Ice_Beam.value: ItemData(SuitUpgrade.Ice_Beam.value, 1, ItemClassification.progression),
    SuitUpgrade.Wave_Beam.value: ItemData(SuitUpgrade.Wave_Beam.value, 2, ItemClassification.progression),
    SuitUpgrade.Plasma_Beam.value: ItemData(SuitUpgrade.Plasma_Beam.value, 3, ItemClassification.progression),
    SuitUpgrade.Missile_Expansion.value: ItemData(SuitUpgrade.Missile_Expansion.value, 4, ItemClassification.filler, 999),
    SuitUpgrade.Scan_Visor.value: ItemData(SuitUpgrade.Scan_Visor.value, 5, ItemClassification.progression),
    SuitUpgrade.Morph_Ball_Bomb.value: ItemData(SuitUpgrade.Morph_Ball_Bomb.value, 6, ItemClassification.progression),
    SuitUpgrade.Power_Bomb_Expansion.value: ItemData(SuitUpgrade.Power_Bomb_Expansion.value, 7, ItemClassification.useful, 99),
    SuitUpgrade.Flamethrower.value: ItemData(SuitUpgrade.Flamethrower.value, 8, ItemClassification.useful),
    SuitUpgrade.Thermal_Visor.value: ItemData(SuitUpgrade.Thermal_Visor.value, 9, ItemClassification.progression),
    SuitUpgrade.Charge_Beam.value: ItemData(SuitUpgrade.Charge_Beam.value, 10, ItemClassification.progression),
    SuitUpgrade.Super_Missile.value: ItemData(SuitUpgrade.Super_Missile.value, 11, ItemClassification.progression),
    SuitUpgrade.Grapple_Beam.value: ItemData(SuitUpgrade.Grapple_Beam.value, 12, ItemClassification.progression),
    SuitUpgrade.X_Ray_Visor.value: ItemData(SuitUpgrade.X_Ray_Visor.value, 13, ItemClassification.progression),
    SuitUpgrade.Ice_Spreader.value: ItemData(SuitUpgrade.Ice_Spreader.value, 14, ItemClassification.useful),
    SuitUpgrade.Space_Jump_Boots.value: ItemData(SuitUpgrade.Space_Jump_Boots.value, 15, ItemClassification.progression),
    SuitUpgrade.Morph_Ball.value: ItemData(SuitUpgrade.Morph_Ball.value, 16, ItemClassification.progression),
    SuitUpgrade.Combat_Visor.value: ItemData(SuitUpgrade.Combat_Visor.value, 17, ItemClassification.progression),
    SuitUpgrade.Boost_Ball.value: ItemData(SuitUpgrade.Boost_Ball.value, 18, ItemClassification.progression),
    SuitUpgrade.Spider_Ball.value: ItemData(SuitUpgrade.Spider_Ball.value, 19, ItemClassification.progression),
    SuitUpgrade.Power_Suit.value: ItemData(SuitUpgrade.Power_Suit.value, 20, ItemClassification.progression),
    SuitUpgrade.Gravity_Suit.value: ItemData(SuitUpgrade.Gravity_Suit.value, 21, ItemClassification.progression),
    SuitUpgrade.Varia_Suit.value: ItemData(SuitUpgrade.Varia_Suit.value, 22, ItemClassification.progression),
    SuitUpgrade.Phazon_Suit.value: ItemData(SuitUpgrade.Phazon_Suit.value, 23, ItemClassification.progression),
    SuitUpgrade.Energy_Tank.value: ItemData(SuitUpgrade.Energy_Tank.value, 24, ItemClassification.useful, 14),
    SuitUpgrade.Wavebuster.value: ItemData(SuitUpgrade.Wavebuster.value, 28, ItemClassification.useful),
}

misc_item_table: dict[str, ItemData] = {
    "UnknownItem1": ItemData("UnknownItem1", 25, ItemClassification.useful),
    "Ice Trap": ItemData("Ice Trap", 27, ItemClassification.trap),
}

# These item ids are invalid in the player state, we'll need to exclude it from logic relying on that
custom_suit_upgrade_table: dict[str, ItemData] = {
    SuitUpgrade.Missile_Launcher.value: ItemData(SuitUpgrade.Missile_Launcher.value, 41, ItemClassification.progression),
    SuitUpgrade.Main_Power_Bomb.value: ItemData(SuitUpgrade.Main_Power_Bomb.value, 42, ItemClassification.progression),

}

artifact_table: dict[str, ItemData] = {
    "Artifact of Truth": ItemData("Artifact of Truth", 29, ItemClassification.progression),
    "Artifact of Strength": ItemData("Artifact of Strength", 30, ItemClassification.progression),
    "Artifact of Elder": ItemData("Artifact of Elder", 31, ItemClassification.progression),
    "Artifact of Wild": ItemData("Artifact of Wild", 32, ItemClassification.progression),
    "Artifact of Lifegiver": ItemData("Artifact of Lifegiver", 33, ItemClassification.progression),
    "Artifact of Warrior": ItemData("Artifact of Warrior", 34, ItemClassification.progression),
    "Artifact of Chozo": ItemData("Artifact of Chozo", 35, ItemClassification.progression),
    "Artifact of Nature": ItemData("Artifact of Nature", 36, ItemClassification.progression),
    "Artifact of Sun": ItemData("Artifact of Sun", 37, ItemClassification.progression),
    "Artifact of World": ItemData("Artifact of World", 38, ItemClassification.progression),
    "Artifact of Spirit": ItemData("Artifact of Spirit", 39, ItemClassification.progression),
    "Artifact of Newborn": ItemData("Artifact of Newborn", 40, ItemClassification.progression),
}

item_table: dict[str, ItemData] = {
    **suit_upgrade_table, **artifact_table, **custom_suit_upgrade_table, **misc_item_table}
