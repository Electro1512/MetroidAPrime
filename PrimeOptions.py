
from Options import DeathLink, DefaultOnToggle, Toggle, Range, ItemDict, StartInventoryPool, Choice, PerGameCommonOptions
from dataclasses import dataclass


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


class NonVariaHeatDamage(DefaultOnToggle):
    """If enabled, the gravity suit and phazon suit will not protect against heat damage which will change the required logic of the game"""
    display_name = "Non-Varia Heat Damage"
    default = True


class StaggeredSuitDamage(Choice):
    """Configure how suit damage reduction is calculated
    Default: based on the strongest suit you have
    Progressive: based on the number of suits you have
    Addititve: Individual suits provide their added damage reduction
    """
    display_name = "Staggered Suit Damage"
    option_default = "Default"
    option_progressive = "Progressive"
    option_additive = "Additive"
    default = "Progressive"

class RemoveHiveMecha(DefaultOnToggle):
    """If enabled, the trigger for the Hive Mecha boss will be removed from the game"""
    display_name = "Remove Hive Mecha"
    default = False

@dataclass
class MetroidPrimeOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    spring_ball: SpringBall
    required_artifacts: RequiredArtifacts
    exclude_items: ExcludeItems
    final_bosses: FinalBosses
    death_link: DeathLink
    artifact_hints: ArtifactHints
    non_varia_heat_damage: NonVariaHeatDamage
    staggered_suit_damage: StaggeredSuitDamage
    remove_hive_mecha: RemoveHiveMecha
