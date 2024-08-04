
import pprint
from shellathon import with_arguments, Argument, Rest
from shellathon.utils.logger import get_logger


logger = get_logger(__name__, use_aggregation=True)


@with_arguments()
def no_params():
    " no doc "
    print('do nothing')


@with_arguments(
    Argument('--float_param', type=float, required=True, help='float param'),
    Argument('--str_param', type=str, required=False, help='str param'),
    Argument("--bool_param", action='store_true', help='bool param'),
    Argument('--with_default', type=str, required=False, help='not required param'),
    Rest(),
    
)
def with_params(
    float_param = 1.1, 
    str_param = 'foo', 
    bool_param = False, 
    with_default = 'bla', 
    _rest = None,
):
    " some useful doc "
    for i in range(3):
        logger.info('some message')

    logger.debug('another message')
    params = dict(
        float_param = float_param,
        str_param = str_param,
        bool_param = bool_param,
        with_default = with_default,
    )

    logger.info(pprint.pformat(params))

    logger.info(f'_rest: {_rest}')
