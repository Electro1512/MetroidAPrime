# Metroid Prime Archipelago
An Archipelago implementation of Metroid Prime multiworld randomizer using [randomprime](https://github.com/randovania/randomprime/)


## Setup Guide
To get started or for troubleshooting, see [the Setup Guide](./docs/setup_en.md).


## What does randomization do to this game?
In Metroid Prime, all suit upgrade and expansion items are shuffled into the multiworld, giving the game a greater variety in routing to complete the end goal.


## What is the goal of Metroid Prime when randomized?
The end goal of the randomizer game can consist of:
- Collecting the required amount of Artifacts (amount is configurable)
- Defeating Ridley (configurable)
- Defeating Metroid Prime (configurable)


## Which items can be in another player's world?
All suit upgrades and expansion items can be shuffled in other players' worlds, excluding Power Suit and Combat Visor.


## What does another world's item look like in Metroid Prime?
Multiworld items appear as a Metroid model with a glitched texture.


## What versions of the Metroid Prime are supported?
Only the GameCube versions of the game are supported. 
  * US `DOL-GM8E-0-00 USA` version recommended  
    Other GameCube regions/versions will also work!  
The Wii and Switch version of the game are *not* supported.  


## When the player receives an item, what happens?
The player will immediately have their suit inventory updated and receive a notification in the Client and a HUD message in-game.


## FAQs
### What happens if I pickup an item without having the client running?
In order for Metroid Prime Archipelago to function correctly, the Client should always be running whenever you are playing through your game.  
Due to the way location checks are handled, the client will not be aware of any item you have picked up when it is not running except the one you most recently picked up.


### Can I teleport to the starting room?
To warp to the starting location,
1. Enter a Save Station  
2. When prompted to Save, choose No  
3. While choosing No, simultaenously hold down the L and R.  


### What Metroid Prime mods/tools does this work with?
It is recommended to use a vanilla ISO with the latest release of [Dolphin](https://dolphin-emu.org/download/#).  
* Not thoroughly tested; but some users report that these work
  * [PrimeHack](https://forums.dolphin-emu.org/Thread-fork-primehack-fps-controls-and-more-for-metroid-prime)
  * [Widescreen HUD Mod](https://wiki.dolphin-emu.org/index.php?title=Metroid_Prime_(GC)#16:9_HUD_Mod) (0-00 USA only)
  * [MPItemTracker](https://github.com/UltiNaruto/MPItemTracker)
* Not compatible
  * Practice Mod (none of the legacy and current versions of this mod are not recognized by the client)


### Can I use tricks like Infinite Speed to collect items?
Infinite Speed can collect multiple items in the same frame - this causes issues for the Client connection.  
It is recommended to avoid using Infinite Speed, especially if using it picks up multiple items at once.


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
  - When Morph Ball Bomb is acquired, Spring Ball can be used.    
    To use Spring Ball, tilt the C-Stick Up.  
- Other Changes:
  - See the game's Template Options (after generating template options in Archipelago) for additional changes.
