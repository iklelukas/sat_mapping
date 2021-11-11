import re
from os import listdir
from os.path import join
from numpy import stack, float32, asarray
from glymur import Jp2k
from ..Util import Channels, Paths
from typing import Union
from datetime import datetime
from typing import Tuple


class FolderMetaData:

    def __init__(self, y: int, m: int, d: int, n: int, r: int, tile: str):
        self.year = y
        self.month = m
        self.day = d
        self.n = n
        self.r = r
        self.tile = tile

    @staticmethod
    def from_folder_name(name: str):
        # example name "S2A_MSIL1C_20191007T103021_N0208_R108_T32TMT_20191007T123034.SAFE"
        segments = name.split("_")
        date = segments[-1]
        date_format = re.compile(r"^(\d{4})(\d{2})(\d{2}).*")
        img_info_format = re.compile(r"^N(\d+)?.R(\d+)")
        matches = re.match(date_format, date)
        y, m, d = [int(matches.group(i)) for i in [1, 2, 3]]
        matches = re.match(img_info_format, segments[-4] + segments[-3])
        n, r = [int(matches.group(i)) for i in [1, 2]]
        tile = segments[-2]
        return FolderMetaData(y, m, d, n, r, tile)


class FolderData:

    def __init__(self, folder_name: str,
                 upper_left: Tuple[float, float] = (0.0, 0.0),
                 lower_right: Tuple[float, float] = (109800.0, 109800.0)):
        self.meta = FolderMetaData.from_folder_name(folder_name)
        self.x_indices = (int(upper_left[0] // 10), int(lower_right[0] // 10))
        self.y_indices = (int(upper_left[1] // 10), int(lower_right[1] // 10))
        self._folder = folder_name
        self._img_path = join(self._folder, f"GRANULE/{listdir(join(self._folder, 'GRANULE'))[0]}/IMG_DATA")
        self._img_names = listdir(self._img_path)
        data = [self._load_channel(Channels(i)) for i in [0, 1, 2, 3]]
        self.data = stack(data, axis=-1)

    def _load_channel(self, channel: Channels):
        for img_name in self._img_names:
            if img_name.split(".")[0].endswith(channel.sentinel_short()):
                jp2 = Jp2k(join(self._img_path, img_name))
                x = slice(self.x_indices[0], self.x_indices[1])
                y = slice(self.y_indices[0], self.y_indices[1])
                return asarray(jp2[y, x], dtype=float32) / 4096.0


def folders_time_frame(paths: Paths, time_start: Union[datetime, None], time_end: Union[datetime, None]):
    folders = paths.folders
    folder_meta = map(lambda name: (name, FolderMetaData.from_folder_name(name)), folders)
    result = []
    for (name, meta) in folder_meta:
        folder_time = datetime(meta.year, meta.month, meta.day)
        later_as_start = time_start is None or folder_time >= time_start
        before_end = time_end is None or folder_time <= time_end
        if later_as_start and before_end:
            result.append(name)
    return result
