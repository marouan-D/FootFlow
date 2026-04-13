# test_pipeline.py
# Geautomatiseerde testen voor de FootFlow data pipeline.
# Voer uit met: pytest test_pipeline.py -v

import pytest
import pandas as pd
import sys
import os
from unittest.mock import MagicMock, patch
import requests
import mysql.connector

# Zorg dat de src map gevonden wordt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from transformer import DataTransformer
from csv_handler import CSVHandler


# ============================================================
# US-01: API connectie — testen voor FootballAPI
# ============================================================

def test_api_geeft_none_bij_verbindingsfout():
    """
    Test dat de API None teruggeeft bij een verbindingsfout.
    Gerelateerd aan: US-01
    """
    from api import FootballAPI
    api = FootballAPI()
    with patch('requests.get', side_effect=requests.exceptions.RequestException("Verbinding mislukt")):
        resultaat = api.get_wedstrijden()
        assert resultaat is None


# ============================================================
# US-02: Data transformatie — testen voor DataTransformer
# ============================================================

def test_transformer_schoon_wedstrijden_verwijdert_lege_rijen():
    """
    Test dat schoon_wedstrijden lege rijen verwijdert.
    Gerelateerd aan: US-02
    """
    transformer = DataTransformer()
    wedstrijden = [
        {"datum": "2024-08-16", "uitslag": "2-1"},
        {"datum": None, "uitslag": None},
        {"datum": "2024-08-17", "uitslag": "0-0"},
    ]
    resultaat = transformer.schoon_wedstrijden(wedstrijden)
    assert len(resultaat) == 2


def test_transformer_schoon_wedstrijden_lege_lijst():
    """
    Test dat schoon_wedstrijden None teruggeeft bij een lege lijst.
    Gerelateerd aan: US-02
    """
    transformer = DataTransformer()
    resultaat = transformer.schoon_wedstrijden([])
    assert resultaat is None


def test_transformer_schoon_teams_verwijdert_duplicaten():
    """
    Test dat schoon_teams duplicaten verwijdert.
    Gerelateerd aan: US-02
    """
    transformer = DataTransformer()
    teams = [
        {"naam": "Arsenal FC", "stadion": "Emirates"},
        {"naam": "Arsenal FC", "stadion": "Emirates"},
        {"naam": "Chelsea FC", "stadion": "Stamford Bridge"},
    ]
    resultaat = transformer.schoon_teams(teams)
    assert len(resultaat) == 2


# ============================================================
# US-03: Database — testen voor de Database klasse
# ============================================================

def test_database_verbinding_mislukt_zonder_env():
    """
    Test dat de database verbinding None teruggeeft bij een fout.
    Gerelateerd aan: US-03
    """
    from database import Database
    with patch('mysql.connector.connect', side_effect=mysql.connector.Error("Verbinding mislukt")):
        db = Database()
        resultaat = db.connect()
        assert resultaat is None


def test_database_fetch_all_geeft_lege_lijst_bij_fout():
    """
    Test dat fetch_all een lege lijst teruggeeft bij een fout.
    Gerelateerd aan: US-03
    """
    from database import Database
    db = Database()
    db.connection = MagicMock()
    db.connection.cursor.side_effect = mysql.connector.Error("Query mislukt")
    resultaat = db.fetch_all("SELECT * FROM teams")
    assert resultaat == []


# ============================================================
# US-04: CSV verwerking — testen voor CSVHandler
# ============================================================

def test_csv_handler_bestand_niet_gevonden():
    """
    Test dat lees_csv None teruggeeft als het bestand niet bestaat.
    Gerelateerd aan: US-04
    """
    handler = CSVHandler(data_map="../data")
    resultaat = handler.lees_csv("bestaat_niet.csv")
    assert resultaat is None


def test_csv_handler_valideer_data_geslaagd():
    """
    Test dat valideer_data True teruggeeft als alle kolommen aanwezig zijn.
    Gerelateerd aan: US-04
    """
    handler = CSVHandler()
    df = pd.DataFrame({
        "naam": ["Mohamed Salah"],
        "positie": ["Aanvaller"],
        "leeftijd": [32],
        "team_naam": ["Liverpool FC"]
    })
    resultaat = handler.valideer_data(df, ["naam", "positie", "leeftijd", "team_naam"])
    assert resultaat == True


def test_csv_handler_valideer_data_mislukt():
    """
    Test dat valideer_data False teruggeeft als een kolom ontbreekt.
    Gerelateerd aan: US-04
    """
    handler = CSVHandler()
    df = pd.DataFrame({
        "naam": ["Mohamed Salah"],
        "positie": ["Aanvaller"]
    })
    resultaat = handler.valideer_data(df, ["naam", "positie", "leeftijd", "team_naam"])
    assert resultaat == False


# ============================================================
# US-07: Foutafhandeling — testen voor foutafhandeling
# ============================================================

def test_transformer_schoon_teams_lege_lijst():
    """
    Test dat schoon_teams None teruggeeft bij een lege lijst.
    Gerelateerd aan: US-07
    """
    transformer = DataTransformer()
    resultaat = transformer.schoon_teams([])
    assert resultaat is None


def test_csv_handler_valideer_data_lege_dataframe():
    """
    Test dat valideer_data False teruggeeft bij een lege DataFrame.
    Gerelateerd aan: US-07
    """
    handler = CSVHandler()
    df = pd.DataFrame()
    resultaat = handler.valideer_data(df, ["naam", "positie"])
    assert resultaat == False