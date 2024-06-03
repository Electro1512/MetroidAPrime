from typing import Dict, Any, Optional


from .PrimeOptions import MetroidPrimeOptions
from .data.RoomData import MetroidPrimeArea
from .data.Transports import get_transport_data
from .data.MagmoorCaverns import MagmoorCavernsAreaData
from .data.PhazonMines import PhazonMinesAreaData
from .data.PhendranaDrifts import PhendranaDriftsAreaData
from .data.TallonOverworld import TallonOverworldAreaData
from .data.ChozoRuins import ChozoRuinsAreaData


def starting_inventory(world, item) -> bool:
    items = world.multiworld.precollected_items.values()
    if item in items:
        return True
    else:
        return False


def starting_ammo(world, item) -> int:
    items = world.multiworld.precollected_items.values()
    count = 0
    if item == "Missile Expansion":
        for i in items:
            if i == "Missile Expansion" or i == "Missile Launcher":
                count += 5
        return count
    if item == "Energy Tank":
        for i in items:
            if i == "Energy Tank":
                count += 1
    if item == "Power Bomb (Main)":
        for i in items:
            if i == "Power Bomb (Main)" or i == "Power Bomb Expansion":
                count += 1
    return count


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


def make_artifact_hints(world) -> str:
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


def make_config(world):
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
            "artifactHintBehavior": "All"
        },
        "gameConfig": {
            "mainMenuMessage": "Archipelago Metroid Prime",
            "startingRoom": "Tallon Overworld:Landing Site",
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
                "powerBeam": True,  # starting_inventory(world, "Power Beam"), disabling this for now since we don't have this worked into logic
                "scanVisor": True,  # starting_inventory(world, "Scan Visor"),
                "missiles": starting_ammo(world, "Missile Launcher"),
                "energyTanks": starting_ammo(world, "Energy Tank"),
                "powerBombs": starting_ammo(world, "Power Bomb (Main)"),
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
            "startingBeam": "Power",
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
            "backwardsLowerMines": True,
            "patchPowerConduits": False,
            "removeMineSecurityStationLocks": False,
            "powerBombArboretumSandstone": False,
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
