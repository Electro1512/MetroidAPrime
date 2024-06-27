from enum import Enum
import os
import random
from typing import TYPE_CHECKING, Dict, Any, List, Optional

from worlds.metroidprime.Items import SuitUpgrade


from .PrimeOptions import HudColor, MetroidPrimeOptions
from .data.RoomData import MetroidPrimeArea
from .data.Transports import get_transport_data
from .data.MagmoorCaverns import MagmoorCavernsAreaData
from .data.PhazonMines import PhazonMinesAreaData
from .data.PhendranaDrifts import PhendranaDriftsAreaData
from .data.TallonOverworld import TallonOverworldAreaData
from .data.ChozoRuins import ChozoRuinsAreaData


if TYPE_CHECKING:
    from worlds.metroidprime import MetroidPrimeWorld


def starting_inventory(world: 'MetroidPrimeWorld', item: str) -> bool:
    items = [item.name for item in world.multiworld.precollected_items[world.player]]
    if item in items:
        return True
    else:
        return False


def spring_check(spring) -> bool:
    if spring == 1:
        return True
    else:
        return False


def ridley(boss) -> bool:
    if boss == 0 or boss == 1:
        return False
    else:
        return True


def get_starting_beam(world: 'MetroidPrimeWorld') -> str:
    starting_items = [item.name for item in world.multiworld.precollected_items[world.player]]
    starting_beam = "Power"
    for item in starting_items:
        if item in [SuitUpgrade.Wave_Beam.value, SuitUpgrade.Ice_Beam.value, SuitUpgrade.Plasma_Beam.value]:
            starting_beam = item.split(" ")[0]
            break
    return starting_beam


def color_options_to_value(world: 'MetroidPrimeWorld') -> List[float]:
    options = world.options
    # If any overrides are set, use that instead
    if options.hud_color_red.value or options.hud_color_green.value or options.hud_color_blue.value:
        return [options.hud_color_red.value/255, options.hud_color_green.value/255, options.hud_color_blue.value/255]

    # get the key in hudcolor enum that matches all caps color
    color: str = world.options.hud_color.value
    color = color.upper()
    for key in HudColor.__members__.keys():
        if key == color:
            return HudColor[key].value
    return HudColor.DEFAULT.value


def make_artifact_hints(world: 'MetroidPrimeWorld') -> str:
    def make_artifact_hint(item) -> str:
        try:
            if world.options.artifact_hints.value:
                location = world.multiworld.find_item(item, world.player)
                player_string = f"{world.multiworld.player_name[location.player]}'s" if location.player != world.player else "your"
                return f"The &push;&main-color=#c300ff;{item}&pop; can be found in &push;&main-color=#d4cc33;{player_string}&pop; &push;&main-color=#89a1ff;{location.name}&pop;."
            else:
                return f"The &push;&main-color=#c300ff;{item}&pop; has not been collected."
            # This will error when trying to find an artifact that does not have a location since was pre collected
        except:
            return f"The &push;&main-color=#c300ff;{item}&pop; does not need to be collected."

    return {
        "Artifact of Chozo": make_artifact_hint("Artifact of Chozo"),
        "Artifact of Nature": make_artifact_hint("Artifact of Nature"),
        "Artifact of Sun": make_artifact_hint("Artifact of Sun"),
        "Artifact of World": make_artifact_hint("Artifact of World"),
        "Artifact of Spirit": make_artifact_hint("Artifact of Spirit"),
        "Artifact of Newborn": make_artifact_hint("Artifact of Newborn"),
        "Artifact of Truth": make_artifact_hint("Artifact of Truth"),
        "Artifact of Strength": make_artifact_hint("Artifact of Strength"),
        "Artifact of Elder": make_artifact_hint("Artifact of Elder"),
        "Artifact of Wild": make_artifact_hint("Artifact of Wild"),
        "Artifact of Lifegiver": make_artifact_hint("Artifact of Lifegiver"),
        "Artifact of Warrior": make_artifact_hint("Artifact of Warrior")
    }


