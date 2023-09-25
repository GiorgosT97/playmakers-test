from Badge import Badge
from Logger import Logger
import sys

LOGGER = Logger(__name__)

if __name__ == "__main__":
    try:
        badge = Badge(sys.argv[1])
        if ("-T" in sys.argv):
            badge.transform_image()
        else:
            badge.perform_checks()
    except Exception as err:
        LOGGER.logMessage(err.args[-1], "error")
