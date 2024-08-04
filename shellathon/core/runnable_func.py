import argparse
import inspect
from functools import update_wrapper
from shellathon.utils.iterable_utils import non_consecutive_groupby
from shellathon.utils.modules_utils import get_classpath
from shellathon.utils.dict_utils import to_dict
from shellathon.core.argument import Rest


class MyFormatter(argparse.RawTextHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
    pass

class RunnableFunc:
    def __init__(self, func, arguments):
        self.func = func
        self.arguments = arguments
        self.known_arguments, self.rest_argument = self.process_arguments(arguments)

        update_wrapper(self, self.func)

    @property
    def underlying_func(self):
        return self.func
    

    @property
    def argument_of_name(self):
        return to_dict(self.known_arguments, by='naked_name')

    
    def process_arguments(self, arguments):
        by_flag = dict(non_consecutive_groupby(
            enumerate(arguments), lambda x: isinstance(x[1], Rest)))
        
        known = by_flag.get(False, [])
        rest = by_flag.get(True, [])

        assert len(rest) < 2, 'There should not be more than one Rest'
        rest_argument = None
        if rest:
            rest_index, rest_argument = rest[0]
            assert rest_index == len(arguments) - 1, 'Rest must be declared last'

        known_arguments = [x[1] for x in known]
        return known_arguments, rest_argument


    def apply_func(self, *args, **kws):
        return self.underlying_func(*args, **kws)


    def __call__(self, *args, **kws):
        return self.apply_func(*args, **kws)
    
    
    def get_defaults(self):
        signature = inspect.signature(self.underlying_func)

        return {
            x.name: x.default
            for x in signature.parameters.values()
            if x.default is not inspect.Parameter.empty
        }


    def get_parser(self):
        prog = get_classpath(self.underlying_func)
        parser = argparse.ArgumentParser(
            prog=prog, description=self.underlying_func.__doc__, formatter_class=MyFormatter)

        for argument in self.known_arguments:
            parser.add_argument(*argument.args, **argument.kws)

        defaults = self.get_defaults()
        parser.set_defaults(**defaults)
        return parser


    def parse_args(self, args=None, is_strict=False):
        parser = self.get_parser()
        args = args or []
        if is_strict:
            known_args = parser.parse_args(args)
            _rest = None
        else:
            known_args, _rest = parser.parse_known_args(args)

        params = vars(known_args)
        if _rest:
            params['_rest'] = (params.get('_rest') or []) + _rest

        return params


    def run_args(self, args):
        kws = self.parse_args(args)
        return self.apply_func(**kws)
