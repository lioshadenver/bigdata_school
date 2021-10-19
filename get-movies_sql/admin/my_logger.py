from logging import StreamHandler, Formatter
import logging
import sys


def get_logger():
    '''
    function creates and returns logger. Logger output error mesagges in STDUOT
    '''
    try:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        handler = StreamHandler(stream=sys.stdout)
        handler.setFormatter(Formatter(fmt=
            '[%(asctime)s: %(levelname)s] %(message)s'))  # messages format
        logger.addHandler(handler)
        return logger
    except Exception as err:
        logger.error(f'error in logger() function. Error massage: {err}')
