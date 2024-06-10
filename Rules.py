from worlds.generic.Rules import add_rule
from .Logic import MetroidPrimeLogic as logic
from BaseClasses import MultiWorld


def set_rules(multiworld: MultiWorld, player, locations):
    access_rules = {
      # Chzo Ruins Locations
      # Handled by region creation

        # tallon overworld locations
        # Handled with region creation
        # phazon mines locations
        'Phazon Mines: Main Quarry': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                    logic.prime_can_bomb(state, multiworld, player) and
                                                    logic.prime_can_spider(state, multiworld, player) and
                                                    state.has('Thermal Visor', player)),
        'Phazon Mines: Security Access A': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                          logic.prime_can_pb(state, multiworld, player)),
        'Phazon Mines: Storage Depot B': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                        logic.prime_can_bomb(state, multiworld, player) and
                                                        logic.prime_can_pb(state, multiworld, player) and
                                                        logic.prime_can_spider(state, multiworld, player) and
                                                        state.has('Grapple Beam', player)),
        'Phazon Mines: Storage Depot A': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                        logic.prime_can_pb(state, multiworld, player) and
                                                        state.has('Plasma Beam', player)),
        'Phazon Mines: Elite Research - Phazon Elite': lambda state: (
            logic.prime_upper_mines(state, multiworld, player) and
            logic.prime_can_pb(state, multiworld, player)),
        'Phazon Mines: Elite Research - Laser': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                               logic.prime_can_bomb(state, multiworld, player) and
                                                               logic.prime_can_boost(state, multiworld, player)),
        'Phazon Mines: Elite Control Access': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                             logic.prime_can_bomb(state, multiworld, player) and
                                                             logic.prime_can_pb(state, multiworld, player) and
                                                             logic.prime_can_spider(state, multiworld, player)),
        'Phazon Mines: Ventilation Shaft': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                          logic.prime_can_bomb(state, multiworld, player) and
                                                          logic.prime_can_pb(state, multiworld, player) and
                                                          logic.prime_can_spider(state, multiworld, player) and
                                                          logic.prime_can_boost(state, multiworld, player)),
        'Phazon Mines: Phazon Processing Center': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                                 logic.prime_can_bomb(state, multiworld, player) and
                                                                 logic.prime_can_pb(state, multiworld, player) and
                                                                 logic.prime_can_spider(state, multiworld, player) and
                                                                 state.has('Grapple Beam', player)),
        'Phazon Mines: Processing Center Access': lambda state: (logic.prime_lower_mines(state, multiworld, player) and
                                                                 state.has('X-Ray Visor', player)),
        'Phazon Mines: Elite Quarters': lambda state: (logic.prime_lower_mines(state, multiworld, player) and
                                                       state.has('X-Ray Visor', player) and
                                                       state.count('Energy Tank', player) >= 7),
        'Phazon Mines: Central Dynamo': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                       logic.prime_can_bomb(state, multiworld, player) and
                                                       logic.prime_can_pb(state, multiworld, player) and
                                                       logic.prime_can_spider(state, multiworld, player) and
                                                       state.has('X-Ray Visor', player)),
        'Phazon Mines: Metroid Quarantine B': lambda state: (logic.prime_lower_mines(state, multiworld, player) and
                                                             logic.prime_can_super(state, multiworld, player)),
        'Phazon Mines: Metroid Quarantine A': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                             logic.prime_can_bomb(state, multiworld, player) and
                                                             logic.prime_can_pb(state, multiworld, player) and
                                                             logic.prime_can_spider(state, multiworld, player) and
                                                             logic.prime_can_boost(state, multiworld, player) and
                                                             state.has('X-Ray Visor', player)),
        'Phazon Mines: Fungal Hall B': lambda state: (logic.prime_lower_mines(state, multiworld, player) and
                                                      state.has_any({'Thermal Visor', 'X-Ray Visor'}, player)),
        'Phazon Mines: Phazon Mining Tunnel': lambda state: (logic.prime_lower_mines(state, multiworld, player) and
                                                             state.has('Phazon Suit', player)),
        'Phazon Mines: Fungal Hall Access': lambda state: (logic.prime_upper_mines(state, multiworld, player) and
                                                           logic.prime_can_bomb(state, multiworld, player) and
                                                           logic.prime_can_pb(state, multiworld, player) and
                                                           logic.prime_can_boost(state, multiworld, player) and
                                                           state.has_all({'X-Ray Visor', 'Plasma Beam'},
                                                                         player)),

    }

    for i in locations:
        location = multiworld.get_location(i, player)
        try:
            add_rule(location, access_rules[i])
        except KeyError:
            continue
