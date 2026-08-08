import logging
from pathlib import Path
from datetime import datetime

def configura_logger(config):

    log_dir = Path(config["log_path"])

    log_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    log_file = (
        log_dir /
        f"controllo_{timestamp}.log"
    )

    logger = logging.getLogger("controllo_magazzino")

    logger.setLevel(logging.INFO)

    # Evita di aggiungere handler multipli
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S"
    )

    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger