import logging

LOGGING_FORMAT_DEFAULT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def setup_logging(name=__name__, level=logging.INFO, format=None):
    if format is None:
        format = LOGGING_FORMAT_DEFAULT
    logging.basicConfig(level=level, format=format)
    logger = logging.getLogger(name)
    return logger
