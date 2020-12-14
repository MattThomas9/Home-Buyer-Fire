import logging


def logtofile(name, message, lvl):
    logging.basicConfig(
        filename="hbfDev.log",
        filemode="w",
        format="%(asctime)s - %(name)s - %(levelname)s:\n%(message)s",
        level=logging.INFO,
    )
    logger = logging.getLogger(name)
    if lvl == "DEBUG":
        logger.debug(message)
    elif lvl == "INFO":
        logger.info(message)
    elif lvl == "WARNING":
        logger.warning(message)
        print(message)
    elif lvl == "ERROR":
        logger.error(message)
        print(message)
    elif lvl == "CRITICAL":
        logger.critical(message)
        print(message)
