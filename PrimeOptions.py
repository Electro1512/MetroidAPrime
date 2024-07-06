
from enum import Enum
from Options import DeathLink, DefaultOnToggle, OptionDict, OptionList, TextChoice, Toggle, Range, ItemDict, StartInventoryPool, Choice, PerGameCommonOptions, Visibility
from dataclasses import dataclass
from .data.StartRoomData import StartRoomDifficulty
from .LogicCombat import CombatLogicDifficulty


class HudColor(Enum):
    DEFAULT = [102/255, 174/255, 225/255]
    RED = [1, 0, 0]
    GREEN = [0, 1, 0]
    BLUE = [0, 0, 1]
    VIOLET = [1, 0, 1]
    YELLOW = [1, 1, 0]
    CYAN = [0, 1, 1]
    WHITE = [1, 1, 1]
    ORANGE = [1, 0.5, 0]
    PINK = [1, 0.5, 1]
    LIME = [0.5, 1, 0]
    TEAL = [0.5, 1, 1]
    PURPLE = [0.5, 0, 1]


class SpringBall(Toggle):
    """Enables the spring ball when you receive Morph Ball Bombs. This will allow you to jump while in morph ball form by pressing up on the c stick, reducing the complexity of double bomb jumps."""
    display_name = "Add Spring Ball"
    default = True


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
    """If enabled, scanning the artifact stones in the temple will give a hint to their location. Additionally, hints will be pre collected in the client"""
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

class ShuffleScanVisor(Toggle):
    """If enabled, the scan visor will be shuffled into the item pool and will need to be found in order to scan dash and open certain locks"""
    display_name = "Shuffle Scan Visor"
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


class TrickAllowList(OptionList):
    """A list of tricks to explicitly allow in logic, regardless of selected difficulty. Values should match the trick name found here: https://github.com/Electro1512/MetroidAPrime/blob/main/data/Tricks.py#L55
       For example, "Crashed Frigate Scan Dash" or "Alcove Escape" """
    default = []


class TrickDenyList(OptionList):
    """A list of tricks to explicitly deny in logic, regardless of selected difficulty. Values should match the trick name found here: https://github.com/Electro1512/MetroidAPrime/blob/main/data/Tricks.py#L55. For example, "Crashed Frigate Scan Dash" or "Alcove Escape" """
    default = []


class BackwardsLowerMines(Toggle):
    """If enabled, allows the player to progress through the lower mines in reverse by removing the locks in the PCA room"""
    display_name = "Backwards Lower Mines"
    default = False


class FlaahgraPowerBombs(Toggle):
    """If enabled, makes the sandstone block at the top of arboretum breakable with power bombs. Note that this will require the player to have 4 power bombs in order to defeat flaahgra"""
    display_name = "Flaahgra Power Bombs"
    default = False


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


class DisableStartingRoomBKPrevention(Toggle):
    """Normally, starting rooms will give you a minimum set of items in order to have access to several checks immediately. This option disables that behavior as well as any pre filled items that would have been set.
       WARNING: This will possibly require multiple attempts to generate, especially in solo worlds
"""
    display_name = "Disable Starting Room BK Prevention"
    default = False


class StartingRoomName(TextChoice):
    """Should not be shown in ui, can be used to override the starting room"""
    display_name = "Starting Room Name"
    default = ""
    visibility = Visibility.spoiler


class CombatLogicDifficultyOption(Choice):
    """When enabled, the game will include energy tanks and the charge beam as requirements for certain combat heavy rooms"""
    display_name = "Combat Logic Difficulty"
    default = CombatLogicDifficulty.NORMAL.value
    option_no_logic = CombatLogicDifficulty.NO_LOGIC.value
    option_normal_logic = CombatLogicDifficulty.NORMAL.value
    option_minimal_logic = CombatLogicDifficulty.MINIMAL.value


class ElevatorRandomization(Toggle):
    """Randomizes the elevators between regions"""
    display_name = "Elevator Randomization"
    default = False


class ElevatorMapping(OptionDict):
    """Which elevators go to which regions, only visible for spoiler"""
    visibility = Visibility.spoiler
    default = {}


# COSMETIC OPTIONS

class RandomizeSuitColors(Toggle):
    """Randomize the colors of the suits. Is overriden if any of the color overrides are greater than 0. """
    display_name = "Randomize Suit Colors"
    default = False

