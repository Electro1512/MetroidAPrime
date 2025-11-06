# Metroid Prime Archipelago

To get started or for troubleshooting, see **[the Setup Guide](./docs/setup_en.md)**!

An Archipelago implementation of Metroid Prime multiworld randomizer using [randomprime](https://github.com/randovania/randomprime/)

## Info
### What does randomization do to this game?

In Metroid Prime, all suit upgrade and expansion items are shuffled into the multiworld, giving the game a greater variety in routing to complete the end goal.

### What is the goal of Metroid Prime when randomized?

The end goal of the randomizer game can consist of:

- Collecting the required amount of Artifacts (amount is configurable)
- Defeating Ridley (configurable)
- Defeating Metroid Prime (configurable)

If randomized, the end goal can be scanned in the Temple Security station.

### Which items can be in another player's world?

All suit upgrades and expansion items can be shuffled in other players' worlds, excluding Power Suit and Combat Visor.

### What does another world's item look like in Metroid Prime?

Multiworld item pickups appear as one of the following:

- Progression Item: Cog
- Useful or Trap Item: Zoomer model with a random texture
- Filler Item: Metroid model with a random texture

### What versions of the Metroid Prime are supported?

Only the GameCube versions of the game are supported.  
The Wii and Switch version of the game are _not_ supported.  

### When the player receives an item, what happens?

The player will immediately have their suit inventory updated and receive a notification in the Client and a HUD message in-game.

### Can I teleport to the starting room?

To warp to the starting location,

1. Enter a Save Station
2. When prompted to Save, choose No
3. While choosing No, simultaenously hold down the L and R buttons.

### What happens to my own collected items at Game Over or if the game is reset without saving?
As long as the game is connected to the Client and the Client is connected to the server, items you collected before the Game Over or reset will be kept and returned to you when you re-enter the game, even if you did not save.  
(The item dot indicators on the map will still show the item location as not collected, even if the Client gives the items back to you.)

### Aside from item locations being shuffled, how does this differ from the vanilla game?

Some of the changes include:

- Layout Changes
  - The game skips the Space Pirate Frigate introduction sequence, automatically placing you into the Starting Room (default: Tallon Overworld - Landing Site)
  - Starting Room can optionally be randomized.
  - Elevator destinations can optionally be randomized.
  - In Main Plaza, Chozo Ruins, the upper ledge door to Vault is no longer locked.
  - Traversing "backwards" through the Pirate Labs in Phendrana is now possible:
    In Research Lab Hydra, the switch to disable the force field can be scanned from behind the force field.
  - Traversing "backwards" through the Crashed Frigate is now possble:
    In Main Ventilation Shaft Section B, the door will be powered up and openable when approached from behind.
  - Traversing "backwards" through Upper Phazon Mines can be possible (configurable):
    In Main Quarry, the barrier is automatically disabled when entering from Mine Security Station.
  - In Elite Research, Phazon Mines, the fight with Phazon Elite can now be started without needing to collect the item in Central Dynamo.
- QOL Changes:
  - Spring Ball has been implemented! When Morph Ball Bomb is acquired, Spring Ball can be used. To use Spring Ball, tilt the C-Stick Up.
