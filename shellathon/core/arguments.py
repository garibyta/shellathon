import argparse
from shellathon.core.runnable_func import RunnableFunc


def with_arguments(*arguments):
    def wrapper(func):
        return RunnableFunc(func, arguments)
    return wrapper


def parse_arguments(description, arguments):
    parser = argparse.ArgumentParser(description=description)
    for argument in arguments:
        parser.add_argument(*argument.args, **argument.kws)
    return parser.parse_args()
