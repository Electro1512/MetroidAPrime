import typing

from worlds.metroidprime.data.ChozoRuins import ChozoRuinsAreaData
from worlds.metroidprime.data.MagmoorCaverns import MagmoorCavernsAreaData
from worlds.metroidprime.data.PhendranaDrifts import PhendranaDriftsAreaData
from worlds.metroidprime.data.RoomNames import RoomName
from worlds.metroidprime.data.TallonOverworld import TallonOverworldAreaData
from .Logic import MetroidPrimeLogic as logic
from BaseClasses import LocationProgressType, Region
from .Locations import tallon_location_table, magmoor_location_table, mines_location_table, chozo_location_table, \
    phen_location_table, MetroidPrimeLocation
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

    phazon_mines = Region("Phazon Mines", world.player, world.multiworld)
    phazon_mines.add_locations(mines_location_table, MetroidPrimeLocation)
    world.multiworld.regions.append(phazon_mines)

    impact_crater = Region("Impact Crater", world.player, world.multiworld)
    world.multiworld.regions.append(impact_crater)

    mission_complete = Region("Mission Complete", world.player, world.multiworld)
    world.multiworld.regions.append(mission_complete)

    landing_site = world.multiworld.get_region(RoomName.Landing_Site.value, world.player)
    # entrances
    menu.connect(landing_site, "Landing Site")

    tallon_transport_to_chozo_west = world.multiworld.get_region(RoomName.Transport_to_Chozo_Ruins_West.value, world.player)
    tallon_transport_to_chozo_east = world.multiworld.get_region(RoomName.Transport_to_Chozo_Ruins_East.value, world.player)
    tallon_transport_to_chozo_south = world.multiworld.get_region(RoomName.Transport_to_Chozo_Ruins_South.value, world.player)
    tallon_transport_to_magmoor_east = world.multiworld.get_region(RoomName.Transport_to_Magmoor_Caverns_East.value, world.player)
    tallon_transport_to_phazon_east = world.multiworld.get_region(RoomName.Transport_to_Phazon_Mines_East.value, world.player)

    chozo_transport_to_tallon_north = world.multiworld.get_region(RoomName.Transport_to_Tallon_Overworld_North.value, world.player)
    chozo_transport_to_magmoor_north = world.multiworld.get_region(RoomName.Transport_to_Magmoor_Caverns_North.value, world.player)
    chozo_transport_to_tallon_east = world.multiworld.get_region(RoomName.Transport_to_Tallon_Overworld_East.value, world.player)
    chozo_transport_to_tallon_south = world.multiworld.get_region(RoomName.Transport_to_Tallon_Overworld_South.value, world.player)

    magmoor_transport_to_chozo_north = world.multiworld.get_region(RoomName.Transport_to_Chozo_Ruins_North.value, world.player)
    magmoor_transport_to_phazon_west = world.multiworld.get_region(RoomName.Transport_to_Phazon_Mines_West.value, world.player)
    magmoor_transport_to_phendrana_north = world.multiworld.get_region(RoomName.Transport_to_Phendrana_Drifts_North.value, world.player)
    magmoor_transport_to_phendrana_south = world.multiworld.get_region(RoomName.Transport_to_Phendrana_Drifts_South.value, world.player)
    magmoor_transport_to_tallon_west = world.multiworld.get_region(RoomName.Transport_to_Tallon_Overworld_West.value, world.player)

    phendrana_transport_to_magmoor_west = world.multiworld.get_region(RoomName.Transport_to_Magmoor_Caverns_West.value, world.player)
    phendrana_transport_to_magmoor_south = world.multiworld.get_region("Phendrana Drifts: " + RoomName.Transport_to_Magmoor_Caverns_South.value, world.player)  # There are two transports to magmoor south, other is in phazon mines

    tallon_transport_to_chozo_west.connect(chozo_transport_to_tallon_north, "West Chozo Elevator")
    tallon_transport_to_chozo_east.connect(chozo_transport_to_tallon_east, "East Chozo Elevator")
    tallon_transport_to_chozo_south.connect(chozo_transport_to_tallon_south, "South Chozo Elevator")
    tallon_transport_to_magmoor_east.connect(magmoor_transport_to_tallon_west, "East Magmoor Elevator")
    tallon_transport_to_phazon_east.connect(phazon_mines, "East Mines Elevator")

    chozo_transport_to_tallon_north.connect(tallon_transport_to_chozo_west, "North Tallon Elevator")
    chozo_transport_to_tallon_east.connect(tallon_transport_to_chozo_east, "East Tallon Elevator")
    chozo_transport_to_tallon_south.connect(tallon_transport_to_chozo_south, "South Tallon Elevator")

    magmoor_transport_to_chozo_north.connect(chozo_transport_to_magmoor_north, "North Chozo Elevator")
    magmoor_transport_to_phazon_west.connect(phazon_mines, "West Mines Elevator")
    magmoor_transport_to_phendrana_north.connect(phendrana_transport_to_magmoor_west, "North Phendrana Elevator")
    magmoor_transport_to_phendrana_south.connect(phendrana_transport_to_magmoor_south, "South Phendrana Elevator")
    magmoor_transport_to_tallon_west.connect(tallon_transport_to_magmoor_east, "West Tallon Elevator")

    phendrana_transport_to_magmoor_west.connect(magmoor_transport_to_phendrana_north, "West Magmoor Elevator")
    phendrana_transport_to_magmoor_south.connect(magmoor_transport_to_phendrana_south, "South Magmoor Elevator")

    if final_boss_selection == 0 or final_boss_selection == 2:
        world.multiworld.get_region(RoomName.Artifact_Temple.value, world.player).connect(impact_crater, "Crater Access", lambda state: (
            logic.prime_has_missiles(state, world.multiworld, world.player) and
            logic.prime_artifact_count(state, world.multiworld, world.player) and
            state.count('Energy Tank', world.player) >= 8 and
            state.has_all({"Wave Beam", "Ice Beam", "Plasma Beam", "Thermal Visor", "X-Ray Visor", "Phazon Suit",
                           "Space Jump Boots"}, world.player)))
    elif final_boss_selection == 1:
        world.multiworld.get_region(RoomName.Artifact_Temple.value, world.player).connect(mission_complete, "Mission Complete", lambda state: (
            logic.prime_has_missiles(state, world.multiworld, world.player) and
            logic.prime_artifact_count(state, world.multiworld, world.player) and
            (state.has("Plasma Beam", world.player) or logic.prime_can_super(state, world.multiworld,
                                                                             world.player)) and
            logic.prime_etank_count(state, world.multiworld, world.player) >= 8))
    elif final_boss_selection == 3:
        world.multiworld.get_region(RoomName.Artifact_Temple.value, world.player).connect(mission_complete, "Mission Complete", lambda state: (
            logic.prime_has_missiles(state, world.multiworld, world.player) and
            logic.prime_artifact_count(state, world.multiworld, world.player)))

    if (final_boss_selection == 0 or
            final_boss_selection == 2):
        impact_crater.connect(mission_complete, "Mission Complete")

    from Utils import visualize_regions
    visualize_regions(world.multiworld.get_region("Menu", world.player), "my_world.puml")
