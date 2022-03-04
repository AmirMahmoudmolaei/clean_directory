import shutil
from pathlib import Path
import json
from loguru import logger
from src.data import DATA_DIR
from src.utils.io import read_json

class Oragnizefiles:
    """
    This class is used to organize files in a directory by
    moving files into directories based on extension.
    """

    def __init__(self, directory):
        self.directory = Path(directory)
        if not self.directory.exists():
            raise FileNotFoundError(f'{self.directory}dose not exist')

        ext_dirs = read_json(DATA_DIR / "extensions.json")
        self.extensions_dest = {}
        for dir_name, ext_list in ext_dirs.items():
            for ext in ext_list:
                self.extensions_dest[ext] = dir_name



    def __call__(self):
        """
        Organize files in directory by moving them to sub directories
        based on extensions.
        """
        logger.info(f"Organizing files in {self.directory}...")
        file_extensions = []
        for file_path in self.directory.iterdir():
            # ignor directories
            if file_path.is_dir():
                continue

            # ignor hidden files
            if file_path.name.startswith('.'):
                continue

            # get all file types
            file_extensions.append(file_path.suffix)

            # moving files to Destination folder
            if file_path.suffix not in self.extensions_dest:
                DEST_DIR = self.directory / 'other'

            else:
                DEST_DIR = self.directory / self.extensions_dest[file_path.suffix]

            DEST_DIR.mkdir(exist_ok=True)
            logger.info(f'Moving {file_path} to {DEST_DIR}...')
            shutil.move(str(file_path), str(DEST_DIR))


if __name__ == "__main__":
    org_files = Oragnizefiles('/mnt/c/Users/HP/Downloads')
    org_files()
    logger.info("Done!")