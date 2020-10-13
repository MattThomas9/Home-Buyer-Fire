import logging


def logToFile(name, data, lvl):
    logging.basicConfig(
        filename="hbfDev.log",
        format="%(asctime)s - %(name)s - %(levelname)s:\n%(message)s",
    )
    logger = logging.getLogger(name)
    level = logging.getLevelName(lvl)
    logger.setLevel(lvl)
    logger.info(data)
