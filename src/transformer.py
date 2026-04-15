import pandas as pd
from logger import get_logger

logger = get_logger(__name__)

class DataTransformer:

    def schoon_wedstrijden(self, wedstrijden):
        try:
            if not wedstrijden:
                logger.warning("Geen wedstrijden om op te schonen.")
                return None

            df = pd.DataFrame(wedstrijden)
            df.dropna(subset=["datum", "uitslag"], inplace=True)
            df["datum"] = pd.to_datetime(df["datum"])
            df.drop_duplicates(inplace=True)

            logger.info(f"Wedstrijddata opgeschoond: {len(df)} rijen over.")
            return df

        except Exception as e:
            logger.error(f"Fout bij opschonen wedstrijden: {e}")
            return None

    def schoon_teams(self, teams):
        try:
            if not teams:
                logger.warning("Geen teams om op te schonen.")
                return None

            df = pd.DataFrame(teams)
            df.dropna(subset=["naam"], inplace=True)
            df.drop_duplicates(subset=["naam"], inplace=True)
            df.columns = df.columns.str.lower()

            logger.info(f"Teamdata opgeschoond: {len(df)} rijen over.")
            return df

        except Exception as e:
            logger.error(f"Fout bij opschonen teams: {e}")
            return None
