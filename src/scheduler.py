from apscheduler.schedulers.blocking import BlockingScheduler
from logger import get_logger

logger = get_logger(__name__)

class PipelineScheduler:

    def __init__(self, pipeline_functie):
        self.scheduler = BlockingScheduler()
        self.pipeline_functie = pipeline_functie

    def start(self, test_modus=False):
        try:
            if test_modus:
                self.scheduler.add_job(
                    self.pipeline_functie,
                    trigger="interval",
                    minutes=2,
                    id="footflow_pipeline_test"
                )
                logger.info("Scheduler gestart in TEST MODUS — pipeline draait elke 2 minuten.")
                print("⏰ Scheduler actief — pipeline draait elke 2 minuten. Druk Ctrl+C om te stoppen.")
            else:
                self.scheduler.add_job(
                    self.pipeline_functie,
                    trigger="cron",
                    hour=8,
                    minute=0,
                    id="footflow_pipeline"
                )
                logger.info("Scheduler gestart — pipeline draait elke dag om 08:00.")
                print("⏰ Scheduler actief — pipeline draait elke dag om 08:00. Druk Ctrl+C om te stoppen.")

            try:
                self.scheduler.start()
            except KeyboardInterrupt:
                logger.info("Scheduler gestopt door gebruiker.")
                self.scheduler.shutdown()
                print("\n⛔ Scheduler gestopt. Tot ziens!")

        except Exception as e:
            logger.error(f"Fout bij starten scheduler: {e}")

    def stop(self):
        try:
            self.scheduler.shutdown()
            logger.info("Scheduler gestopt.")
        except Exception as e:
            logger.error(f"Fout bij stoppen scheduler: {e}")
