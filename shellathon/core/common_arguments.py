import logging
from shellathon.core.argument import Argument


def script_path_argument(help='Python path to the script function', **kws):
    return Argument('script_path', type=str, help=help, **kws)

def console_level_argument(default=logging.INFO, help='Console logging level', **kws):
    return Argument('--console_level', type=int, default=default, help=help, **kws)
