import subprocess
import argparse

from reverse_argparse import ReverseArgumentParser


def reverse_argparse(pyexe, module_path, arguments, subparser=None):
    root_parser = argparse.ArgumentParser()

    if subparser:
        subparsers = root_parser.add_subparsers()
        parser = subparsers.add_parser(subparser)
    else:
        parser = root_parser

    for argument in arguments:
        parser.add_argument(*argument.args, **argument.kws)

    args = [
        action.default for action in parser._actions 
        if not action.option_strings]

    unparser = ReverseArgumentParser(parser, parser.parse_args(args))
    effective_cmdline = unparser.get_effective_command_line_invocation()
    stripped_cmd = effective_cmdline.split(' ',1)[1]

    runner_cmd = subprocess.list2cmdline([pyexe, module_path])
    return f'{runner_cmd} {stripped_cmd}'
