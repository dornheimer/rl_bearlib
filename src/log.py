import logging


LOG_LEVELS = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL}


def initialize_logger(level='debug', log_file=None):
    logger = logging.getLogger('roguelike')
    logger.setLevel(logging.DEBUG)

    if log_file is not None:
        file_handler = logging.handlers.RotatingFileHandler(log_file,
                                                            maxBytes=1048576,
                                                            backupCount=1)
        file_format = "[%(levelname)-6s:%(module)s:%(funcName)s]: %(message)s"
        file_formatter = logging.Formatter(file_format)
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(LOG_LEVELS[level])
        logger.addHandler(file_handler)

    console = logging.StreamHandler()
    console_format = "%(asctime)s %(levelname)-8s[%(funcName)s]: %(message)s"
    date_format = "%H:%M:%S"
    console_formatter = logging.Formatter(console_format, date_format)
    console.setFormatter(console_formatter)
    console.setLevel(LOG_LEVELS[level])
    logger.addHandler(console)

    return logger