class ShowSuitIndexOnPauseMenu(DefaultOnToggle):
    """If enabled, the selected suit color index will be shown on the pause menu under "Suits". This has unexpected behavior on non US versions """
    display_name = "Show Suit Index on Pause Menu (Disable if using non US version)"
    default = True

class PowerSuitColorOverride(Range):
    """Override the color of the Power Suit using an index from the game's color wheel"""
    display_name = "Power Suit Color Override"
    range_start = 0
    range_end = 359
    default = 0


class VariaSuitColorOverride(Range):
    """Override the color of the Varia Suit using an index from the game's color wheel"""
    display_name = "Varia Suit Color Override"
    range_start = 0
    range_end = 359
    default = 0


class GravitySuitColorOverride(Range):
    """Override the color of the Gravity Suit using an index from the game's color wheel"""
    display_name = "Gravity Suit Color Override"
    range_start = 0
    range_end = 359
    default = 0


class PhazonSuitColorOverride(Range):
    """Override the color of the Phazon Suit using an index from the game's color wheel"""
    display_name = "Phazon Suit Color Override"
    range_start = 0
    range_end = 359
    default = 0


class HudColorOption(Choice):
    """Determines the color of the HUD in the game. Will be overriden if any of the color overrides are greater than 0."""
    display_name = "HUD Color"
    default = "Default"
    option_default = "Default"
    option_red = "Red"
    option_green = "Green"
    option_blue = "Blue"
    option_violet = "Violet"
    option_yellow = "Yellow"
    option_cyan = "Cyan"
    option_white = "White"
    option_orange = "Orange"
    option_pink = "Pink"
    option_lime = "Lime"
    option_teal = "Teal"
    option_purple = "Purple"


class HudColorOverrideRed(Range):
    """0 to 255, sets the Red channel of the HUD color"""
    display_name = "HUD Color Red"
    range_start = 0
    range_end = 255
    default = 0


class HudColorOverrideGreen(Range):
    """0 to 255, sets the Green channel of the HUD color"""
    display_name = "HUD Color Green"
    range_start = 0
    range_end = 255
    default = 0


class HudColorOverrideBlue(Range):
    """0 to 255, sets the Blue channel of the HUD color"""
    display_name = "HUD Color Blue"
    range_start = 0
    range_end = 255
    default = 0


@dataclass
class MetroidPrimeOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    spring_ball: SpringBall
    required_artifacts: RequiredArtifacts
    exclude_items: ExcludeItems
    final_bosses: FinalBosses
    artifact_hints: ArtifactHints
    missile_launcher: MissileLauncher
    main_power_bomb: MainPowerBomb
    shuffle_scan_visor: ShuffleScanVisor
    non_varia_heat_damage: NonVariaHeatDamage
    staggered_suit_damage: StaggeredSuitDamage
    elevator_randomization: ElevatorRandomization
    elevator_mapping: ElevatorMapping
    starting_room: StartingRoom
    starting_room_name: StartingRoomName
    disable_starting_room_bk_prevention: DisableStartingRoomBKPrevention
    combat_logic_difficulty: CombatLogicDifficultyOption
    trick_difficulty: TrickDifficulty
    trick_allow_list: TrickAllowList
    trick_deny_list: TrickDenyList
    flaahgra_power_bombs: FlaahgraPowerBombs
    backwards_lower_mines: BackwardsLowerMines
    remove_xray_requirements: RemoveXrayRequirements
    remove_thermal_requirements: RemoveThermalRequirements
    remove_hive_mecha: RemoveHiveMecha

    # Cosmetic options
    fusion_suit: FusionSuit
    hud_color: HudColorOption
    hud_color_red: HudColorOverrideRed
    hud_color_green: HudColorOverrideGreen
    hud_color_blue: HudColorOverrideBlue
    randomize_suit_colors: RandomizeSuitColors
    show_suit_index_on_pause_menu: ShowSuitIndexOnPauseMenu
    power_suit_color: PowerSuitColorOverride
    varia_suit_color: VariaSuitColorOverride
    gravity_suit_color: GravitySuitColorOverride
    phazon_suit_color: PhazonSuitColorOverride

    death_link: DeathLink
