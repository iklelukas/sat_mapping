from .Util import Paths
from .Fetch import download
from .FolderData import FolderData, folders_time_frame
from os.path import join as _join, abspath as _abspath, dirname as _dirname

with open(_join(_abspath(_dirname(__file__)), "../../", 'VERSION'), 'r') as f:
    VERSION = f.read().strip()

__version__ = VERSION
__author__ = 'Lukas Ikle'
__credits__ = 'Cyborg-AI'
