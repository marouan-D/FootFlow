# api.py
# Dit bestand beheert de verbinding met de football-data.org API.
# De API sleutel wordt opgehaald uit het .env bestand.

import requests
import os
from dotenv import load_dotenv
from logger import get_logger

# Laad de omgevingsvariabelen uit .env
load_dotenv()

logger = get_logger(__name__)

class FootballAPI:
    """
    Klasse voor het ophalen van voetbaldata via de football-data.org API.
    """

    BASE_URL = "https://api.football-data.org/v4"

    def __init__(self):
        """Initialiseer de API met de sleutel uit het .env bestand."""
        self.api_key = os.getenv("API_KEY")
        self.headers = {"X-Auth-Token": self.api_key}

    def get_competities(self):
        """Haal alle beschikbare competities op via de API."""
        try:
            url = f"{self.BASE_URL}/competitions"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            logger.info("Competities succesvol opgehaald.")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Fout bij ophalen competities: {e}")
            return None

    def get_wedstrijden(self, competitie_code="PL", seizoen="2024"):
        """
        Haal wedstrijden op voor een specifieke competitie en seizoen.
        Standaard: Premier League 2024
        """
        try:
            url = f"{self.BASE_URL}/competitions/{competitie_code}/matches"
            params = {"season": seizoen}
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            logger.info(f"Wedstrijden opgehaald voor {competitie_code} seizoen {seizoen}.")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Fout bij ophalen wedstrijden: {e}")
            return None

    def get_teams(self, competitie_code="PL", seizoen="2024"):
        """
        Haal teams op voor een specifieke competitie en seizoen.
        Standaard: Premier League 2024
        """
        try:
            url = f"{self.BASE_URL}/competitions/{competitie_code}/teams"
            params = {"season": seizoen}
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            logger.info(f"Teams opgehaald voor {competitie_code} seizoen {seizoen}.")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Fout bij ophalen teams: {e}")
            return None

    def get_standen(self, competitie_code="PL"):
        """
        Haal de competitiestand op.
        Standaard: Premier League
        """
        try:
            url = f"{self.BASE_URL}/competitions/{competitie_code}/standings"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            logger.info(f"Standen opgehaald voor {competitie_code}.")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Fout bij ophalen standen: {e}")
            return None