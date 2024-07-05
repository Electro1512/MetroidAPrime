from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict

from BaseClasses import CollectionState
from ..Logic import can_bomb, can_boost, can_charge_beam, can_defeat_sheegoth, can_grapple, can_heat, can_ice_beam, can_infinite_speed, can_melt_ice, can_missile, can_morph_ball, can_move_underwater, can_plasma_beam, can_power_beam, can_power_bomb, can_scan, can_space_jump, can_spider, can_super_missile, can_thermal, can_wave_beam, can_xray, has_energy_tanks
from ..data.RoomNames import RoomName


class TrickDifficulty(Enum):
    No_Tricks = -1
    Easy = 0
    Medium = 1
    Hard = 2


class Trick_Type(Enum):
    L_Jump = "L Jump"
    L_Jump_Space_Jump = "L-Jump Space Jump"
    R_Jump = "R-Jump"
    R_Jump_Space_Jump = "R-Jump Space Jump"
    Scan_Dash = "Scan Dash"
    Scan_Dash_Space_Jump = "Scan Dash"
    Slope_Jump_With_Space_Jump = "Slope Jump With Space Jump"
    Slope_Jump = "Slope Jump No Space Jump"
    Combat_Dash = "Combat Dash"
    Combat_Dash_Space_Jump = "Combat Dash"
    Infinite_Speed = "Infinite Speed"
    Double_Bomb_Jump = "Double Bomb Jump"
    No_XRay = "No XRay"


@dataclass
class TrickInfo:
    name: str
    description: str
    difficulty: TrickDifficulty
    rule_func: Callable[[CollectionState, int], bool]


