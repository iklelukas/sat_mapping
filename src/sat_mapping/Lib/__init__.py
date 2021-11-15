import subprocess
from os.path import dirname, abspath, realpath, join
from itertools import cycle as _cycle
from time import sleep as _sleep

_SPINNER = _cycle(['-', '/', '|', '\\'])

_GSUTIL_DIR = join(dirname(abspath(realpath(__file__))), "gsutil")


def gsutil(argv):
    gsutil_runner = subprocess.Popen(["python", join(_GSUTIL_DIR, "gsutil")] + argv)
    command_str = " ".join(["gsutil"] + argv)
    while gsutil_runner.poll() is None:
        _sleep(0.5)
        print(f"{command_str} {next(_SPINNER)}", end='\r')
    done = "DONE" if gsutil_runner.returncode == 0 else "FAILED"
    print(f"{command_str} {done}")
