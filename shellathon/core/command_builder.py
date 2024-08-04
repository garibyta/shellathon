import logging
import copy
import sys
from shellathon.utils.shell_utils import reverse_argparse
from shellathon.utils.dict_utils import exclude_nones, to_dict
from shellathon.utils.modules_utils import get_classpath, get_module_fullpath
from shellathon.core import run_func
from shellathon.core.helpers import as_regular_func
from shellathon.core.common_arguments import console_level_argument


def validate_required(runnable_func, func_kws):
    # TODO: can it be validated in reverse_argparse?
    required = [x.naked_name for x in runnable_func.arguments if x.kws.get('required', False)]
    given = func_kws.keys()
    missing = set(required) - set(given)
    assert not missing, f'Missing required arguments {missing}'


def hacky_argument(argument, val):
    argument = copy.deepcopy(argument)
    argument.kws['default'] = argument.encoder(val)
    if 'type' in argument.kws:
        argument.kws['type'] = str
    if 'required' in argument.kws:
        del argument.kws['required']
    return argument


def build_shellathon_command(
    runnable_func, 
    pyexe = None, 
    console_level = logging.DEBUG, 
    **func_kws
):
    # TODO: not elegant
    real_func_kws = exclude_nones(func_kws)

    argument_of_name = to_dict(runnable_func.arguments, by='naked_name')
    validate_required(runnable_func, real_func_kws)
    
    return reverse_argparse(
        pyexe = pyexe or sys.executable,
        module_path = get_module_fullpath(run_func),
        subparser = get_classpath(as_regular_func(runnable_func)),
        arguments = [
            console_level_argument(default=console_level)
        ] + [
            hacky_argument(argument_of_name[key], val) for key, val in real_func_kws.items()
        ],
    )
