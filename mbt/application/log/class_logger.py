import logging


def get_logger(logger_name):
    return logging.LoggerAdapter(logging.getLogger(logger_name), {})
