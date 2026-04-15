from database import Database
from models import Competitie, Team, Wedstrijd, Speler
from collector import DataCollector
from csv_handler import CSVHandler
from scheduler import PipelineScheduler
from logger import get_logger

logger = get_logger(__name__)

def run_pipeline():
    logger.info("=== FootFlow Pipeline gestart ===")

    db = Database()
    verbinding = db.connect()

    if not verbinding:
        logger.error("Kan geen verbinding maken met de database. Pipeline gestopt.")
        return

    try:
        logger.info("Tabellen aanmaken...")
        Competitie.maak_tabel(db)
        Team.maak_tabel(db)
        Wedstrijd.maak_tabel(db)
        Speler.maak_tabel(db)
        logger.info("Tabellen aangemaakt!")

        logger.info("Stap 2: Data verzamelen via API...")
        collector = DataCollector(db)
        collector.verzamel_alles(competitie_code="PL", seizoen="2024")

        logger.info("Stap 3: CSV bestanden verwerken...")
        csv_handler = CSVHandler(data_map="../data")
        df_spelers = csv_handler.lees_csv("spelers.csv")

        if df_spelers is not None:
            verplicht = ["naam", "positie", "leeftijd", "team_naam"]
            if csv_handler.valideer_data(df_spelers, verplicht):

                df_spelers = df_spelers.dropna()

                opgeslagen = 0
                fouten = 0

                for _, rij in df_spelers.iterrows():
                    try:
                        resultaat = db.fetch_all(
                            "SELECT team_id FROM teams WHERE naam = %s",
                            (rij["team_naam"],)
                        )
                        if resultaat:
                            team_id = resultaat[0]["team_id"]
                            Speler.opslaan(
                                db,
                                naam=rij["naam"],
                                positie=rij["positie"],
                                leeftijd=int(rij["leeftijd"]),
                                team_id=team_id
                            )
                            opgeslagen += 1
                        else:
                            logger.warning(f"Team niet gevonden voor speler: {rij['naam']}")
                            fouten += 1
                    except Exception as e:
                        logger.error(f"Fout bij opslaan speler {rij['naam']}: {e}")
                        fouten += 1

                logger.info(f"Spelers verwerkt: {opgeslagen} opgeslagen, {fouten} fouten.")
            else:
                logger.error("CSV validatie mislukt — verplichte kolommen ontbreken.")
        else:
            logger.warning("Geen spelers CSV bestand gevonden.")

        logger.info("=== FootFlow Pipeline succesvol afgerond ===")

    except Exception as e:
        logger.error(f"Fout tijdens pipeline: {e}")

    finally:
        db.disconnect()


def main():
    print("⚽ Welkom bij FootFlow Data Pipeline!")
    print("1. Pipeline nu uitvoeren")
    print("2. Pipeline automatisch starten (elke dag 08:00)")

    keuze = input("Maak een keuze (1 of 2): ")

    if keuze == "1":
        run_pipeline()
    elif keuze == "2":
        scheduler = PipelineScheduler(run_pipeline)
        scheduler.start(test_modus=True)
    else:
        print("Ongeldige keuze. Probeer opnieuw.")


if __name__ == "__main__":
    main()