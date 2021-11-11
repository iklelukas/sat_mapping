from os.path import join
import matplotlib.pyplot as plt
from datetime import datetime

from sat_mapping import FolderData, folders_time_frame, Paths, download


if __name__ == '__main__':
    plt.switch_backend("TkAgg")
    plt.ion()
    paths = Paths("/home/cyberman/data/sentinel2")
    download(paths, years=[2019], tiles=["32TMT"], months=[7])
    after = datetime(2019, 6, 6)
    before = datetime(2019, 8, 8)
    folders = folders_time_frame(paths, after, before)
    data = FolderData(join(paths.data_path, folders[11]), (100000.0, 0.0), (109800.0, 10000.0))
    # picture = data.data[:, :, :-1]
    picture = data.data[:, :, [3, 1, 2]]
    fig: plt.Figure = plt.figure()
    plt.imshow(picture)
    plt.show()
    figure_closed = False
    while not figure_closed:
        try:
            fig.canvas.flush_events()
        except Exception:
            figure_closed = True
    print(data)
