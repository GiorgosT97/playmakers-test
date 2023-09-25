""" Logging module where basic logging logic is done """
import logging


class Logger():
    """ This class is used for logging messages. Logging configuration will be done here instead of config class """

    def __init__(self, module):
        self.logger = logging.getLogger(module)
        logging.root.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s | %(name)-8s | %(levelname)-7s | %(message)s')
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)
        # File handler
        file_handler = logging.FileHandler('logs/main.log')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        # Set the handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def logMessage(self, message="", level="info"):
        """ 
        Method for logging all messages.
        Parameters:
            message (string): message to log 
            level (string): defaults as info. Can be either info, warning, error or debug
        Logs out logging message
        """
        if (level == 'error'):
            self.logger.error(message)
        elif (level == 'warning'):
            self.logger.warning(message)
        elif (level == 'debug'):
            self.logger.debug(message)
        else:
            self.logger.info(message)
