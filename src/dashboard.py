# dashboard.py
# Dit bestand maakt een interactief dashboard met Streamlit.
# Het dashboard toont competitiestand, wedstrijduitslagen en spelers.

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

    def haal_alle_wedstrijden_op(self):
        """Haal alle gespeelde wedstrijden op uit de database."""
        try:
            query = (
                "SELECT t1.naam AS thuis_team, t2.naam AS uit_team, "
                "w.datum, w.uitslag "
                "FROM wedstrijden w "
                "JOIN teams t1 ON w.thuis_team_id = t1.team_id "
                "JOIN teams t2 ON w.uit_team_id = t2.team_id "
                "WHERE w.uitslag IS NOT NULL AND w.uitslag != '' "
                "ORDER BY w.datum DESC"
            )
            resultaat = self.db.fetch_all(query)
            logger.info("Wedstrijden opgehaald voor dashboard.")
            return pd.DataFrame(resultaat)
        except Exception as e:
            logger.error(f"Fout bij ophalen wedstrijden: {e}")
            return pd.DataFrame()

    def haal_teams_op(self):
        """Haal alle teamnamen op."""
        try:
            query = "SELECT naam FROM teams ORDER BY naam"
            resultaat = self.db.fetch_all(query)
            return [rij["naam"] for rij in resultaat]
        except Exception as e:
            logger.error(f"Fout bij ophalen teams: {e}")
            return []

    def haal_competitiestand_op(self):
        """Bereken de competitiestand op basis van wedstrijduitslagen."""
        try:
            query = (
                "SELECT t1.naam AS thuis_team, t2.naam AS uit_team, w.uitslag "
                "FROM wedstrijden w "
                "JOIN teams t1 ON w.thuis_team_id = t1.team_id "
                "JOIN teams t2 ON w.uit_team_id = t2.team_id "
                "WHERE w.uitslag IS NOT NULL AND w.uitslag != ''"
            )
            resultaat = self.db.fetch_all(query)
            df = pd.DataFrame(resultaat)

            if df.empty:
                return pd.DataFrame()

            stand = {}

            for _, rij in df.iterrows():
                try:
                    scores = rij["uitslag"].split("-")
                    thuis_goals = int(scores[0].strip())
                    uit_goals = int(scores[1].strip())
                except:
                    continue

                thuis = rij["thuis_team"]
                uit = rij["uit_team"]

                for team in [thuis, uit]:
                    if team not in stand:
                        stand[team] = {
                            "gespeeld": 0, "gewonnen": 0, "gelijk": 0,
                            "verloren": 0, "punten": 0,
                            "thuis_gewonnen": 0, "uit_gewonnen": 0
                        }

                stand[thuis]["gespeeld"] += 1
                stand[uit]["gespeeld"] += 1

                if thuis_goals > uit_goals:
                    stand[thuis]["gewonnen"] += 1
                    stand[thuis]["punten"] += 3
                    stand[thuis]["thuis_gewonnen"] += 1
                    stand[uit]["verloren"] += 1
                elif thuis_goals < uit_goals:
                    stand[uit]["gewonnen"] += 1
                    stand[uit]["punten"] += 3
                    stand[uit]["uit_gewonnen"] += 1
                    stand[thuis]["verloren"] += 1
                else:
                    stand[thuis]["gelijk"] += 1
                    stand[thuis]["punten"] += 1
                    stand[uit]["gelijk"] += 1
                    stand[uit]["punten"] += 1

            df_stand = pd.DataFrame(stand).T.reset_index()
            df_stand.columns = ["Team", "Gespeeld", "Gewonnen", "Gelijk", "Verloren", "Punten", "Thuis Gewonnen", "Uit Gewonnen"]
            df_stand = df_stand.sort_values("Punten", ascending=False).reset_index(drop=True)
            df_stand.index += 1

            logger.info("Competitiestand berekend.")
            return df_stand

        except Exception as e:
            logger.error(f"Fout bij berekenen competitiestand: {e}")
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
        st.set_page_config(page_title="FootFlow Dashboard", page_icon="⚽", layout="wide")

        st.title("⚽ FootFlow — Premier League Dashboard 2024")
        st.markdown("*Data pipeline gebouwd met Python, MySQL en Streamlit*")
        st.markdown("---")

        # Sectie 1 — Competitiestand
        st.header("🏆 Competitiestand")
        df_stand = self.haal_competitiestand_op()

        if not df_stand.empty:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Aantal teams", len(df_stand))
            with col2:
                st.metric("Koploper", df_stand.iloc[0]["Team"])
            with col3:
                st.metric("Punten koploper", int(df_stand.iloc[0]["Punten"]))

            st.markdown("")
            st.dataframe(df_stand[["Team", "Gespeeld", "Gewonnen", "Gelijk", "Verloren", "Punten"]], width="stretch")

            # Grafiek — Thuis vs Uit winst per team (top 10)
            st.subheader("🏠 Thuis vs Uit Gewonnen — Top 10 Teams")
            top10 = df_stand.head(10).copy()
            top10 = top10.sort_values("Thuis Gewonnen", ascending=True)

            fig, ax = plt.subplots(figsize=(12, 7))
            y = range(len(top10))
            breedte = 0.35

            ax.barh([i + breedte/2 for i in y], top10["Thuis Gewonnen"], breedte,
                   label="Thuis gewonnen", color="#2ecc71")
            ax.barh([i - breedte/2 for i in y], top10["Uit Gewonnen"], breedte,
                   label="Uit gewonnen", color="#3498db")

            ax.set_yticks(list(y))
            ax.set_yticklabels(top10["Team"].tolist())
            ax.set_xlabel("Aantal gewonnen wedstrijden")
            ax.set_title("Thuis vs Uit Gewonnen — Top 10 Teams", fontsize=14, fontweight="bold")
            ax.legend()
            plt.tight_layout()
            st.pyplot(fig)

        else:
            st.warning("Geen competitiedata beschikbaar.")

        st.markdown("---")

        # Sectie 2 — Wedstrijden met filter
        st.header("📋 Wedstrijden")
        df_alle_wedstrijden = self.haal_alle_wedstrijden_op()
        teams = self.haal_teams_op()

        if not df_alle_wedstrijden.empty:
            # Filter op team
            col1, col2 = st.columns([1, 3])
            with col1:
                gekozen_team = st.selectbox(
                    "🔍 Filter op team:",
                    ["Alle teams"] + teams
                )

            if gekozen_team == "Alle teams":
                df_gefilterd = df_alle_wedstrijden.head(10)
                st.caption("Laatste 10 wedstrijden")
            else:
                df_gefilterd = df_alle_wedstrijden[
                    (df_alle_wedstrijden["thuis_team"] == gekozen_team) |
                    (df_alle_wedstrijden["uit_team"] == gekozen_team)
                ]
                st.caption(f"Alle wedstrijden van {gekozen_team} — {len(df_gefilterd)} wedstrijden")

            st.dataframe(df_gefilterd, width="stretch")
        else:
            st.warning("Geen wedstrijden beschikbaar.")

        st.markdown("---")

        # Sectie 3 — Spelers overzicht
        st.header("👟 Spelers Overzicht")
        df_spelers = self.haal_spelers_op()

        if not df_spelers.empty:
            col1, col2 = st.columns([2, 1])

            with col1:
                st.dataframe(df_spelers, width="stretch")

            with col2:
                fig2, ax2 = plt.subplots()
                kleuren_pie = ["#2ecc71", "#3498db", "#e74c3c", "#f39c12"]
                df_spelers["positie"].value_counts().plot(
                    kind="pie", ax=ax2, autopct="%1.0f%%", colors=kleuren_pie
                )
                ax2.set_title("Spelers per positie")
                ax2.set_ylabel("")
                st.pyplot(fig2)
        else:
            st.warning("Geen spelers beschikbaar.")

        st.markdown("---")
        st.caption("FootFlow Data Pipeline — MBO niveau 4 Eindproject | Marouan")


# Start het dashboard direct als dit bestand wordt uitgevoerd
db = Database()
db.connect()
dashboard = Dashboard(db)
dashboard.toon_dashboard()