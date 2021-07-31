"""
This is not an script file, It's meant to be imported.

This is for interacting with '../var/'.json files


Author: SasumaTho
Discord: SasumaTho#9999

Status: Still in development.

"""


import json

class MyJson:
    folder: str = 'jsonfiles/'

    def __init__(self, filename: str, write: bool=False) -> None:
        self.filename: str = filename
        self.write: bool = write
        self.data: dict = self.get()


    def get(self) -> dict:
        with open(self.folder + self.filename) as f:
            return json.load(f)


    def save(self) -> None:
        with open(self.folder + self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)


    def __enter__(self) -> dict:
        return self.data


    def __exit__(self, *args, **kwargs):
        if self.write:
            self.save()


    @classmethod
    def read(cls, filename: str) -> dict:
        return cls(filename)


    @classmethod
    def readwrite(cls, filename: str) -> dict:
        return cls(filename, write=True)


    @classmethod
    def rw(cls, filename: str) -> dict: # This is the same as readwrite but just rw
        return cls(filename, write=True)
