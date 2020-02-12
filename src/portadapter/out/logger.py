import logging


def init(name):
    requests_logger = logging.getLogger("urllib3")
    requests_logger.setLevel(logging.DEBUG)
    requests_logger.propagate = True

    logger = logging.getLogger(name)

    logger.setLevel(logging.DEBUG)

    fh_debug = logging.FileHandler("logs/debug.log")
    fh_debug.setLevel(logging.DEBUG)

    fh_info = logging.FileHandler("logs/info.log")
    fh_info.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh_debug.setFormatter(formatter)
    fh_info.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh_debug)
    logger.addHandler(fh_info)
    logger.addHandler(ch)

    return logger
