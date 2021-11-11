from datetime import datetime
from time import process_time
from os.path import isfile, isdir, join
from os import system, makedirs, getenv
from typing import List, Union
from ..Lib import gsutil
from ..Util import Paths
from itertools import cycle

SPINNER = cycle(["-", "\\", "|", "/"])

# COLUMS  : 'GRANULE_ID',
#           'PRODUCT_ID',
#           'DATATAKE_IDENTIFIER',
#           'MGRS_TILE',
#           'SENSING_TIME',
#           'TOTAL_SIZE',
#           'CLOUD_COVER',
#           'GEOMETRIC_QUALITY_FLAG',
#           'GENERATION_TIME',
#           'NORTH_LAT',
#           'SOUTH_LAT',
#           'WEST_LON',
#           'EAST_LON',
#           'BASE_URL'

# Time format : 2020-06-04T04:18:22.187000Z (UTC)
TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def download(path: Paths,
             years: List[int] = [2019],
             tiles: List[str] = ["32TMT"],
             months: Union[List[int], None] = None):
    base_path = path.base_path
    makedirs(base_path, exist_ok=True)
    urls = []
    tiles_str = "_".join([str(tile) for tile in tiles])
    years_str = "_".join([str(year) for year in years])
    months_str = "_" + "_".join([str(month) for month in months]) if months is not None else ""
    url_file = f"urls_{tiles_str}_{years_str}" + months_str + ".txt"

    # if gsutil is not configured, configure it. (might not work on Windows)
    if not (isdir(join(getenv("HOME"), ".gsutil")) or isfile(join(getenv("HOME"), ".boto"))):
        gsutil(["config"])

    # Check if an index file for the specified time/tile exists
    if not isfile(join(base_path, url_file)):

        # Download and Unzip index file
        if not isfile(join(base_path, "index.csv")):
            print("DOWNLOADING SENTINEL INDEX")
            gsutil(["cp", "gs://gcp-public-data-sentinel-2/index.csv.gz", base_path])
            print("UNZIPPING...")
            command = "gunzip {}".format(join(base_path, "index.csv"))
            system(command)

        # Read the index file line wise
        print(f"FILTER index for {tiles} {years} {months}")
        with open(join(base_path, "index.csv"), "r") as f:

            # Get Column information from the first line.
            line = f.readline()
            column_names = line[:-1].split(",")
            year_index = column_names.index("SENSING_TIME")
            tile_index = column_names.index("MGRS_TILE")
            url_index = column_names.index("BASE_URL")
            time = process_time()

            # Check the date and tile info for each line.
            while line:
                if process_time() - time > 0.7:
                    print(f"READING INDEX FILE: {SPINNER.__next__()}", end="\r")
                    time = process_time()
                line = f.readline()
                items = line.split(",")
                try:
                    date = datetime.strptime(items[year_index], TIME_FORMAT)
                    tile = items[tile_index]
                    if date.year in years and tile in tiles and date.month in months:
                        # Add the URL
                        urls.append(items[url_index])
                except IndexError:
                    print(line)

        # Save for future use.
        with open(join(base_path, url_file), "w") as f:
            f.writelines(urls)
    else:
        with open(join(base_path, url_file), "r") as f:
            urls = f.readlines()

    if not isdir(join(base_path, "data")):
        makedirs(join(base_path, "data"), exist_ok=True)

    # Download the previously specified data
    for url in urls:
        if not isdir(join(base_path, "data", url.split("/")[-1][:-1])):
            gsutil(["-m", "cp", "-r", url[:-1], join(base_path, "data")])


