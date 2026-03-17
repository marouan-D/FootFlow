# database.py
# Dit bestand beheert de verbinding met de MySQL database.
# De verbindingsgegevens worden opgehaald uit het .env bestand.

import mysql.connector
import os
from dotenv import load_dotenv
from logger import get_logger

# Laad de omgevingsvariabelen uit .env
load_dotenv()

# Maak een logger aan
logger = get_logger(__name__)

class Database:
    """
    Klasse voor het beheren van de MySQL database verbinding.
    """

    def __init__(self):
        """Initialiseer de database verbinding."""
        self.connection = None

    def connect(self):
        """
        Maak verbinding met de MySQL database.
        Gegevens worden opgehaald uit het .env bestand.
        """
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
            logger.info("Verbinding met database succesvol!")
            return self.connection
        except mysql.connector.Error as e:
            logger.error(f"Fout bij verbinden met database: {e}")
            return None

    def disconnect(self):
        """Verbreek de verbinding met de database."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Verbinding met database verbroken.")

    def execute_query(self, query, params=None):
        """
        Voer een SQL query uit op de database.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            logger.info(f"Query succesvol uitgevoerd.")
            return cursor
        except mysql.connector.Error as e:
            logger.error(f"Fout bij uitvoeren query: {e}")
            return None

    def fetch_all(self, query, params=None):
        """
        Haal alle resultaten op van een SELECT query.
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except mysql.connector.Error as e:
            logger.error(f"Fout bij ophalen data: {e}")
            return []