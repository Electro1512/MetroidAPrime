import typing

from worlds.metroidprime.data.RoomNames import RoomName
from worlds.metroidprime.data.TallonOverworld import TallonOverworldAreaData
from .Logic import MetroidPrimeLogic as logic
from BaseClasses import Region
from .Locations import tallon_location_table, magmoor_location_table, mines_location_table, chozo_location_table, \
    phen_location_table, MetroidPrimeLocation
if typing.TYPE_CHECKING:
    from . import MetroidPrimeWorld


def create_regions(world: 'MetroidPrimeWorld', final_boss_selection):
    # create all regions and populate with locations
    menu = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu)

    # tallon_overworld = Region("Tallon Overworld", self.player, self.multiworld)
    # tallon_overworld.add_locations(tallon_location_table, MetroidPrimeLocation)
    # self.multiworld.regions.append(tallon_overworld)

    TallonOverworldAreaData().create_world_region(world)

    chozo_ruins = Region("Chozo Ruins", world.player, world.multiworld)
    chozo_ruins.add_locations(chozo_location_table, MetroidPrimeLocation)
    world.multiworld.regions.append(chozo_ruins)

    magmoor_caverns = Region("Magmoor Caverns", world.player, world.multiworld)
    magmoor_caverns.add_locations(magmoor_location_table, MetroidPrimeLocation)
    world.multiworld.regions.append(magmoor_caverns)

    phendrana_drifts = Region("Phendrana Drifts", world.player, world.multiworld)
    phendrana_drifts.add_locations(phen_location_table, MetroidPrimeLocation)
    world.multiworld.regions.append(phendrana_drifts)

    phazon_mines = Region("Phazon Mines", world.player, world.multiworld)
    phazon_mines.add_locations(mines_location_table, MetroidPrimeLocation)
    world.multiworld.regions.append(phazon_mines)

    impact_crater = Region("Impact Crater", world.player, world.multiworld)
    world.multiworld.regions.append(impact_crater)

    mission_complete = Region("Mission Complete", world.player, world.multiworld)
    world.multiworld.regions.append(mission_complete)

    # entrances
    menu.connect(world.multiworld.get_region(RoomName.Landing_Site.value, world.player), "Landing Site")

# TODO: Nuke these 3
    world.multiworld.get_region(RoomName.Transport_to_Chozo_Ruins_West.value, world.player).connect(chozo_ruins, "West Chozo Elevator")
    world.multiworld.get_region(RoomName.Transport_to_Chozo_Ruins_East.value, world.player).connect(chozo_ruins, "East Chozo Elevator")
    world.multiworld.get_region(RoomName.Transport_to_Chozo_Ruins_South.value, world.player).connect(chozo_ruins, "South Chozo Elevator")

    world.multiworld.get_region(RoomName.Transport_to_Magmoor_Caverns_East.value, world.player).connect(magmoor_caverns, "East Magmoor Elevator", lambda state: (
        logic.prime_has_missiles(state, world.multiworld, world.player) and
        logic.prime_can_heat(state, world.multiworld, world.player)))
    world.multiworld.get_region(RoomName.Transport_to_Phazon_Mines_East.value, world.player).connect(phazon_mines, "East Mines Elevator", lambda state: (
        logic.prime_frigate(state, world.multiworld, world.player)))
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

    chozo_ruins.connect(magmoor_caverns, "North Magmoor Elevator", lambda state: (
        logic.prime_has_missiles(state, world.multiworld, world.player) and
        logic.prime_can_heat(state, world.multiworld, world.player) and
        state.has("Morph Ball", world.player)))

    magmoor_caverns.connect(phendrana_drifts, "Magmoor-Phendrana Elevators", lambda state: (
        logic.prime_front_phen(state, world.multiworld, world.player) or
        logic.prime_late_magmoor(state, world.multiworld, world.player)))
    magmoor_caverns.connect(phazon_mines, "West Mines Elevator", lambda state: (
        logic.prime_late_magmoor(state, world.multiworld, world.player) and state.has("Ice Beam", world.player)))

    if (final_boss_selection == 0 or
            final_boss_selection == 2):
        impact_crater.connect(mission_complete, "Mission Complete")

    from Utils import visualize_regions
    visualize_regions(world.multiworld.get_region("Menu", world.player), "my_world.puml")