class Tricks:
  # Tallon
    alcove_escape: TrickInfo = TrickInfo("Alcove Escape", "Escape the Alcove without space jump", TrickDifficulty.Easy, lambda state, player: True)
    landing_site_scan_dash: TrickInfo = TrickInfo("Landing Site Scan Dash", "Perform a scan dash to reach the landing site without bombs", TrickDifficulty.Medium, can_scan)

    frigate_no_gravity: TrickInfo = TrickInfo("Frigate No Gravity", "Complete the Frigate without Gravity Suit", TrickDifficulty.Easy,
                                              lambda state, player: can_bomb(state, player) and can_space_jump(state, player) and can_wave_beam(state, player) and can_thermal(state, player))

    hydro_access_tunnel_no_gravity: TrickInfo = TrickInfo("Hydro Access Tunnel No Gravity", "Complete the Hydro Access Tunnel without Gravity Suit using Wall Boosting", TrickDifficulty.Hard,
                                                          lambda state, player: can_boost(state, player))

    frigate_backwards_no_gravity: TrickInfo = TrickInfo("Frigate No Gravity", "Complete the Frigate without Gravity Suit", TrickDifficulty.Easy,
                                                        lambda state, player: can_morph_ball(state, player) and can_space_jump(state, player) and can_boost(state, player))

    frigate_crash_site_scan_dash: TrickInfo = TrickInfo("Crashed Frigate Scan Dash", "Perform a scan dash to reach the item at Crashed Frigate", TrickDifficulty.Hard, can_scan)

    frigate_crash_site_slope_jump: TrickInfo = TrickInfo("Crashed Frigate Slope Jump", "Perform a slope jump to reach the item at Crashed Frigate", TrickDifficulty.Easy, can_space_jump)
    frigate_crash_site_slope_jump_no_sjb: TrickInfo = TrickInfo("Crashed Frigate Slope Jump", "Perform a slope jump to reach the item at Crashed Frigate", TrickDifficulty.Medium, lambda state, player: True)

    frigate_crash_site_climb_to_overgrown_cavern: TrickInfo = TrickInfo("Crashed Frigate Climb to Overgrown Cavern", "Climb to Overgrown Cavern", TrickDifficulty.Medium,
                                                                        lambda state, player: can_bomb(state, player) and can_space_jump(state, player))
    great_tree_hall_skip_bars: TrickInfo = TrickInfo("Great Tree Hall Skip Bars", "Skip the bars in Great Tree Hall using Morph Ball Bombs", TrickDifficulty.Hard, can_bomb)

    great_tree_chamber_no_xray: TrickInfo = TrickInfo("Great Tree Chamber No XRay", "Reach the Great Tree Chamber without XRay Visor", TrickDifficulty.Easy, can_space_jump)

    great_tree_hall_no_spider_ball: TrickInfo = TrickInfo("Great Tree Hall No Spider Ball", "Reach the door to the Life Grove Tunnel without Spider Ball", TrickDifficulty.Easy, can_space_jump)

    root_cave_arbor_chamber_no_grapple_xray: TrickInfo = TrickInfo("Root Cave Arbor Chamber No Grapple XRay", "Reach the Arbor Chamber without Grapple Beam or XRay Visor using a Combat Dash", TrickDifficulty.Hard, lambda state, player: can_space_jump(state, player) and can_scan(state, player))
  # Chozo
    vault_via_plaza: TrickInfo = TrickInfo("Vault Via Plaza", "Reach the Vault via the Main Plaza using an L Jump", TrickDifficulty.Easy, can_space_jump)
    plaza_half_pipe_no_boost: TrickInfo = TrickInfo("Plaza Half Pipe No Boost", "Reach the Half Pipe in the Main Plaza using a slope jump", TrickDifficulty.Easy, can_space_jump)
    plaza_grapple_ledge_r_jump: TrickInfo = TrickInfo("Plaza Grapple Ledge R Jump", "Reach the Grapple Ledge in the Main Plaza using an R Jump", TrickDifficulty.Easy, can_space_jump)

    ruined_shrine_upper_door_no_spider_ball: TrickInfo = TrickInfo("Ruined Shrine Upper Door L Jump", "Reach the upper door in the Ruined Shrine by L Jumping off the root", TrickDifficulty.Easy, can_space_jump)
    ruined_shrine_upper_door_scan_dash: TrickInfo = TrickInfo("Ruined Shrine Upper Door Scan Dash", "Reach the upper door in the Ruined Shrine by scan dashing without space jump", TrickDifficulty.Hard, can_scan)
    ruined_shrine_scan_dash_escape: TrickInfo = TrickInfo("Ruined Shrine Scan Dash Escape", "Escape the Ruined Shrine by scan dashing  off the branches", TrickDifficulty.Easy, can_scan)

    tower_of_light_climb_without_missiles: TrickInfo = TrickInfo("Tower of Light Climb Without Missiles", "Tower of Light can be climbed by dashing to the outside edges, skipping the 40 missile requirement.", TrickDifficulty.Easy, rule_func=lambda state, player: can_space_jump(state, player) and can_scan(state, player))
    tower_chamber_no_gravity: TrickInfo = TrickInfo("Tower Chamber No Gravity", "Reach the Tower Chamber without Gravity Suit by using a slope jump", TrickDifficulty.Easy, can_space_jump)
    tower_chamber_no_space_jump: TrickInfo = TrickInfo("Tower Chamber No Gravity", "Reach the Tower Chamber without Space Jump by using a double bomb jump", TrickDifficulty.Easy, rule_func=lambda state, player: can_bomb(state, player) and can_move_underwater(state, player))

    ruined_nursery_no_bombs: TrickInfo = TrickInfo("Ruined Nursery No Bombs", "Reach the Ruined Nursery Item by space jumping and morphing near the item", TrickDifficulty.Hard, lambda state, player: can_space_jump(state, player) and can_morph_ball(state, player))

    magma_pool_scan_dash: TrickInfo = TrickInfo("Cross Magma Pool Suitless", "Cross magma pool using a scan dash on the crate items", TrickDifficulty.Medium, lambda state, player: can_space_jump(state, player) and can_scan(state, player))
    magma_pool_debris_jump: TrickInfo = TrickInfo("Cross Magma Pool With SJB and Gravity", "Use the space jump boots to jump off debris to cross the pool", TrickDifficulty.Easy, lambda state, player: can_space_jump(state, player) and can_move_underwater(state, player) and has_energy_tanks(state, player, 2))
    magma_pool_item_debris_jump: TrickInfo = TrickInfo("Magma Pool Debris Jump", "Use the space jump boots to jump off debris to cross the pool", TrickDifficulty.Easy, lambda state, player: can_space_jump(state, player) and can_move_underwater(state, player) and has_energy_tanks(state, player, 2) and can_power_bomb(state, player))
    magma_pool_item_scan_dash: TrickInfo = TrickInfo("Magma Pool Item No Grapple", "Use the scan dash and a power bomb to get the item in the magma pool", TrickDifficulty.Medium, lambda state, player: can_space_jump(state, player) and can_scan(state, player) and can_power_bomb(state, player))
    magma_pool_item_infinite_speed: TrickInfo = TrickInfo("Magma Pool Item Infinite Speed", "Use infinite speed to get the item in the magma pool", TrickDifficulty.Medium, can_infinite_speed)

    arboretum_scan_gate_skip: TrickInfo = TrickInfo("Arboretum Scan Gate Skip", "Skip the gate in the Arboretum by double bomb jumping", TrickDifficulty.Easy, can_bomb)

    gathering_hall_without_space_jump: TrickInfo = TrickInfo("Gathering Hall Without Space Jump", "Double bomb jump from the side platform to the grate where the item is", TrickDifficulty.Easy, lambda state, player: can_bomb(state, player) and can_power_bomb(state, player))

    watery_hall_no_gravity: TrickInfo = TrickInfo("Watery Hall No Gravity", "Reach the Watery Hall Underwater Item without Gravity Suit by using a slope jump", TrickDifficulty.Easy, can_space_jump)
    watery_hall_no_gravity_no_space_jump: TrickInfo = TrickInfo("Watery Hall No Gravity No Space Jump", "Reach the Watery Hall Underwater Item without Gravity Suit by using a slope jump", TrickDifficulty.Medium, lambda state, player: can_move_underwater(state, player) == False or can_bomb(state, player))

    furnace_no_spider_ball = TrickInfo("Furnace No Spider Ball", "Reach the Item inside the Furnace without Spider Ball by jumping on the side of the spider track", TrickDifficulty.Easy, lambda state, player: can_bomb(state, player))
    furnace_spider_track_hbj = TrickInfo("Furnace Spider Track HBJ", "Reach the first track in furnace with a hyper bomb jump", TrickDifficulty.Medium, lambda state, player: can_bomb(state, player) and can_spider(state, player))
    furnace_spider_track_sj_bombs = TrickInfo("Furnace Spider Track SJ Bombs", "You can climb the Furnace and its spider tracks using Space Jump, reach the top of the room, then bomb jump across to the item.", TrickDifficulty.Medium, lambda state, player: can_bomb(state, player) and can_space_jump(state, player))

    crossway_item_fewer_reqs = TrickInfo("Crossway Item Fewer Reqs", "Reach the crossway item using only SJB and Morph Ball", TrickDifficulty.Easy, lambda state, player: can_bomb(state, player) and can_space_jump(state, player))
    crossway_hpbj = TrickInfo("Crossway Half pip bomb jump", "Reach the hall of the elders using a half pipe bomb jump", TrickDifficulty.Hard, lambda state, player: can_bomb(state, player))

    hall_of_elders_bomb_slots_no_spider = TrickInfo("Hall of Elders No Spider Ball", "Reach the bomb slots without the spider ball by jumping on a peg to activate the top bomb slot", TrickDifficulty.Easy, lambda state, player: can_space_jump(state, player) and can_bomb(state, player) and can_power_beam(state, player))
    hall_of_elders_reflecting_pool_no_spider = TrickInfo("Hall of Elders Reflecting Pool No Spider Ball", "Reach the reflecting pool without the spider ball", TrickDifficulty.Easy, lambda state, player: can_space_jump(state, player) and can_wave_beam(state, player) and can_bomb(state, player) and can_power_beam(state, player))
    hall_of_elders_reflecting_pool_no_wave_beam = TrickInfo("Hall of Elders Reflecting Pool No Wave Beam", "In Hall of the Elders, you can Hyper Bomb Jump (HBJ) to the morph ball track and reach the door to Reflecting Pool Access.", TrickDifficulty.Medium, lambda state, player: can_space_jump(state, player) and can_bomb(state, player) and can_power_beam(state, player))

    hall_of_elders_elder_chamber_no_spider = TrickInfo("Hall of Elders Elder Chamber No Spider Ball", "Reach the bomb slots without the spider ball by jumping on a peg to activate the top bomb slot", TrickDifficulty.Easy, lambda state, player: can_bomb(state, player) and can_plasma_beam(state, player) and can_space_jump(state, player) and can_power_beam(state, player))
    hall_of_elders_item_no_spider = TrickInfo("Hall of Elders Item No Spider Ball", "Reach the bomb slots without the spider ball by jumping on a peg to activate the top bomb slot", TrickDifficulty.Easy, lambda state, player: can_bomb(state, player) and can_ice_beam(state, player) and can_space_jump(state, player) and can_power_beam(state, player))

    reflecting_pool_space_jump_climb = TrickInfo("Reflecting Pool Space Jump Climb", "Climb the reflecting pool by space jumping off a stone toad", TrickDifficulty.Easy, can_space_jump)

  # Magmoor

    lava_lake_item_suitless = TrickInfo("Lava Lake Item Suitless", "Reach the Lava Lake item without the Varia Suit", TrickDifficulty.Medium, lambda state, player: can_missile(state, player) and can_space_jump(state, player) and has_energy_tanks(state, player, 4) and state.can_reach("Magmoor Caverns: " + RoomName.Lake_Tunnel.value, None, player))
    lava_lake_item_missiles_only = TrickInfo("Lava Lake Item Missiles Only", "Reach lava lake item without space jump by jumping on base of column", TrickDifficulty.Easy, lambda state, player: can_missile(state, player) and state.can_reach("Magmoor Caverns: " + RoomName.Lake_Tunnel.value, None, player))

    triclops_pit_item_no_sj = TrickInfo("Triclops Pit Item No SJ", "Reach the Triclops Pit item without Space Jump, assumes has xray and can use charge or missiles", TrickDifficulty.Medium, lambda state, player: can_xray(state, player) and (can_missile(state, player) or can_charge_beam(state, player)))
    triclops_pit_item_no_xray = TrickInfo("Triclops Pit Item No XRay", "Reach the Triclops Pit item without XRay Visor, assumes has space jump and can use charge or missiles", TrickDifficulty.Medium, lambda state, player: can_space_jump(state, player) and (can_missile(state, player) or can_charge_beam(state, player)))
    triclops_pit_item_no_sj_no_xray = TrickInfo("Triclops Pit Item No SJ No XRay", "Reach the Triclops Pit item without Space Jump or XRay Visor, assumes has charge or missiles", TrickDifficulty.Medium, lambda state, player: can_missile(state, player) or can_charge_beam(state, player))
    triclops_pit_item_no_missiles = TrickInfo("Triclops Pit Item No Missiles", "Reach the Triclops Pit item without Missiles, and instead use Charge Beam", TrickDifficulty.Easy, lambda state, player: can_space_jump(state, player) and can_xray(state, player) and can_charge_beam(state, player))

    warrior_shrine_no_boost = TrickInfo("Warrior Shrine No Boost", "Reach the Warrior by using an R Jump or Scan Dash", TrickDifficulty.Easy, can_space_jump)
    warrior_shrine_minimal_reqs = TrickInfo("Warrior Shrine Minimal Reqs", "Reach the Warrior Shrine without the Boost Ball or space jump", TrickDifficulty.Medium, can_scan)

    shore_tunnel_escape_no_sj = TrickInfo("Shore Tunnel Escape No SJ", "Escape the Shore Tunnel without Space Jump by using a slope jump or double bomb jump", TrickDifficulty.Medium, lambda state, player: can_power_bomb(state, player))

    fiery_shores_morphball_track_sj = TrickInfo("Fiery Shores Morphball Track SJ", "Reach the Morph Ball Track in Fiery Shores using the space jump boots", TrickDifficulty.Easy, can_space_jump)

    transport_tunnel_b_damage_boost = TrickInfo("Transport Tunnel B Damage Boost", "Cross the tunnel through the lava rather than using the morph ball track", TrickDifficulty.Easy, can_heat)

    twin_fires_tunnel_no_spider = TrickInfo("Twin Fires Tunnel No Spider Ball", "Traverse the Twin Fires Tunnel by using an R Jump and geometrey near the transport door", TrickDifficulty.Medium, lambda state, player: can_bomb(state, player) and can_space_jump(state, player))
    cross_twin_fires_suitless = TrickInfo("Cross Twin Fires Suitless", "Removes the suit requirement when crossing this room. Twin Fires Tunnel is the only room in late Magmoor that is superheated. This trick automatically assumes you have 2 Energy Tanks and can cross without Spider Ball, since it cannot be used while you are taking heat damage.", TrickDifficulty.Medium, lambda state, player: can_space_jump(state, player) and has_energy_tanks(state, player, 2))

    geothermal_core_no_grapple_spider = TrickInfo("Geothermal Core No Grapple Spider", "You can R jump or dash to reach the boost spinners, and either slope R jump or abuse standable collision to skip the spider track.", TrickDifficulty.Medium, lambda state, player: can_bomb(state, player) and can_boost(state, player) and can_space_jump(state, player))

    magmoor_workstation_no_thermal = TrickInfo("Magmoor Workstation No Thermal", "Reach the Magmoor Workstation Item without the Thermal Visor", TrickDifficulty.Easy, lambda state, player: can_scan(state, player) and can_wave_beam(state, player) and can_morph_ball(state, player))
  # Phendrana

    ice_temple_no_sj = TrickInfo("Ice Temple No SJ", "You can reach these locations by doing a hyper bomb jump in Phendrana Shorelines to reach the temple, and double bomb jumping to climb the temple itself", TrickDifficulty.Medium, rule_func=can_bomb)
    shorelines_spider_track_no_sj = TrickInfo("Shorelines Spider Track No SJ", "You can reach the item in the Phendrana Shorelines Spider Track without Space Jump by using a hyper bomb jump", TrickDifficulty.Medium, lambda state, player: can_bomb(state, player) and can_spider(state, player) and can_super_missile(state, player) and can_scan(state, player))

    ice_temple_item_no_sj = TrickInfo("Ice Temple Item No SJ", "Reach the Ice Temple item without Space Jump by double bomb jumps", TrickDifficulty.Medium, lambda state, player: can_bomb(state, player) and can_melt_ice(state, player))
    chapel_of_elders_escape_no_sj = TrickInfo("Chapel of Elders Escape No SJ", "Escape the Chapel of Elders without Space Jump by using a double bomb jump", TrickDifficulty.Medium, lambda state, player: can_defeat_sheegoth(state, player) and can_bomb(state, player) and can_wave_beam(state, player))

    phendrana_canyon_escape_no_items = TrickInfo("Phendrana Canyon Escape No Items", "You can leave Phendrana Canyon without any items by jumping on the crates. However, if you destroy the crates and don't have Boost Ball or Space Jump, you will softlock.", TrickDifficulty.Easy, lambda state, player: True)
    phendrana_courtyard_no_boost_spider = TrickInfo("Phendrana Courtyard No Boost Spider", "There is standable collision near the lower door that can be used to climb to the top of the room.", TrickDifficulty.Easy, lambda state, player: can_space_jump(state, player))

    control_tower_item_no_plasma = TrickInfo("Control Tower Item No Plasma", "Reach the Control Tower item without Plasma Beam by jumping off of crates in the middle and missiling the tower base", TrickDifficulty.Easy, lambda state, player: can_bomb(state, player) and can_missile(state, player) and can_space_jump(state, player))

    monitor_cave_no_grapple = TrickInfo("Monitor Cave No Grapple", "Reach the Monitor Station without the Grapple Beam by using a scan dash", TrickDifficulty.Medium, lambda state, player: can_spider(state, player) and can_space_jump(state, player) and can_scan(state, player))
    quarantine_to_north_courtyard_slope_jump = TrickInfo("Quarantine to North Courtyard Slope Jump", "You can exit Quarantine Cave to Ruined Courtyard by slope jumping next to the Spider Ball track.", TrickDifficulty.Medium, lambda state, player: can_space_jump(state, player))

    observatory_puzzle_skip = TrickInfo("Observatory Puzzle Skip", "This trick expects you to dash to climb Observatory without Boost Ball and Bombs, and then slope jump to the pipes to reach the item.", TrickDifficulty.Medium, lambda state, player: can_space_jump(state, player) and can_scan(state, player))
    frozen_pike_no_bombs = TrickInfo("Frozen Pike No Bombs", "To skip the morph ball bomb tunnel, you can R jump or dash to the upper platform on the opposite end of the tunnel.", TrickDifficulty.Easy, lambda state, player: can_space_jump(state, player))
    frozen_pike_no_gravity_suit = TrickInfo("Frozen Pike No Gravity Suit", "Reach hunter cave without gravity suit by doing a slope jump", TrickDifficulty.Medium, lambda state, player: can_space_jump(state, player))

    frost_cave_no_grapple = TrickInfo("Frost Cave No Grapple", "Reach the Frost Cave item without the Grapple Beam", TrickDifficulty.Easy, lambda state, player: can_missile(state, player) and can_space_jump(state, player) and can_move_underwater(state, player))  # Requires gravity

    phendranas_edge_storage_cavern_no_grapple = TrickInfo("Phendrana's Edge Storage Cavern No Grapple", "Reach the Phendrana's Edge storage cavern without the Grapple Beam", TrickDifficulty.Easy, lambda state, player: (can_thermal(state, player) or can_xray(state, player)) and can_power_bomb(state, player) and can_space_jump(state, player))
    phendranas_edge_security_cavern_no_grapple = TrickInfo("Phendrana's Edge Security Cavern No Grapple", "Reach the Phendrana's Edge security cavern without the Grapple Beam", TrickDifficulty.Easy, lambda state, player: can_grapple(state, player) and can_morph_ball(state, player) and can_space_jump(state, player))

    hunter_cave_no_grapple = TrickInfo("Hunter Cave No Grapple", "Reach the Hunter Cave upper levels without the grapple beam using an r jump", TrickDifficulty.Easy, lambda state, player: can_space_jump(state, player))

    gravity_chamber_no_grapple_plasma = TrickInfo("Gravity Chamber No Grapple Plasma", "You can R jump to reach the ledge without Grapple and Plasma Beam.", TrickDifficulty.Medium, lambda state, player: can_space_jump(state, player) and can_move_underwater(state, player))

  # Phazon Mines

    main_quarry_item_no_spider = TrickInfo("Main Quarry Item No Spider Ball", "You can slope jump onto the top of the crane and R jump over to the item.", TrickDifficulty.Medium, lambda state, player:  can_morph_ball(state, player) and can_bomb(state, player) and can_thermal(state, player) and can_wave_beam(state, player) and can_scan(state, player) and can_space_jump(state, player))
    main_quarry_to_waste_disposal_no_grapple = TrickInfo("Main Quarry to Waste Disposal No Grapple", "You can scan dash from the top of the structure (using the crane spider track scan point) to reach the door to Waste Disposal.", TrickDifficulty.Easy, lambda state, player: can_scan(state, player) and can_space_jump(state, player))

    ore_processing_to_storage_depot_b_no_spider = TrickInfo("Ore Processing Climb to Storage No Grapple Spider", "You can stand on various collision in the room, such as on the rotating column, to climb to the top of Ore Processing.", TrickDifficulty.Easy, lambda state, player: can_bomb(state, player) and can_power_bomb(state, player) and can_space_jump(state, player))
    ore_processing_climb_no_grapple_spider = TrickInfo("Ore Processing Climb No Grapple Spider", "You can stand on various collision in the room, such as on the rotating column, to climb to the top of Ore Processing.", TrickDifficulty.Easy, lambda state, player:  can_bomb(state, player) and can_power_bomb(state, player) and can_space_jump(state, player))

    mines_climb_shafts_no_spider = TrickInfo("Mines Climb Shafts No Spider Ball", "Elevator Access A and Research Access can be climbed without Spider Ball.", TrickDifficulty.Hard, lambda state, player: can_space_jump(state, player))
    elite_research_spinner_no_boost = TrickInfo("Elite Research laser No Boost", "You can get the laser turret to spin by wedging the morph ball in the spinner, bombing out, and then spinning the morph ball while in the laser before it locks you in.", TrickDifficulty.Easy, lambda state, player: can_bomb(state, player) and can_scan(state, player) and can_space_jump(state, player))
    ventilation_shaft_hpbj = TrickInfo("Ventilation Shaft HPBJ", "It's possible to return to Elite Control by performing a half pipe bomb jump to reach the Elite Control door.", TrickDifficulty.Hard, lambda state, player: can_bomb(state, player) and can_space_jump(state, player))

    metroid_quarantine_a_no_spider = TrickInfo("Metroid Quarantine A No Spider Ball", "Using R jumps, slope jumps, and dashes, you can traverse the entirety of lower Phazon Mines without Spider Ball and Grapple Beam.", TrickDifficulty.Medium, lambda state, player: can_scan(state, player) and can_xray(state, player) and can_space_jump(state, player))

    fungal_hall_access_no_phazon_suit = TrickInfo("Fungal Hall Access No Phazon Suit", "You can reach the Fungal Hall Access item without the Phazon Suit", TrickDifficulty.Easy, lambda state, player: can_morph_ball(state, player) and has_energy_tanks(state, player, 1))

    fungal_hall_a_no_grapple = TrickInfo("Fungal Hall A No Grapple", "Traverse Fungal Hall A with Slope Jumps and R Jumps", TrickDifficulty.Medium, can_space_jump)
    fungal_hall_b_no_grapple = TrickInfo("Fungal Hall B No Grapple", "Traverse Fungal Hall B with Slope Jumps and R Jumps", TrickDifficulty.Medium, can_space_jump)

    metroid_quarantine_b_no_spider_grapple = TrickInfo("Metroid Quarantine B No Spider Grapple", "You can reach the other side of the quarantine by using a slope jump and an r jump", TrickDifficulty.Medium, lambda state, player: lambda state, player: can_space_jump(state, player) and can_scan(state, player))

    phazon_processing_center_item_no_spider = TrickInfo("Phazon Processing Center Item No Spider Ball", "You can abuse standable collision such as the morph track and the scaffolding to access the top of the room without needing Spider Ball.", TrickDifficulty.Easy, lambda state, player: can_space_jump(state, player) and can_power_bomb(state, player))
    phazon_processing_center_no_phazon_suit = TrickInfo("Phazon Processing Center No Phazon Suit", "Reach the elite quarters by damage boosting through the phazon without the suit", TrickDifficulty.Easy, lambda state, player: True)
    climb_phazon_processing_center_no_spider = TrickInfo("Phazon Processing Center No Spider Ball", "You can abuse standable collision such as the morph track and the scaffolding to access the top of the room without needing Spider Ball.", TrickDifficulty.Easy, can_space_jump)
