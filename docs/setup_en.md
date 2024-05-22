# Setup Guide for Metroid Prime Archipelago

This guide is meant to help you get up and running with Metroid Prime in your Archipelago run.

Windows is the only OS this has been tested on, but feel free to let us know if you get the chance to try it on Linux or MacOS

## Requirements

The following are required in order to play Metroid Prime in Archipelago

- Installed [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) v0.4.5 or higher.\
   **Make sure to install the Generator if you intend to generate multiworlds.**
- The latest version of the [Metroid Prime apworld](https://github.com/Electro1512/MetroidAPrime/releases/latest).
- [Dolphin Emulator](https://dolphin-emu.org/download/). We recommend the latest beta version.
- A Metroid Prime US ISO (`US 0-00`)

## AP World Installation

1. Unzip the downloaded Metroid Prime apworld zip file
2. Place the `metroidprime.apworld` file in your Archipelago installation's `lib/worlds` folder (Windows default to:
   `%programdata%/Archipelago`).
3. Copy the contents of the `lib` folder from the downloaded Metroid Prime zip file into your Archipelago installation's
   `lib` folder.

- If you have a `metroidprime.apworld` file from a previous version of the apworld, you **must** delete it, as it is no longer
  supported. Additionally, if there is a `metroidprime` folder in that folder, you **must** also delete it. Keeping
  these around will cause issues, even if multiworlds are successfully generated.

## Setting Up a YAML

All players playing Metroid Prime must provide the room host with a YAML file containing the settings for their world.
A sample YAML file for Metroid Prime is supplied in the Metroid Prime apworld download. Refer to the comments in that file for
details about what each setting does.

Once complete, provide the room host with your YAML file.

## Generating a Multiworld

If you're generating a multiworld game that includes Metroid Prime, you'll need to run it locally since the online
generator does not yet support it. Follow these steps to generate a multiworld:

1. Gather all player's YAMLs. Place these YAMLs into the `Players` folder of your Archipelago installation. If the
   folder does not exist, then it must be created manually. The files here should not be compressed.
2. Modify any local host settings for generation, as desired.
3. Run `ArchipelagoGenerate.exe` (without `.exe` on Linux) or click `Generate` in the launcher. The generation output
   is placed in the `output` folder (usually named something like `AP_XXXXX.zip`). \* Please note that if any player in the game you want to generate plays a game that needs a ROM file to generate,
   you will need the corresponding ROM files.
4. Unzip the `AP_XXXXX.zip` file. It should include a zip file for each player in the room playing Metroid Prime. Distribute each file to the appropriate player.
5. **Delete the distributed zip files and re-zip the remaining files**. In the next section, use this archive file to
   host a room or provide it to the room host. \* If you plan to host the room on a local machine, skip this step and use the original zip file (`AP_XXXX.zip`) instead.

## Hosting a Room

If you're generating the multiworld, follow the instructions in the previous section. Once you have the zip file
corresponding to your multiworld, follow
[these steps](https://archipelago.gg/tutorial/Archipelago/setup/en#hosting-an-archipelago-server) to host a room. Follow
the instructions for hosting on the website from a locally generated game or on a local machine.

## Starting the Game and Connecting to a Room

You should have the `apmp1` file provided to you by the multiworld generator. You should also have the room's server
name and port number from the room's host.

Once you do, follow these steps to connect to the room:

1. Double click the `apmp1` file. If you have not done so before, it will ask you what program you want to open it with. Click "Choose another program" and browser to your Archipelago directory. Select `ArchipelagoLauncher.exe`.
2. Be patient, after clicking the `apmp1` file, it can take a minute to have the client and patched iso showup
3. If this is your first time, it will prompt you for an input iso. Select your Metroid Prime USA V1.0 (0-00) iso
4. Once the output iso file appears in the same directory as your `apmp1` file (it should have a name `AP_XXXX.iso`), open it with Dolphin
5. After the game is running, connect the Metroid Prime Client to the room by entering the server name and port number at the top and pressing `Connect`. For rooms hosted
   on the website, this will be `archipelago.gg:<port>`, where `<port>` is the port number. If a game is hosted from the
   `ArchipelagoServer.exe` (without `.exe` on Linux), this will default to `38281` but may be changed in the `host.yaml`.

## Troubleshooting

- If you do not see the client in the launcher, ensure you have placed the `metroidprime.apworld` in the correct folder (the
  `lib/worlds` folder of your Archipelago installation).

## Feedback

In the offical [Archipelago Discord](https://discord.com/invite/8Z65BR2) under the `future-game-design` channel there is a `Metroid Prime` [thread](https://discord.com/channels/731205301247803413/1172631093837570068). Feel free to ping `@Electro15` or `@hesto2` with any bugs/thoughts/complaints/wishes/jokes you may have!
