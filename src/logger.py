import logging
import os

def get_logger(name):
    basis_map = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logs_map = os.path.join(basis_map, "logs")

    os.makedirs(logs_map, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    log_bestand = os.path.join(logs_map, "pipeline.log")
    file_handler = logging.FileHandler(log_bestand)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
