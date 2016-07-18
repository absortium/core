import inspect
import logging
from functools import wraps

import pp

__author__ = 'andrew.shvv@gmail.com'


def get_prev_method_name():
    return inspect.stack()[2][3]


def pretty_wrapper(func):
    @wraps(func)
    def decorator(msg, *args, **kwargs):
        pretty_msg = "Func:  %s\n" % get_prev_method_name()

        if type(msg) == str:
            pretty_msg += msg
        else:
            pretty_msg += pp.fmt(msg)
        pretty_msg += "\n+ " + "- " * 30 + "+\n"

        func(pretty_msg, *args, **kwargs)

    return decorator


class LogMixin(object):
    def __init__(self):
        super().__init__()

        # create logger
        name = '.'.join([__name__, self.__class__.__name__])
        self.logger = getLogger(name)


def wrap_logger(logger):
    logger.info = pretty_wrapper(logger.info)
    logger.debug = pretty_wrapper(logger.debug)
    logger.warning = pretty_wrapper(logger.warning)
    logger.exception = pretty_wrapper(logger.exception)
    return logger


def getPrettyLogger(name, level=None):
    from django.conf import settings

    if settings.WHOAMI == "DJANGO":
        if level is None:
            level = logging.DEBUG
        return getLogger(name, level)

    elif settings.WHOAMI == "CELERY":
        if level is None:
            level = logging.DEBUG
        return getLogger(name, level)
    #
    #     from celery.utils.log import get_task_logger
    #     logger = get_task_logger(name)
    #     logger.setLevel(level)
    #     return wrap_logger(logger)

    else:
        if level is None:
            level = logging.DEBUG
        return getLogger(name, level)


def getLogger(name="", level=logging.DEBUG):
    # create logger
    logger = logging.getLogger(name)
    logger = wrap_logger(logger)

    # create console handler and set level to debug
    ch = logging.StreamHandler()

    # create formatter
    formatter = logging.Formatter('\nLevel: %(levelname)s - %(name)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    logger.setLevel(level)

    return logger
