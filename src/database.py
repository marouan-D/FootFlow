import mysql.connector
import os
from dotenv import load_dotenv
from logger import get_logger

load_dotenv()

logger = get_logger(__name__)

class Database:

    def __init__(self):
        self.connection = None

    def connect(self):
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
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Verbinding met database verbroken.")

    def execute_query(self, query, params=None):
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
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except mysql.connector.Error as e:
            logger.error(f"Fout bij ophalen data: {e}")
            return []
