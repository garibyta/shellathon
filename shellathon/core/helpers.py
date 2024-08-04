import sys
import traceback
from shellathon.utils.modules_utils import load_class
from shellathon.core.runnable_func import RunnableFunc
from shellathon.core.arguments import with_arguments


def as_runnable_func(obj):
    return obj if isinstance(obj, RunnableFunc) else with_arguments()(obj)

def as_regular_func(obj):
    return obj.func if isinstance(obj, RunnableFunc) else obj


def load_path(path, print_traceback=False):
    try:
        func = load_class(path)
    except Exception as e:
        short_message = f"{'*'*80}\nFailed to load path {path}:\n{e!r}\n{'*'*80}\n"
        long_message = traceback.format_exc()
        message = long_message if print_traceback else short_message
        print(message)
        return

    return as_runnable_func(func)


def display_help():
    if len(sys.argv) < 3:
        return

    if '-h' not in sys.argv:
        return

    factory = load_path(sys.argv[1], print_traceback=False)
    if factory:
        factory.parse_args(sys.argv)
