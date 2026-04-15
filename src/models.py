from logger import get_logger

logger = get_logger(__name__)

class Competitie:

    @staticmethod
    def maak_tabel(db):
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
        query = "INSERT IGNORE INTO competities (naam, land) VALUES (%s, %s)"
        db.execute_query(query, (naam, land))
        logger.info(f"Competitie opgeslagen: {naam}")


class Team:

    @staticmethod
    def maak_tabel(db):
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
        query = "INSERT IGNORE INTO teams (naam, stadion, competitie_id) VALUES (%s, %s, %s)"
        db.execute_query(query, (naam, stadion, competitie_id))
        logger.info(f"Team opgeslagen: {naam}")


class Wedstrijd:

    @staticmethod
    def maak_tabel(db):
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
        query = (
            "INSERT IGNORE INTO wedstrijden "
            "(seizoen_id, thuis_team_id, uit_team_id, datum, uitslag) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        db.execute_query(query, (seizoen_id, thuis_team_id, uit_team_id, datum, uitslag))
        logger.info(f"Wedstrijd opgeslagen: {datum}")


class Speler:

    @staticmethod
    def maak_tabel(db):
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
        query = (
            "INSERT IGNORE INTO spelers (naam, positie, leeftijd, team_id) "
            "VALUES (%s, %s, %s, %s)"
        )
        db.execute_query(query, (naam, positie, leeftijd, team_id))
        logger.info(f"Speler opgeslagen: {naam}")
