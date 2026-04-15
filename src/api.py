import requests
import os
from dotenv import load_dotenv
from logger import get_logger

load_dotenv()

logger = get_logger(__name__)

class FootballAPI:

    BASE_URL = "https://api.football-data.org/v4"

    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.headers = {"X-Auth-Token": self.api_key}

    def get_wedstrijden(self, competitie_code="PL", seizoen="2024"):
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