import logging
from decouple import config

LOGLEVEL = config("LOGLEVEL", default=logging.DEBUG)
LOGFORMAT = config(
    "LOGFORMAT",
    default="::::%(asctime)s::::%(levelname)s::::%(filename)s:%(funcName)s():%(lineno)d::::%(message)s::::",
)
LOGFILE = config("LOGFILE", default="log.log")


def get_logger():
    fmt = logging.Formatter(LOGFORMAT)

    # init logger
    logger = logging.getLogger(__name__)
    logger.setLevel(LOGLEVEL)

    # add filehandler:
    fh = logging.FileHandler(LOGFILE)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    # add streamhandler
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    logger.addHandler(sh)
    return logger


logger = get_logger()


def await_input(prompt:str,allow:list[str]=[])->str:
    """_summary_

    Args:
        prompt (str): question to ask user
        allow (list[str], optional): Allowed string as answer (case-insensitive). Defaults to [].

    Returns:
        str: _description_
    """
    while True:
        answer = input(prompt).strip().lower()
        if answer in allow or len(allow)==0:
            return answer
        logger.info(f"Invalid prompt, must be one of {allow}")
