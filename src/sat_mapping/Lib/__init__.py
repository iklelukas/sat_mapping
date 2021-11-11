from __future__ import absolute_import
import sys
import logging
from os.path import dirname, abspath, realpath, join
from getopt import getopt
GSUTIL_DIR = join(dirname(abspath(realpath(__file__))), "gsutil")

if GSUTIL_DIR not in sys.path:
    sys.path.append(GSUTIL_DIR)

from .gsutil.gslib import __main__ as gs_main


def gsutil(argv):
    opts, args = gs_main.opts, gs_main.args

    try:
        gs_main.context_config.create_context_config(logging.getLogger())
    except gs_main.context_config.ContextConfigSingletonAlreadyExistsError:
        pass

    def fake_context_creation(*args):
        return gs_main.context_config.get_context_config()

    config_creator = gs_main.context_config.create_context_config
    gs_main.context_config.create_context_config = fake_context_creation

    o, a = getopt(argv, 'dDvo:?h:i:u:mq', [
        'debug', 'detailedDebug', 'version', 'option', 'help', 'header',
        'impersonate-service-account=', 'multithreaded', 'quiet',
        'testexceptiontraces', 'trace-token=', 'perf-trace-token='
    ])

    while len(opts) > 0:
        opts.pop()
    while len(args) > 0:
        args.pop()
    for option in o:
        opts.append(option)
    for argument in a:
        args.append(argument)
    gs_main.main()

    gs_main.context_config.create_context_config = config_creator
