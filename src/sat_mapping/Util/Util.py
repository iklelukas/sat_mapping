from os import listdir, makedirs
from os.path import join, abspath, realpath
from typing import List


class Paths:

    def __init__(self, base_path: str):
        self.base_path = abspath(realpath(base_path))
        self.data_path = join(base_path, "data")
        makedirs(self.data_path, exist_ok=True)

    @property
    def folders(self) -> List[str]:
        return listdir(self.data_path)


class Channels:

    RED = 0
    GREEN = 1
    BLUE = 2
    VNIR = 3

    CHANNELS = [RED, GREEN, BLUE, VNIR]

    CHANNEL_NAMES = {
        "red": RED,
        "green": GREEN,
        "blue": BLUE,
        "vnir": VNIR
    }

    def __init__(self, channel):
        assert channel in self.CHANNELS or channel in self.CHANNEL_NAMES
        if channel in self.CHANNEL_NAMES:
            self.channel = self.CHANNEL_NAMES[channel]
        else:
            self.channel = channel

    def sentinel_short(self):
        if self.channel == self.RED:
            return "B04"
        elif self.channel == self.GREEN:
            return "B03"
        elif self.channel == self.BLUE:
            return "B02"
        elif self.channel == self.VNIR:
            return "B08"
