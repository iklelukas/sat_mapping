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
        date_format = re.compile(r"^.*MSI.{3}_(\d{4})(\d{2})(\d{2}).*")
        img_info_format = re.compile(r"^.*_N(\d+)?.R(\d+)_.*")
        matches_date = re.match(date_format, name)
        matches_nr = re.match(img_info_format, name)

        try:
            y, m, d = [int(matches_date.group(i)) for i in [1, 2, 3]]
            n, r = [int(matches_nr.group(i)) for i in [1, 2]]
        except Exception as e:
            print(f"{e}:: couldn't parse {name}")
            y, m, d = (0, 0, 0)
            n, r = (0, 0)

        tile = name.split("_")[-2]
        return FolderMetaData(y, m, d, n, r, tile)


class FolderData:

    def __init__(self, folder_name: str,
                 edge_1: Tuple[float, float] = (0.0, 0.0),
                 edge_2: Tuple[float, float] = (109800.0, 109800.0)):
        self.meta = FolderMetaData.from_folder_name(folder_name)
        x_low = (min(int(edge_1[0] // 10), int(edge_2[0] // 10)))
        x_high = (max(int(edge_1[0] // 10), int(edge_2[0] // 10)))
        y_low = (min(int(edge_1[1] // 10), int(edge_2[1] // 10)))
        y_high = (max(int(edge_1[1] // 10), int(edge_2[1] // 10)))
        self.x_indices = (x_low, x_high)
        self.y_indices = (y_low, y_high)
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
