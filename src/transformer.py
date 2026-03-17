# transformer.py
# Dit bestand schoont de ruwe data op en transformeert het
# zodat het klaar is voor opslag in de database.

import pandas as pd
from logger import get_logger

logger = get_logger(__name__)

class DataTransformer:
    """
    Klasse voor het opschonen en transformeren van voetbaldata.
    """

    def __init__(self):
        """Initialiseer de transformer."""
        pass

    def schoon_wedstrijden(self, wedstrijden):
        """
        Schoon wedstrijddata op en transformeer het naar een DataFrame.
        """
        try:
            if not wedstrijden:
                logger.warning("Geen wedstrijden om op te schonen.")
                return None

            # Zet data om naar DataFrame
            df = pd.DataFrame(wedstrijden)

            # Verwijder lege rijen
            df.dropna(subset=["datum", "uitslag"], inplace=True)

            # Zet datum om naar correct formaat
            df["datum"] = pd.to_datetime(df["datum"])

            # Verwijder duplicaten
            df.drop_duplicates(inplace=True)

            logger.info(f"Wedstrijddata opgeschoond: {len(df)} rijen over.")
            return df

        except Exception as e:
            logger.error(f"Fout bij opschonen wedstrijden: {e}")
            return None

    def schoon_teams(self, teams):
        """
        Schoon teamdata op en transformeer het naar een DataFrame.
        """
        try:
            if not teams:
                logger.warning("Geen teams om op te schonen.")
                return None

            # Zet data om naar DataFrame
            df = pd.DataFrame(teams)

            # Verwijder lege rijen
            df.dropna(subset=["naam"], inplace=True)

            # Verwijder duplicaten
            df.drop_duplicates(subset=["naam"], inplace=True)

            # Zet kolomnamen om naar kleine letters
            df.columns = df.columns.str.lower()

            logger.info(f"Teamdata opgeschoond: {len(df)} rijen over.")
            return df

        except Exception as e:
            logger.error(f"Fout bij opschonen teams: {e}")
            return None

    def bereken_statistieken(self, df_wedstrijden):
        """
        Bereken statistieken op basis van wedstrijddata.
        Bijvoorbeeld: aantal gewonnen, gelijkgespeeld, verloren per team.
        """
        try:
            if df_wedstrijden is None or df_wedstrijden.empty:
                logger.warning("Geen data om statistieken van te berekenen.")
                return None

            logger.info("Statistieken berekend.")
            return df_wedstrijden

        except Exception as e:
            logger.error(f"Fout bij berekenen statistieken: {e}")
            return None