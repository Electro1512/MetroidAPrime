import typing

from .RoomData import MetroidPrimeArea


if typing.TYPE_CHECKING:
    from .. import MetroidPrimeWorld


def temple_dest(boss) -> str:
    if boss == 0 or boss == 2:
        return "Crater Entry Point"
    else:
        return "Credits"


def get_transport_data(world: 'MetroidPrimeWorld', area: MetroidPrimeArea):
    data = {
        MetroidPrimeArea.Tallon_Overworld: {
            "Tallon Overworld North (Tallon Canyon)":  "Chozo Ruins West (Main Plaza)",
            "Tallon Overworld West (Root Cave)": "Magmoor Caverns East (Twin Fires)",
            "Tallon Overworld East (Frigate Crash Site)": "Chozo Ruins East (Reflecting Pool, Save Station)",
            "Tallon Overworld South (Great Tree Hall, Upper)": "Chozo Ruins South (Reflecting Pool, Far End)",
            "Tallon Overworld South (Great Tree Hall, Lower)": "Phazon Mines East (Main Quarry)",
            "Artifact Temple": temple_dest(world.options.final_bosses.value)
        },
        MetroidPrimeArea.Chozo_Ruins: {
            "Chozo Ruins West (Main Plaza)": "Tallon Overworld North (Tallon Canyon)",
            "Chozo Ruins North (Sun Tower)": "Magmoor Caverns North (Lava Lake)",
            "Chozo Ruins East (Reflecting Pool, Save Station)": "Tallon Overworld East (Frigate Crash Site)",
            "Chozo Ruins South (Reflecting Pool, Far End)": "Tallon Overworld South (Great Tree Hall, Upper)",
        },
        MetroidPrimeArea.Magmoor_Caverns: {
            "Magmoor Caverns North (Lava Lake)": "Chozo Ruins North (Sun Tower)",
            "Magmoor Caverns West (Monitor Station)": "Phendrana Drifts North (Phendrana Shorelines)",
            "Magmoor Caverns East (Twin Fires)": "Tallon Overworld West (Root Cave)",
            "Magmoor Caverns South (Magmoor Workstation, Save Station)": "Phendrana Drifts South (Quarantine Cave)",
            "Magmoor Caverns South (Magmoor Workstation, Debris)": "Phazon Mines West (Phazon Processing Center)",
        },
        MetroidPrimeArea.Phendrana_Drifts: {
            "Phendrana Drifts North (Phendrana Shorelines)": "Magmoor Caverns West (Monitor Station)",
            "Phendrana Drifts South (Quarantine Cave)": "Magmoor Caverns South (Magmoor Workstation, Save Station)",
        },
        MetroidPrimeArea.Phazon_Mines: {
            "Phazon Mines East (Main Quarry)": "Tallon Overworld South (Great Tree Hall, Lower)",
            "Phazon Mines West (Phazon Processing Center)": "Magmoor Caverns South (Magmoor Workstation, Debris)",
        },

    }

    return data[area]
