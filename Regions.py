import typing

from worlds.metroidprime.Logic import can_ice_beam, can_missile, can_plasma_beam, can_power_beam, can_super_missile, can_thermal, can_wave_beam, can_xray, has_energy_tanks, has_required_artifact_count
from worlds.metroidprime.data.ChozoRuins import ChozoRuinsAreaData
from worlds.metroidprime.data.MagmoorCaverns import MagmoorCavernsAreaData
from worlds.metroidprime.data.PhazonMines import PhazonMinesAreaData
from worlds.metroidprime.data.PhendranaDrifts import PhendranaDriftsAreaData
from worlds.metroidprime.data.RoomNames import RoomName
from worlds.metroidprime.data.TallonOverworld import TallonOverworldAreaData
from BaseClasses import Region
if typing.TYPE_CHECKING:
    from . import MetroidPrimeWorld


def create_regions(world: 'MetroidPrimeWorld', final_boss_selection):
    # create all regions and populate with locations
    menu = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu)

    TallonOverworldAreaData().create_world_region(world)
    ChozoRuinsAreaData().create_world_region(world)
    MagmoorCavernsAreaData().create_world_region(world)
    PhendranaDriftsAreaData().create_world_region(world)
    PhazonMinesAreaData().create_world_region(world)

    impact_crater = Region("Impact Crater", world.player, world.multiworld)
    world.multiworld.regions.append(impact_crater)

    mission_complete = Region("Mission Complete", world.player, world.multiworld)
    world.multiworld.regions.append(mission_complete)

    starting_room = world.multiworld.get_region(RoomName.Landing_Site.value, world.player)
    # entrances
    menu.connect(starting_room, "Landing Site")

    tallon_transport_to_chozo_west = world.multiworld.get_region(RoomName.Transport_to_Chozo_Ruins_West.value, world.player)
    tallon_transport_to_chozo_east = world.multiworld.get_region(RoomName.Transport_to_Chozo_Ruins_East.value, world.player)
    tallon_transport_to_chozo_south = world.multiworld.get_region(RoomName.Transport_to_Chozo_Ruins_South.value, world.player)
    tallon_transport_to_magmoor_east = world.multiworld.get_region(RoomName.Transport_to_Magmoor_Caverns_East.value, world.player)
    tallon_transport_to_phazon_east = world.multiworld.get_region(RoomName.Transport_to_Phazon_Mines_East.value, world.player)

    chozo_transport_to_tallon_north = world.multiworld.get_region(RoomName.Transport_to_Tallon_Overworld_North.value, world.player)
    chozo_transport_to_magmoor_north = world.multiworld.get_region(RoomName.Transport_to_Magmoor_Caverns_North.value, world.player)
    chozo_transport_to_tallon_east = world.multiworld.get_region(RoomName.Transport_to_Tallon_Overworld_East.value, world.player)
    chozo_transport_to_tallon_south = world.multiworld.get_region("Chozo Ruins: " + RoomName.Transport_to_Tallon_Overworld_South.value, world.player)

    magmoor_transport_to_chozo_north = world.multiworld.get_region(RoomName.Transport_to_Chozo_Ruins_North.value, world.player)
    magmoor_transport_to_phazon_west = world.multiworld.get_region(RoomName.Transport_to_Phazon_Mines_West.value, world.player)
    magmoor_transport_to_phendrana_north = world.multiworld.get_region(RoomName.Transport_to_Phendrana_Drifts_North.value, world.player)
    magmoor_transport_to_phendrana_south = world.multiworld.get_region(RoomName.Transport_to_Phendrana_Drifts_South.value, world.player)
    magmoor_transport_to_tallon_west = world.multiworld.get_region(RoomName.Transport_to_Tallon_Overworld_West.value, world.player)

    phazon_mines_transport_to_magmoor_south = world.multiworld.get_region("Phazon Mines: " + RoomName.Transport_to_Magmoor_Caverns_South.value, world.player)
    phazon_mines_transport_to_tallon_south = world.multiworld.get_region("Phazon Mines: " + RoomName.Transport_to_Tallon_Overworld_South.value, world.player)

    phendrana_transport_to_magmoor_west = world.multiworld.get_region(RoomName.Transport_to_Magmoor_Caverns_West.value, world.player)
    phendrana_transport_to_magmoor_south = world.multiworld.get_region("Phendrana Drifts: " + RoomName.Transport_to_Magmoor_Caverns_South.value, world.player)  # There are two transports to magmoor south, other is in phazon mines

    tallon_transport_to_chozo_west.connect(chozo_transport_to_tallon_north, "West Chozo Elevator")
    tallon_transport_to_chozo_east.connect(chozo_transport_to_tallon_east, "East Chozo Elevator")
    tallon_transport_to_chozo_south.connect(chozo_transport_to_tallon_south, "South Chozo Elevator")
    tallon_transport_to_magmoor_east.connect(magmoor_transport_to_tallon_west, "East Magmoor Elevator")
    tallon_transport_to_phazon_east.connect(phazon_mines_transport_to_tallon_south, "East Mines Elevator")

    chozo_transport_to_tallon_north.connect(tallon_transport_to_chozo_west, "North Tallon Elevator")
    chozo_transport_to_tallon_east.connect(tallon_transport_to_chozo_east, "East Tallon Elevator")
    chozo_transport_to_tallon_south.connect(tallon_transport_to_chozo_south, "South Tallon Elevator")

    magmoor_transport_to_chozo_north.connect(chozo_transport_to_magmoor_north, "North Chozo Elevator")
    magmoor_transport_to_phazon_west.connect(phazon_mines_transport_to_magmoor_south, "West Mines Elevator")
    magmoor_transport_to_phendrana_north.connect(phendrana_transport_to_magmoor_west, "North Phendrana Elevator")
    magmoor_transport_to_phendrana_south.connect(phendrana_transport_to_magmoor_south, "South Phendrana Elevator")
    magmoor_transport_to_tallon_west.connect(tallon_transport_to_magmoor_east, "West Tallon Elevator")

    phendrana_transport_to_magmoor_west.connect(magmoor_transport_to_phendrana_north, "West Magmoor Elevator")
    phendrana_transport_to_magmoor_south.connect(magmoor_transport_to_phendrana_south, "South Magmoor Elevator")

    artifact_temple = world.multiworld.get_region(RoomName.Artifact_Temple.value, world.player)

    if final_boss_selection == 0 or final_boss_selection == 2:
        world.multiworld.get_region(RoomName.Artifact_Temple.value, world.player).connect(impact_crater, "Crater Access", lambda state: (
            can_missile(state, world.player) and
            has_required_artifact_count(state, world.player) and
            has_energy_tanks(state, world.player, 8) and
            can_plasma_beam(state, world.player) and can_wave_beam(state, world.player) and can_ice_beam(state, world.player) and can_power_beam(state, world.player) and
            can_xray(state, world.player, True) and can_thermal(state, world.player, True)))
    elif final_boss_selection == 1:
        world.multiworld.get_region(RoomName.Artifact_Temple.value, world.player).connect(mission_complete, "Mission Complete", lambda state:
                                                                                          can_missile(state, world.player) and
                                                                                          has_required_artifact_count(state, world.player) and (can_plasma_beam(state, world.player) or can_super_missile(state, world.multiworld, world.player)) and
                                                                                          has_energy_tanks(state, world.player, 8))
    elif final_boss_selection == 3:
        world.multiworld.get_region(RoomName.Artifact_Temple.value, world.player).connect(mission_complete, "Mission Complete", lambda state: (
            can_missile(state, world.player) and
            has_required_artifact_count(state, world.player)))

    if (final_boss_selection == 0 or
            final_boss_selection == 2):
        impact_crater.connect(mission_complete, "Mission Complete")

    from Utils import visualize_regions
    visualize_regions(world.multiworld.get_region("Menu", world.player), "my_world.puml")
