import datetime
import logging
import sys
import __main__

PREFIX = "spotifriends"
LOG_PATH = "logs/"
LOG_NAME = f"{PREFIX}_{datetime.datetime.now().date()}"

logger = logging.getLogger(PREFIX)

logFormatter = logging.Formatter(
    "%(asctime)s [%(levelname)-5.5s]  %(message)s"  # [%(threadName)-12.12s]
)

fileHandler = logging.FileHandler(
    "{0}/{1}.log".format(LOG_PATH, LOG_NAME),
    mode="a+",
)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)
logger.setLevel(logging.DEBUG)
logger.info("\n\n>>>>> start execution")
