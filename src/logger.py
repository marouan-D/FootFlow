# logger.py
# Dit bestand zorgt voor de logging van de FootFlow pipeline.
# Alle meldingen en fouten worden weggeschreven naar logs/pipeline.log

import logging
import os

def get_logger(name):
    """
    Maak een logger aan met de opgegeven naam.
    Logs worden weggeschreven naar logs/pipeline.log en de terminal.
    """
    # Zorg dat de logs map bestaat
    os.makedirs("logs", exist_ok=True)

    # Maak de logger aan
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Formaat van de log berichten
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Log naar bestand
    file_handler = logging.FileHandler("logs/pipeline.log")
    file_handler.setFormatter(formatter)

    # Log naar terminal
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Voeg handlers toe aan logger
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger