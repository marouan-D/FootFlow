# csv_handler.py
# Dit bestand leest CSV/Excel bestanden in en verwerkt de data.
# De verwerkte data wordt opgeslagen in de MySQL database.

import pandas as pd
import os
from logger import get_logger

logger = get_logger(__name__)

class CSVHandler:
    """
    Klasse voor het inlezen en verwerken van CSV en Excel bestanden.
    """

    def __init__(self, data_map="data"):
        """Initialiseer de handler met het pad naar de data map."""
        self.data_map = data_map

    def lees_csv(self, bestandsnaam):
        """
        Lees een CSV bestand in vanuit de data map.
        """
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
        """
        Lees een Excel bestand in vanuit de data map.
        """
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
        """
        Valideer of de verplichte kolommen aanwezig zijn in het DataFrame.
        """
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

    def sla_op_in_database(self, db, df, tabel):
        """
        Sla een DataFrame op in de database.
        Foutieve rijen worden gelogd en overgeslagen.
        """
        opgeslagen = 0
        fouten = 0

        for _, rij in df.iterrows():
            try:
                kolommen = ", ".join(rij.index)
                waarden = tuple(rij.values)
                placeholders = ", ".join(["%s"] * len(waarden))
                query = f"INSERT IGNORE INTO {tabel} ({kolommen}) VALUES ({placeholders})"
                db.execute_query(query, waarden)
                opgeslagen += 1
            except Exception as e:
                logger.error(f"Fout bij opslaan rij: {e}")
                fouten += 1

        logger.info(f"{opgeslagen} rijen opgeslagen, {fouten} fouten.")