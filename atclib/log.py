# $Id$
import logging


def setup_custom_logger(name, loggingLevel, fileLocation=None):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, loggingLevel))
    logger.addHandler(handler)
    if fileLocation:
        fileHandler = logging.FileHandler(fileLocation)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)
    return logger
