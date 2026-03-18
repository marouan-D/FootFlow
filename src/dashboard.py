# dashboard.py
# Dit bestand maakt een interactief dashboard met Streamlit.
# Het dashboard toont competitiestand, topscorers en wedstrijduitslagen.

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Zorg dat de src map gevonden wordt
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import Database
from logger import get_logger

logger = get_logger(__name__)

class Dashboard:
    """
    Klasse voor het weergeven van voetbaldata in een dashboard.
    """

    def __init__(self, db):
        """Initialiseer het dashboard met een database verbinding."""
        self.db = db

    def haal_wedstrijden_op(self):
        """Haal de laatste 10 wedstrijden op uit de database."""
        try:
            query = (
                "SELECT t1.naam AS thuis_team, t2.naam AS uit_team, "
                "w.datum, w.uitslag "
                "FROM wedstrijden w "
                "JOIN teams t1 ON w.thuis_team_id = t1.team_id "
                "JOIN teams t2 ON w.uit_team_id = t2.team_id "
                "ORDER BY w.datum DESC LIMIT 10"
            )
            resultaat = self.db.fetch_all(query)
            logger.info("Wedstrijden opgehaald voor dashboard.")
            return pd.DataFrame(resultaat)
        except Exception as e:
            logger.error(f"Fout bij ophalen wedstrijden: {e}")
            return pd.DataFrame()

    def haal_teams_op(self):
        """Haal alle teams op uit de database."""
        try:
            query = "SELECT naam, stadion FROM teams ORDER BY naam"
            resultaat = self.db.fetch_all(query)
            logger.info("Teams opgehaald voor dashboard.")
            return pd.DataFrame(resultaat)
        except Exception as e:
            logger.error(f"Fout bij ophalen teams: {e}")
            return pd.DataFrame()

    def haal_spelers_op(self):
        """Haal alle spelers op uit de database."""
        try:
            query = (
                "SELECT s.naam, s.positie, s.leeftijd, t.naam AS team "
                "FROM spelers s "
                "JOIN teams t ON s.team_id = t.team_id "
                "ORDER BY s.naam"
            )
            resultaat = self.db.fetch_all(query)
            logger.info("Spelers opgehaald voor dashboard.")
            return pd.DataFrame(resultaat)
        except Exception as e:
            logger.error(f"Fout bij ophalen spelers: {e}")
            return pd.DataFrame()

    def toon_dashboard(self):
        """
        Toon het Streamlit dashboard met alle visualisaties.
        """
        st.title("⚽ FootFlow — Voetbal Data Dashboard")
        st.markdown("---")

        # Sectie 1 — Laatste wedstrijden
        st.header("📋 Laatste Wedstrijden")
        df_wedstrijden = self.haal_wedstrijden_op()

        if not df_wedstrijden.empty:
            st.dataframe(df_wedstrijden, width="stretch")
        else:
            st.warning("Geen wedstrijden beschikbaar.")

        st.markdown("---")

        # Sectie 2 — Teams overzicht
        st.header("🏟️ Teams Overzicht")
        df_teams = self.haal_teams_op()

        if not df_teams.empty:
            st.dataframe(df_teams, width="stretch")

            # Grafiek — Premier League teams horizontaal
            fig, ax = plt.subplots(figsize=(10, 8))
            ax.barh(df_teams["naam"], range(len(df_teams)), color="steelblue")
            ax.set_title("Premier League Teams 2024")
            ax.set_xlabel("Index")
            ax.set_ylabel("Team")
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.warning("Geen teams beschikbaar.")

        st.markdown("---")

        # Sectie 3 — Spelers overzicht
        st.header("👟 Spelers Overzicht")
        df_spelers = self.haal_spelers_op()

        if not df_spelers.empty:
            st.dataframe(df_spelers, width="stretch")

            # Grafiek — spelers per positie
            fig2, ax2 = plt.subplots()
            df_spelers["positie"].value_counts().plot(
                kind="pie", ax=ax2, autopct="%1.0f%%"
            )
            ax2.set_title("Spelers per positie")
            ax2.set_ylabel("")
            st.pyplot(fig2)
        else:
            st.warning("Geen spelers beschikbaar.")

        st.markdown("---")
        st.caption("FootFlow Data Pipeline — MBO niveau 4 Eindproject")


# Start het dashboard direct als dit bestand wordt uitgevoerd
db = Database()
db.connect()
dashboard = Dashboard(db)
dashboard.toon_dashboard()