
from Options import DeathLink, DefaultOnToggle, TextChoice, Toggle, Range, ItemDict, StartInventoryPool, Choice, PerGameCommonOptions, Visibility
from dataclasses import dataclass

from worlds.metroidprime.data.StartRoomData import StartRoomDifficulty


class SpringBall(Toggle):
    """Adds Spring Ball to the item pool. This item will allow you to jump in Morph Ball mode,
    significantly reducing the necessity of bomb jumps. Does not change the logic at this current time."""
    display_name = "Add Spring Ball"


class RequiredArtifacts(Range):
    """Determines the amount of Artifacts needed to begin the endgame sequence."""
    display_name = "Required Artifacts"
    range_start = 1
    range_end = 12
    default = 12


class ExcludeItems(ItemDict):
    """Replaces the following items with filler. INPUT AT YOUR OWN RISK. I cannot promise that removing
    progression items will not break logic. (for now please leave the default starting items in)"""
    verify_item_name = True
    display_name = "Exclude Items"


class FinalBosses(Choice):
    """Determines the final bosses required to beat the seed. Choose from Meta Ridley, Metroid Prime,
    both, or neither."""
    display_name = "Final Boss Select"
    option_both = 0
    option_ridley = 1
    option_prime = 2
    option_none = 3
    default = 0


class ArtifactHints(DefaultOnToggle):
    """If enabled, scanning the artifact stones in the temple will give a hint to their location"""
    display_name = "Artifact Hints"
    default = True


class MissileLauncher(DefaultOnToggle):
    """If enabled, the missile launcher will be added to the item pool. This will only allow you to use missiles once the missile launcher is found (regardless of missile expansions received)."""
    display_name = "Missile Launcher"
    default = False


class MainPowerBomb(DefaultOnToggle):
    """If enabled, the main power bomb will be added to the item pool. This will only allow you to use power bombs once the main power bombs is found (regardless of power bomb expansions received)."""
    display_name = "Main Power Bomb"
    default = False


class NonVariaHeatDamage(DefaultOnToggle):
    """If enabled, the gravity suit and phazon suit will not protect against heat damage which will change the required logic of the game"""
    display_name = "Non-Varia Heat Damage"
    default = True


class StaggeredSuitDamage(Choice):
    """Configure how suit damage reduction is calculated
    Default: based on the strongest suit you have
    Progressive: based on the number of suits you have
    Additive: Individual suits provide their added damage reduction
    """
    display_name = "Staggered Suit Damage"
    option_default = "Default"
    option_progressive = "Progressive"
    option_additive = "Additive"
    default = "Progressive"


class RemoveHiveMecha(Toggle):
    """If enabled, the trigger for the Hive Mecha boss will be removed from the game"""
    display_name = "Remove Hive Mecha"
    default = False


class FusionSuit(Toggle):
    """Whether to use the fusion suit or not"""
    display_name = "Fusion Suit"
    default = False


class TrickDifficulty(Choice):
    """Determines which tricks, if any, are required to complete the seed. This will affect the logic of the game."""
    display_name = "Trick Difficulty"
    option_no_tricks = -1
    option_easy = 0
    option_medium = 1
    option_hard = 2
    default = -1


class BackwardsLowerMines(DefaultOnToggle):
    """If enabled, allows the player to progress through the lower mines in reverse"""
    display_name = "Backwards Lower Mines"


class RemoveXrayRequirements(Toggle):
    """If enabled, removes xray visor requirements for everything but omega pirate and metroid prime"""
    display_name = "Remove Xray Visor Requirements"
    default = False


class RemoveThermalRequirements(Toggle):
    """If enabled, removes thermal visor requirements for everything but metroid prime (note this means wave beam panels will be in logic without the visor to see them)"""
    display_name = "Remove Thermal Visor Requirements"
    default = False


class StartingRoom(Choice):
    """Determines the starting room of the game. This will change your starting loadout depending on the room
  normal: Start at the Talon Overworld Landing Site
  safe: Start in rooms that will not require a significant combat challenge to progress from
  buckle_up: Start in rooms that will pose a significant challenge to players with no energy tanks or suit upgrades. Fun for the aspiring masochist (less fun for their friends in BK).
    """
    option_normal = StartRoomDifficulty.Normal.value
    option_safe = StartRoomDifficulty.Safe.value
    option_buckle_up = StartRoomDifficulty.Buckle_Up.value
    default = StartRoomDifficulty.Normal.value


class StartingRoomName(TextChoice):
    """Should not be shown in ui, can be used to override the starting room"""
    display_name = "Starting Room Name"
    default = ""
    visibility = Visibility.spoiler

@dataclass
class MetroidPrimeOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    spring_ball: SpringBall
    required_artifacts: RequiredArtifacts
    exclude_items: ExcludeItems
    final_bosses: FinalBosses
    death_link: DeathLink
    artifact_hints: ArtifactHints
    missile_launcher: MissileLauncher
    main_power_bomb: MainPowerBomb
    non_varia_heat_damage: NonVariaHeatDamage
    staggered_suit_damage: StaggeredSuitDamage
    remove_hive_mecha: RemoveHiveMecha
    fusion_suit: FusionSuit
    trick_difficulty: TrickDifficulty
    backwards_lower_mines: BackwardsLowerMines
    remove_xray_requirements: RemoveXrayRequirements
    remove_thermal_requirements: RemoveThermalRequirements
    starting_room: StartingRoom
    starting_room_name: StartingRoomName
