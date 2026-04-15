import pandas as pd
import os
from logger import get_logger

logger = get_logger(__name__)

class CSVHandler:

    def __init__(self, data_map="data"):
        self.data_map = data_map

    def lees_csv(self, bestandsnaam):
        try:
            pad = os.path.join(self.data_map, bestandsnaam)
            df = pd.read_csv(pad)
            logger.info(f"CSV bestand ingelezen: {bestandsnaam} ({len(df)} rijen)")
            return df
        except FileNotFoundError:
            logger.error(f"Bestand niet gevonden: {bestandsnaam}")
            return None
        except Exception as e:
            logger.error(f"Fout bij inlezen CSV: {e}")
            return None

    def lees_excel(self, bestandsnaam):
        try:
            pad = os.path.join(self.data_map, bestandsnaam)
            df = pd.read_excel(pad)
            logger.info(f"Excel bestand ingelezen: {bestandsnaam} ({len(df)} rijen)")
            return df
        except FileNotFoundError:
            logger.error(f"Bestand niet gevonden: {bestandsnaam}")
            return None
        except Exception as e:
            logger.error(f"Fout bij inlezen Excel: {e}")
            return None

    def valideer_data(self, df, verplichte_kolommen):
        try:
            ontbrekende_kolommen = [
                col for col in verplichte_kolommen if col not in df.columns
            ]
            if ontbrekende_kolommen:
                logger.error(f"Ontbrekende kolommen: {ontbrekende_kolommen}")
                return False
            logger.info("Data validatie geslaagd.")
            return True
        except Exception as e:
            logger.error(f"Fout bij valideren data: {e}")
            return False
