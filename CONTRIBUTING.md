# Contributing

To develop and run the MetroidPrime world locally, you need to complete a few steps:

## Installation

- Nest the project inside of the Archipelago main project. Go to the archipelago github, clone it, and then copy/paste this project into the `worlds/metroidprime` folder (you will need to create it). I prefer removing the `.git` directory in the AP parent project so I don't accidentally commit to the wrong project
- In a shell, navigate to `worlds/metroidprime` and run `bash build/install_local_requirements.sh`. This should create `lib` folder with the required dependencies in your `metroidprime` world folder.

## Generating a seed

- As normal, place a yaml in the Archipelago parent project's `output` folder for Metroid Prime
- From the root of the parent Archipelago project run `python Generate.py` (You may need to install some dependencies for this to work, if so run `python ModuleUpdates.py` and then re run the generate script)
- The output folder should have the generated seed.

## Testing the client

The way I test the client is as follows:

- Copy a generated `.apmp1` file into your `worlds/metroidprime` dev folder.
- Add the following script to the root of the parent AP project and save it as `TestClient.py`

  ```
  from worlds.metroidprime import MetroidPrimeClient

  if __name__ == "__main__":
    MetroidPrimeClient.launch()
  ```

- From the root of your project run `python TestClient.py nameofyour.apmp1`
