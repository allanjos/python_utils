import logging
from config import Config

Config.load()

LOGGING_FORMAT_MESSAGE = '[%(process)d] %(levelname)s: %(message)s'

LOGGING_LEVEL = logging.INFO

if Config.data()['logging']['level'] == 'debug':
    LOGGING_LEVEL = logging.DEBUG
elif Config.data()['logging']['level'] == 'info':
    LOGGING_LEVEL = logging.INFO
elif Config.data()['logging']['level'] == 'warning':
    LOGGING_LEVEL = logging.WARNING
elif Config.data()['logging']['level'] == 'critical':
    LOGGING_LEVEL = logging.CRITICAL
elif Config.data()['logging']['level'] == 'fatal':
    LOGGING_LEVEL = logging.FATAL

logging.basicConfig(level=LOGGING_LEVEL, format=LOGGING_FORMAT_MESSAGE)

class Log:
    @staticmethod
    def dbg(msg):
        logging.debug(msg)

    @staticmethod
    def info(msg):
        logging.info(msg)

    @staticmethod
    def error(msg):
        logging.error(msg)

    @staticmethod
    def exception(msg):
        logging.exception(msg, exc_info=True)
