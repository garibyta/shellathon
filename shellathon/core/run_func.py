import argparse
import sys
from shellathon.utils.logger import BASIC_MULTI_PROCESS_FMT, standard_logger_config
from shellathon.core.common_arguments import console_level_argument, script_path_argument
from shellathon.core.helpers import load_path, display_help


def run_func(script_path, script_args):
    factory = load_path(script_path, print_traceback=True)
    if not factory:
        sys.exit(1)

    factory.run_args(script_args)


def main():
    parser = argparse.ArgumentParser()
    arguments = [
        script_path_argument(),
        console_level_argument(),
    ]
    for argument in arguments:
        parser.add_argument(*argument.args, **argument.kws)

    display_help()
    args, script_args = parser.parse_known_args()
    standard_logger_config(console_level=args.console_level, console_fmt=BASIC_MULTI_PROCESS_FMT)
    run_func(args.script_path, script_args)


if __name__ == '__main__':
    main()