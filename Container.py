import os
import zipfile
from worlds.Files import APContainer


class MetroidPrimeContainer(APContainer):
    game: str = 'Metroid Prime'

    def __init__(self, config_json: str, outfile_name: str, output_directory: str,
                 player=None, player_name: str = "", server: str = ""):
        self.config_json = config_json
        self.config_path = "config.json"
        container_path = os.path.join(output_directory, outfile_name + ".apmp1")
        super().__init__(container_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        opened_zipfile.writestr(self.config_path, self.config_json)
        super().write_contents(opened_zipfile)