def get_tweaks(world: 'MetroidPrimeWorld') -> Dict[str, Any]:
    color = color_options_to_value(world)
    if color != HudColor.DEFAULT.value:
        return {
            "hudColor": color
        }
    else:
        return {}


def make_config(world: 'MetroidPrimeWorld'):
    options: MetroidPrimeOptions = world.options
    config = {
        "$schema": "https://randovania.org/randomprime/randomprime.schema.json",
        "inputIso": "prime.iso",
        "outputIso": "prime_out.iso",
        "forceVanillaLayout": False,
        "preferences": {
            "forceFusion": bool(options.fusion_suit.value),
            "cacheDir": "cache",
            "qolGeneral": True,
            "qolGameBreaking": True,
            "qolCosmetic": True,
            "qolCutscenes": "Skippable",
            "qolPickupScans": True,
            "mapDefaultState": "Always",
            "artifactHintBehavior": "All",
            "skipSplashScreens": bool(os.environ.get("DEBUG", False)),
            "quickplay": bool(os.environ.get("DEBUG", False)),
            "quickpatch": bool(os.environ.get("DEBUG", False)),
            "quiet": bool(os.environ.get("DEBUG", False)),
            "suitColors": {
                "gravityDeg": world.options.gravity_suit_color.value or 0,
                "phazonDeg": world.options.phazon_suit_color.value or 0,
                "powerDeg": world.options.power_suit_color.value or 0,
                "variaDeg": world.options.varia_suit_color.value or 0
            }
        },
        "tweaks": get_tweaks(world),
        "gameConfig": {
            "mainMenuMessage": "Archipelago Metroid Prime",
            "startingRoom": f"{world.starting_room_data.area.value}:{world.starting_room_data.name}",
            "springBall": spring_check(options.spring_ball.value),
            "warpToStart": True,
            "multiworldDolPatches": True,
            "nonvariaHeatDamage": bool(options.non_varia_heat_damage.value),
            "staggeredSuitDamage": options.staggered_suit_damage.value,
            "heatDamagePerSec": 10.0,
            "poisonDamagePerSec": 0.11,
            "phazonDamagePerSec": 0.964,
            "phazonDamageModifier": "Default",
            "autoEnabledElevators": True,
            "skipRidley": ridley(options.final_bosses.value),
            "removeHiveMecha": bool(options.remove_hive_mecha.value),
            "multiworldDolPatches": False,
            "startingItems": {
                "combatVisor": True,  # starting_inventory(world, "Combat Visor"),
                "powerBeam": starting_inventory(world, "Power Beam"),
                "scanVisor": True,  # starting_inventory(world, "Scan Visor"),
                # These are handled by the client
                "missiles": 0,
                "energyTanks": 0,
                "powerBombs": 0,
                "wave": starting_inventory(world, "Wave Beam"),
                "ice": starting_inventory(world, "Ice Beam"),
                "plasma": starting_inventory(world, "Plasma Beam"),
                "charge": starting_inventory(world, "Charge Beam"),
                "morphBall": starting_inventory(world, "Morph Ball"),
                "bombs": starting_inventory(world, "Morph Ball Bomb"),
                "spiderBall": starting_inventory(world, "Spider Ball"),
                "boostBall": starting_inventory(world, "Boost Ball"),
                "variaSuit": starting_inventory(world, "Varia Suit"),
                "gravitySuit": starting_inventory(world, "Gravity Suit"),
                "phazonSuit": starting_inventory(world, "Phazon Suit"),
                "thermalVisor": starting_inventory(world, "Thermal Visor"),
                "xray": starting_inventory(world, "X-Ray Visor"),
                "spaceJump": starting_inventory(world, "Space Jump Boots"),
                "grapple": starting_inventory(world, "Grapple Beam"),
                "superMissile": starting_inventory(world, "Super Missile"),
                "wavebuster": starting_inventory(world, "Wavebuster"),
                "iceSpreader": starting_inventory(world, "Ice Spreader"),
                "flamethrower": starting_inventory(world, "Flamethrower")
            },
            "disableItemLoss": True,
            "startingVisor": "Combat",
            "startingBeam": get_starting_beam(world),
            "enableIceTraps": False,
            "missileStationPbRefill": True,
            "doorOpenMode": "Original",
            "etankCapacity": 100,
            "itemMaxCapacity": {
                "Power Beam": 1,
                "Ice Beam": 1,
                "Wave Beam": 1,
                "Plasma Beam": 1,
                "Missile": 999,
                "Scan Visor": 1,
                "Morph Ball Bomb": 1,
                "Power Bomb": 99,
                "Flamethrower": 1,
                "Thermal Visor": 1,
                "Charge Beam": 1,
                "Super Missile": 1,
                "Grapple Beam": 1,
                "X-Ray Visor": 1,
                "Ice Spreader": 1,
                "Space Jump Boots": 1,
                "Morph Ball": 1,
                "Combat Visor": 1,
                "Boost Ball": 1,
                "Spider Ball": 1,
                "Power Suit": 1,
                "Gravity Suit": 1,
                "Varia Suit": 1,
                "Phazon Suit": 1,
                "Energy Tank": 99,
                "Unknown Item 1": 6000,
                "Health Refill": 999,
                "Unknown Item 2": 1,
                "Wavebuster": 1,
                "Artifact Of Truth": 1,
                "Artifact Of Strength": 1,
                "Artifact Of Elder": 1,
                "Artifact Of Wild": 1,
                "Artifact Of Lifegiver": 1,
                "Artifact Of Warrior": 1,
                "Artifact Of Chozo": 1,
                "Artifact Of Nature": 1,
                "Artifact Of Sun": 1,
                "Artifact Of World": 1,
                "Artifact Of Spirit": 1,
                "Artifact Of Newborn": 1
            },
            "phazonEliteWithoutDynamo": True,
            "mainPlazaDoor": True,
            "backwardsLabs": True,
            "backwardsFrigate": True,
            "backwardsUpperMines": True,
            "backwardsLowerMines": bool(world.options.backwards_lower_mines.value),
            "patchPowerConduits": False,
            "removeMineSecurityStationLocks": False,
            "powerBombArboretumSandstone": True,
            "artifactHints": make_artifact_hints(world),
            "requiredArtifactCount": world.options.required_artifacts.value
        },
        "levelData": make_level_data(world)
    }

    return config


def make_level_data(world):
    level_data = {
        MetroidPrimeArea.Tallon_Overworld.value:  {
            "transports": get_transport_data(world, MetroidPrimeArea.Tallon_Overworld),
            "rooms":  TallonOverworldAreaData().get_config_data(world)
        },
        MetroidPrimeArea.Chozo_Ruins.value: {
            "transports": get_transport_data(world, MetroidPrimeArea.Chozo_Ruins),
            "rooms":  ChozoRuinsAreaData().get_config_data(world)
        },
        MetroidPrimeArea.Magmoor_Caverns.value: {
            "transports": get_transport_data(world, MetroidPrimeArea.Magmoor_Caverns),
            "rooms":  MagmoorCavernsAreaData().get_config_data(world)
        },
        MetroidPrimeArea.Phendrana_Drifts.value: {
            "transports": get_transport_data(world, MetroidPrimeArea.Phendrana_Drifts),
            "rooms":  PhendranaDriftsAreaData().get_config_data(world)
        },
        MetroidPrimeArea.Phazon_Mines.value: {
            "transports": get_transport_data(world, MetroidPrimeArea.Phazon_Mines),
            "rooms":  PhazonMinesAreaData().get_config_data(world)

        }
    }

    return level_data
