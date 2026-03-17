# collector.py
# Dit bestand verzamelt data via de API en slaat het op in de database.
# Dit is de kern van de data pipeline.

from api import FootballAPI
from models import Competitie, Team, Wedstrijd, Speler
from logger import get_logger

logger = get_logger(__name__)

class DataCollector:
    """
    Klasse voor het verzamelen en opslaan van voetbaldata.
    """

    def __init__(self, db):
        """Initialiseer de collector met een database verbinding."""
        self.db = db
        self.api = FootballAPI()

    def haal_team_id_op(self, teamnaam):
        """
        Zoek het database team_id op via de teamnaam.
        """
        try:
            resultaat = self.db.fetch_all(
                "SELECT team_id FROM teams WHERE naam = %s", (teamnaam,)
            )
            if resultaat:
                return resultaat[0]["team_id"]
            logger.warning(f"Team niet gevonden in database: {teamnaam}")
            return None
        except Exception as e:
            logger.error(f"Fout bij ophalen team_id: {e}")
            return None

    def verzamel_teams(self, competitie_code="PL", seizoen="2024"):
        """
        Haal teams op via de API en sla ze op in de database.
        """
        logger.info(f"Teams ophalen voor {competitie_code}...")
        data = self.api.get_teams(competitie_code, seizoen)

        if not data:
            logger.error("Geen teams data ontvangen.")
            return

        teams = data.get("teams", [])
        logger.info(f"{len(teams)} teams gevonden.")

        for team in teams:
            Team.opslaan(
                self.db,
                naam=team.get("name"),
                stadion=team.get("venue", "Onbekend"),
                competitie_id=1
            )

        logger.info("Alle teams opgeslagen in de database.")

    def verzamel_wedstrijden(self, competitie_code="PL", seizoen="2024"):
        """
        Haal wedstrijden op via de API en sla ze op in de database.
        Teams worden opgezocht via naam in plaats van API ID.
        """
        logger.info(f"Wedstrijden ophalen voor {competitie_code} seizoen {seizoen}...")
        data = self.api.get_wedstrijden(competitie_code, seizoen)

        if not data:
            logger.error("Geen wedstrijden data ontvangen.")
            return

        wedstrijden = data.get("matches", [])
        logger.info(f"{len(wedstrijden)} wedstrijden gevonden.")

        opgeslagen = 0
        overgeslagen = 0

        for wedstrijd in wedstrijden:
            # Haal teamnamen op uit de API
            thuis_naam = wedstrijd.get("homeTeam", {}).get("name")
            uit_naam = wedstrijd.get("awayTeam", {}).get("name")

            # Zoek de database ID's op via teamnaam
            thuis_team_id = self.haal_team_id_op(thuis_naam)
            uit_team_id = self.haal_team_id_op(uit_naam)

            # Sla over als team niet gevonden
            if not thuis_team_id or not uit_team_id:
                logger.warning(f"Team niet gevonden, wedstrijd overgeslagen: {thuis_naam} vs {uit_naam}")
                overgeslagen += 1
                continue

            # Haal de uitslag op
            score = wedstrijd.get("score", {})
            fulltime = score.get("fullTime", {})
            thuis = fulltime.get("home")
            uit = fulltime.get("away")
            uitslag = f"{thuis}-{uit}" if thuis is not None else "Nog niet gespeeld"

            Wedstrijd.opslaan(
                self.db,
                seizoen_id=1,
                thuis_team_id=thuis_team_id,
                uit_team_id=uit_team_id,
                datum=wedstrijd.get("utcDate", "")[:10],
                uitslag=uitslag
            )
            opgeslagen += 1

        logger.info(f"{opgeslagen} wedstrijden opgeslagen, {overgeslagen} overgeslagen.")

    def verzamel_alles(self, competitie_code="PL", seizoen="2024"):
        """
        Verzamel alle data — competitie, teams en wedstrijden.
        """
        logger.info("Start verzamelen van alle data...")

        # Eerst competitie opslaan zodat teams een competitie_id hebben
        logger.info("Competitie opslaan...")
        Competitie.opslaan(self.db, naam="Premier League", land="England")

        self.verzamel_teams(competitie_code, seizoen)
        self.verzamel_wedstrijden(competitie_code, seizoen)
        logger.info("Alle data verzameld!")