# models.py
# Dit bestand bevat de database modellen voor FootFlow.
# Elk model stelt een tabel voor in de MySQL database.

from database import Database
from logger import get_logger

logger = get_logger(__name__)

class Competitie:
    """Model voor de Competitie tabel."""

    def __init__(self, naam, land):
        self.naam = naam
        self.land = land

    @staticmethod
    def maak_tabel(db):
        """Maak de Competitie tabel aan als deze nog niet bestaat."""
        query = (
            "CREATE TABLE IF NOT EXISTS competities ("
            "competitie_id INT AUTO_INCREMENT PRIMARY KEY, "
            "naam VARCHAR(100) NOT NULL, "
            "land VARCHAR(100) NOT NULL"
            ")"
        )
        db.execute_query(query)
        logger.info("Tabel 'competities' aangemaakt of bestaat al.")

    @staticmethod
    def opslaan(db, naam, land):
        """Sla een competitie op in de database."""
        query = "INSERT IGNORE INTO competities (naam, land) VALUES (%s, %s)"
        db.execute_query(query, (naam, land))
        logger.info(f"Competitie opgeslagen: {naam}")


class Team:
    """Model voor de Team tabel."""

    def __init__(self, naam, stadion, competitie_id):
        self.naam = naam
        self.stadion = stadion
        self.competitie_id = competitie_id

    @staticmethod
    def maak_tabel(db):
        """Maak de Team tabel aan als deze nog niet bestaat."""
        query = (
            "CREATE TABLE IF NOT EXISTS teams ("
            "team_id INT AUTO_INCREMENT PRIMARY KEY, "
            "competitie_id INT, "
            "naam VARCHAR(100) NOT NULL, "
            "stadion VARCHAR(100), "
            "FOREIGN KEY (competitie_id) REFERENCES competities(competitie_id)"
            ")"
        )
        db.execute_query(query)
        logger.info("Tabel 'teams' aangemaakt of bestaat al.")

    @staticmethod
    def opslaan(db, naam, stadion, competitie_id):
        """Sla een team op in de database."""
        query = "INSERT IGNORE INTO teams (naam, stadion, competitie_id) VALUES (%s, %s, %s)"
        db.execute_query(query, (naam, stadion, competitie_id))
        logger.info(f"Team opgeslagen: {naam}")


class Wedstrijd:
    """Model voor de Wedstrijd tabel."""

    def __init__(self, seizoen_id, thuis_team_id, uit_team_id, datum, uitslag):
        self.seizoen_id = seizoen_id
        self.thuis_team_id = thuis_team_id
        self.uit_team_id = uit_team_id
        self.datum = datum
        self.uitslag = uitslag

    @staticmethod
    def maak_tabel(db):
        """Maak de Wedstrijd tabel aan als deze nog niet bestaat."""
        query = (
            "CREATE TABLE IF NOT EXISTS wedstrijden ("
            "wedstrijd_id INT AUTO_INCREMENT PRIMARY KEY, "
            "seizoen_id INT, "
            "thuis_team_id INT, "
            "uit_team_id INT, "
            "datum DATE, "
            "uitslag VARCHAR(10), "
            "FOREIGN KEY (thuis_team_id) REFERENCES teams(team_id), "
            "FOREIGN KEY (uit_team_id) REFERENCES teams(team_id)"
            ")"
        )
        db.execute_query(query)
        logger.info("Tabel 'wedstrijden' aangemaakt of bestaat al.")

    @staticmethod
    def opslaan(db, seizoen_id, thuis_team_id, uit_team_id, datum, uitslag):
        """Sla een wedstrijd op in de database."""
        query = (
            "INSERT IGNORE INTO wedstrijden "
            "(seizoen_id, thuis_team_id, uit_team_id, datum, uitslag) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        db.execute_query(query, (seizoen_id, thuis_team_id, uit_team_id, datum, uitslag))
        logger.info(f"Wedstrijd opgeslagen: {datum}")


class Speler:
    """Model voor de Speler tabel."""

    def __init__(self, naam, positie, leeftijd, team_id):
        self.naam = naam
        self.positie = positie
        self.leeftijd = leeftijd
        self.team_id = team_id

    @staticmethod
    def maak_tabel(db):
        """Maak de Speler tabel aan als deze nog niet bestaat."""
        query = (
            "CREATE TABLE IF NOT EXISTS spelers ("
            "speler_id INT AUTO_INCREMENT PRIMARY KEY, "
            "team_id INT, "
            "naam VARCHAR(100) NOT NULL, "
            "positie VARCHAR(50), "
            "leeftijd INT, "
            "FOREIGN KEY (team_id) REFERENCES teams(team_id)"
            ")"
        )
        db.execute_query(query)
        logger.info("Tabel 'spelers' aangemaakt of bestaat al.")

    @staticmethod
    def opslaan(db, naam, positie, leeftijd, team_id):
        """Sla een speler op in de database."""
        query = (
            "INSERT IGNORE INTO spelers (naam, positie, leeftijd, team_id) "
            "VALUES (%s, %s, %s, %s)"
        )
        db.execute_query(query, (naam, positie, leeftijd, team_id))
        logger.info(f"Speler opgeslagen: {naam}")