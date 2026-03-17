# scheduler.py
# Dit bestand beheert de automatische uitvoering van de pipeline.
# De pipeline wordt elke dag om 08:00 automatisch gestart via APScheduler.

from apscheduler.schedulers.blocking import BlockingScheduler
from logger import get_logger

logger = get_logger(__name__)

class PipelineScheduler:
    """
    Klasse voor het automatisch uitvoeren van de data pipeline.
    """

    def __init__(self, pipeline_functie):
        """
        Initialiseer de scheduler met de pipeline functie.
        """
        self.scheduler = BlockingScheduler()
        self.pipeline_functie = pipeline_functie

    def start(self):
        """
        Start de scheduler — pipeline draait elke dag om 08:00.
        """
        try:
            # Voeg de taak toe aan de scheduler
            self.scheduler.add_job(
                self.pipeline_functie,
                trigger="cron",
                hour=8,
                minute=0,
                id="footflow_pipeline"
            )

            logger.info("Scheduler gestart — pipeline draait elke dag om 08:00.")
            self.scheduler.start()

        except Exception as e:
            logger.error(f"Fout bij starten scheduler: {e}")

    def stop(self):
        """Stop de scheduler."""
        try:
            self.scheduler.shutdown()
            logger.info("Scheduler gestopt.")
        except Exception as e:
            logger.error(f"Fout bij stoppen scheduler: {e}")