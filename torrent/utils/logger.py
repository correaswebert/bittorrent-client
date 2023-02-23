import logging
from logging import WARNING
from colorlog import ColoredFormatter


F_LOGFORMAT = (
    "%(asctime)s [%(levelname)s] %(module)s:%(funcName)s:%(lineno)d -- %(message)s"
)
C_LOGFORMAT = (
    "[%(log_color)s%(levelname)s%(reset)s] "
    "%(log_color)s%(module)s:%(funcName)s:%(lineno)d%(reset)s -- "
    "%(log_color)s%(message)s%(reset)s"
)


f_formatter = logging.Formatter(F_LOGFORMAT)
c_formatter = ColoredFormatter(C_LOGFORMAT)

file = logging.FileHandler("file.log")
file.setFormatter(f_formatter)

stream = logging.StreamHandler()
stream.setFormatter(c_formatter)

log = logging.getLogger("root")
log.addHandler(file)


def set_log_level(loglevel):
    loglevel = loglevel.upper()
    if loglevel not in ["DEBUG", "INFO", "WARN", "WARNING", "ERROR", "CRITICAL"]:
        loglevel = logging.WARNING

    logging.root.setLevel(loglevel)
    file.setLevel(loglevel)
    stream.setLevel(loglevel)


def stream_logs():
    """Enable streaming logs to the console"""
    log.addHandler(stream)


if __name__ == "__main__":
    log.warning("This is a warning!")
    log.debug("This is a debugging message.")

# https://stackoverflow.com/questions/15870380/python-custom-logging-across-all-modules
