import sys
import logging
import atexit
import copy
from shellathon.utils.modules_utils import get_modulename


DATEFMT = '%Y-%m-%d %H:%M:%S'

BASIC_FMT = '%(asctime)-25s %(name)-30s %(levelname)-10s %(message)s'
BASIC_MULTI_PROCESS_FMT = '%(asctime)-25s %(processName)-30s %(threadName)-30s %(name)-30s %(levelname)-10s %(message)s'
FULL_FMT = '%(asctime)-25s %(threadName)-30s %(name)-30s %(levelname)-10s %(module)-20s %(lineno)-10d %(message)s'

BASIC_FIELDS = ['asctime', 'processName', 'name', 'levelname', 'module', 'lineno', 'msg']


def get_logger(name, use_aggregation=False):
    logger = logging.getLogger(get_modulename(sys.modules[name]))
    if use_aggregation:
        logger.addFilter(AggregatorFilter())
    return logger


class NewlineFormatter(logging.Formatter):
    def format(self, record):
        msg = super().format(record)
        if record.message != "":
            parts = msg.split(record.message)
            msg = msg.replace('\n', f'\n{parts[0]}[cont] ')
        return msg


class AggregatorFilter(logging.Filter):
    class TrackedInfo:
        def __init__(self, record):
            self.record = copy.deepcopy(record)
            self.name = record.name
            self.msg = record.msg
            self.counter = 1

        def is_dup(self, record):
            return self.msg == record.msg and self.name == record.name


    def __init__(self, *args, **kws):
        super().__init__(*args, **kws)
        self.tracked_info = None
        self.is_exit_triggered = False
        atexit.register(self.exit)


    def fix_record(self, record, tracked_info):
        d = tracked_info.record.__dict__
        msg, counter = tracked_info.msg, tracked_info.counter
        d['msg'] = msg if counter == 1 else f'(x{counter}) {msg}'
        record.__dict__ = d


    def filter(self, record):
        if self.is_exit_triggered:
            self.fix_record(record, self.tracked_info)
            return True

        if self.tracked_info and self.tracked_info.is_dup(record):
            self.tracked_info.counter += 1
            return False

        last_tracked_info = copy.deepcopy(self.tracked_info)
        self.tracked_info = self.TrackedInfo(record)

        if last_tracked_info is None:
                return False

        self.fix_record(record, last_tracked_info)
        return True

    def exit(self):
        self.is_exit_triggered = True
        if self.tracked_info:
            logging.getLogger(self.tracked_info.name).handle(self.tracked_info.record)


def add_stream_handler(stream=sys.stderr, level=logging.INFO, fmt=BASIC_FMT, formatter=None, logger=None):
    logger = logger or logging.getLogger()
    handler = logging.StreamHandler(stream)
    handler.setLevel(level)

    formatter = formatter or NewlineFormatter(fmt=fmt)
    handler.setFormatter(formatter)

    logger.addHandler(handler)


def add_file_handler(fullpath, fmt=FULL_FMT, level=logging.DEBUG, formatter=None, logger=None):
    logger = logger or logging.getLogger()
    handler = logging.FileHandler(fullpath)
    handler.setLevel(level)

    formatter = formatter or NewlineFormatter(fmt=fmt)
    handler.setFormatter(formatter)

    logger.addHandler(handler)



def standard_logger_config(
    fullpath = None, 
    file_level = logging.DEBUG, 
    console_level = logging.INFO,
    console_fmt = BASIC_FMT, 
    logger = None
):
    logger = logger or logging.getLogger()
    add_stream_handler(level=console_level, fmt=console_fmt, logger=logger)

    if fullpath:
        add_file_handler(fullpath, level=file_level, logger=logger)
    logger.setLevel(logging.DEBUG)
