# dashboard.py
# Dit bestand maakt een interactief dashboard met Streamlit.
# Het dashboard toont competitiestand, topscorers en wedstrijduitslagen.

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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
            query = """
            SELECT 
                t1.naam AS thuis_team,
                t2.naam AS uit_team,
                w.datum,
                w.uitslag
            FROM wedstrijden w
            JOIN teams t1 ON w.thuis_team_id = t1.team_id
            JOIN teams t2 ON w.uit_team_id = t2.team_id
            ORDER BY w.datum DESC
            LIMIT 10
            """
            resultaat = self.db.fetch_all(query)
            logger.info("Wedstrijden opgehaald voor dashboard.")
            return pd.DataFrame(resultaat)
        except Exception as e:
            logger.error(f"Fout bij ophalen wedstrijden: {e}")
            return pd.DataFrame()

    def haal_teams_op(self):
        """Haal alle teams op uit de database."""
        try:
            query = "SELECT naam, stad FROM teams ORDER BY naam"
            resultaat = self.db.fetch_all(query)
            logger.info("Teams opgehaald voor dashboard.")
            return pd.DataFrame(resultaat)
        except Exception as e:
            logger.error(f"Fout bij ophalen teams: {e}")
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
            st.dataframe(df_wedstrijden)
        else:
            st.warning("Geen wedstrijden beschikbaar.")

        st.markdown("---")

        # Sectie 2 — Teams overzicht
        st.header("🏟️ Teams Overzicht")
        df_teams = self.haal_teams_op()

        if not df_teams.empty:
            st.dataframe(df_teams)

            # Grafiek — aantal teams per stad
            fig, ax = plt.subplots()
            df_teams["stad"].value_counts().plot(kind="bar", ax=ax, color="steelblue")
            ax.set_title("Aantal teams per stad")
            ax.set_xlabel("Stad")
            ax.set_ylabel("Aantal teams")
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.warning("Geen teams beschikbaar.")

        st.markdown("---")
        st.caption("FootFlow Data Pipeline — MBO niveau 4 Eindproject")


def start_dashboard(db):
    """Start het Streamlit dashboard."""
    dashboard = Dashboard(db)
    dashboard.toon_dashboard()