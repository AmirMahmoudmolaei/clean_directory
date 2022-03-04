import json
import shutil
from pathlib import Path
from typing import Union

from loguru import logger

from src.data import DATA_DIR
from src.utils.io import read_json


class Oragnizefiles:
    """
    This class is used to organize files in a directory by
    moving files into directories based on extension.
    """

    def __init__(self, extensions_dest=None):
        ext_dirs = read_json(DATA_DIR / "extensions.json")
        self.extensions_dest = {}
        for dir_name, ext_list in ext_dirs.items():
            for ext in ext_list:
                self.extensions_dest[ext] = dir_name



    def __call__(self, directory: Union[str, Path]):
        """
        Organize files in directory by moving them to sub directories
        based on extensions.
        """
        directory = Path(directory)
        if not directory.exists():
            raise FileNotFoundError(f'{directory}dose not exist')

        logger.info(f"Organizing files in {directory}...")
        file_extensions = []
        for file_path in directory.iterdir():
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
                DEST_DIR = directory / 'other'

            else:
                DEST_DIR = directory / self.extensions_dest[file_path.suffix]

            DEST_DIR.mkdir(exist_ok=True)
            logger.info(f'Moving {file_path} to {DEST_DIR}...')
            shutil.move(str(file_path), str(DEST_DIR))


if __name__ == "__main__":
    org_files = Oragnizefiles()
    org_files('/mnt/c/Users/HP/Downloads')
    logger.info("Done!")
