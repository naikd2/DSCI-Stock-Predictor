import json
from pathlib import Path

class FileService:

    def __init__(self, clean=False):
        self.clean = clean
        pass

    def save_file(self, data:dict, filename:str):
        self.__create_directories(filename)
        with open(filename, 'w+') as f:
            json.dump(data, f)
        return

    def file_exists(self, filename:str):
        f = Path(filename)
        if f.exists():
            return True
        else:
            return False

    def __create_directories(self, filename:str):
        paths = filename.split("/")
        Path("/".join(paths[:-1])).mkdir(parents=True, exist_ok=True)
