import pathlib
import logging

_FILE_FORMATTER = "%(asctime)s - %(levelname)s - %(message)s"
_STDOUT_FORMATTER = "%(asctime)s - %(levelname)s - %(message)s"
_LOGGER_NAME = "Manifests generation tool"
_WORK_DIRECTORY = pathlib.Path(__file__).parent.parent.parent
_LOG_LEVEL = logging.INFO
_LOG_FILE = "external_asset_ism_ismc_generation_tool.log"

""" logger.py module implemented for gathering logs into single .log file. Based on singleton pattern via Logger class instantiation. """

logging.basicConfig(level=logging.INFO)


def _construct_logger(log_file: str = _LOG_FILE):
    logger = logging.getLogger(_LOGGER_NAME)
    logger.setLevel(_LOG_LEVEL)

    file_handler = logging.FileHandler(_WORK_DIRECTORY.joinpath(log_file))
    file_handler.setLevel(_LOG_LEVEL)
    file_handler.setFormatter(logging.Formatter(_FILE_FORMATTER))
    logger.addHandler(file_handler)
    # Somehow it fixes the problem with invalid logs duplication of FileHandler into sys.stdout
    logger.propagate = False

    console_handler = logging.StreamHandler()
    console_handler.setLevel(_LOG_LEVEL)
    console_handler.setFormatter(logging.Formatter(_STDOUT_FORMATTER))
    logger.addHandler(console_handler)

    return logger


class Logger:
    __logger = _construct_logger()

    @classmethod
    def redefine_log_file(cls, log_file: str):
        cls.__logger = _construct_logger(log_file=log_file)

    """ Logger class parameterized by <name> in constructor, which used as pattern in each message.
        Used the same _logger instance for possibility writing in the same .log file by different threads and processes without conflicts.
    """
    def __init__(self, name):
        if type(name) is str:
            self.__name = name
        else:
            self.__name = type(name).__name__

    def log(self, level, msg):
        self.__logger.log(level=level, msg=f"{self.__name} - {msg}")

    def info(self, msg):
        self.__logger.info(msg=f"{self.__name} - {msg}")

    def warning(self, msg):
        self.__logger.warning(msg=f"{self.__name} - {msg}")

    def error(self, msg):
        self.__logger.error(msg=f"{self.__name} - {msg}")