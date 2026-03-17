# main.py
# Dit is het hoofdbestand van de FootFlow data pipeline.
# Het start de pipeline en verbindt alle onderdelen met elkaar.

from database import Database
from models import Competitie, Team, Wedstrijd, Speler
from collector import DataCollector
from transformer import DataTransformer
from csv_handler import CSVHandler
from scheduler import PipelineScheduler
from logger import get_logger

logger = get_logger(__name__)

def run_pipeline():
    """
    Voer de volledige data pipeline uit:
    1. Verbinding maken met database
    2. Tabellen aanmaken als ze nog niet bestaan
    3. Data verzamelen via API
    4. Data opschonen en transformeren
    5. CSV bestanden verwerken
    6. Database bijwerken
    """
    logger.info("=== FootFlow Pipeline gestart ===")

    # Stap 1 — Verbinding maken met database
    db = Database()
    verbinding = db.connect()

    if not verbinding:
        logger.error("Kan geen verbinding maken met de database. Pipeline gestopt.")
        return

    try:
        # Stap 1b — Tabellen aanmaken als ze nog niet bestaan
        logger.info("Tabellen aanmaken...")
        Competitie.maak_tabel(db)
        Team.maak_tabel(db)
        Wedstrijd.maak_tabel(db)
        Speler.maak_tabel(db)
        logger.info("Tabellen aangemaakt!")

        # Stap 2 — Data verzamelen via API
        logger.info("Stap 2: Data verzamelen via API...")
        collector = DataCollector(db)
        collector.verzamel_alles(competitie_code="PL", seizoen="2024")

        # Stap 3 — Data opschonen en transformeren
        logger.info("Stap 3: Data transformeren...")
        transformer = DataTransformer()

        # Stap 4 — CSV bestanden verwerken
        logger.info("Stap 4: CSV bestanden verwerken...")
        csv_handler = CSVHandler(data_map="data")

        logger.info("=== FootFlow Pipeline succesvol afgerond ===")

    except Exception as e:
        logger.error(f"Fout tijdens pipeline: {e}")

    finally:
        # Altijd de database verbinding verbreken
        db.disconnect()


def main():
    """
    Start de FootFlow applicatie.
    Kies tussen direct uitvoeren of automatisch via scheduler.
    """
    print("⚽ Welkom bij FootFlow Data Pipeline!")
    print("1. Pipeline nu uitvoeren")
    print("2. Pipeline automatisch starten (elke dag 08:00)")

    keuze = input("Maak een keuze (1 of 2): ")

    if keuze == "1":
        run_pipeline()
    elif keuze == "2":
        scheduler = PipelineScheduler(run_pipeline)
        scheduler.start()
    else:
        print("Ongeldige keuze. Probeer opnieuw.")


if __name__ == "__main__":
    main()