import base64
from pathlib import Path
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "Data"
LOGO_PATH = BASE_DIR / "logo.png"
BACKGROUND_PATH = BASE_DIR / "TMF.jpg"

FICHIER_OM = DATA_DIR / "OM.xlsx"
FICHIER_CAMIONS = DATA_DIR / "Camions.xlsx"
FICHIER_CHAUFFEURS = DATA_DIR / "Chauffeurs.xlsx"
FICHIER_CLIENTS = DATA_DIR / "Clients.xlsx"


def lire_excel(fichier):
    if not fichier.exists():
        return pd.DataFrame()
    try:
        df = pd.read_excel(fichier, engine="openpyxl")
        df.columns = df.columns.astype(str).str.strip()
        return df.dropna(how="all")
    except Exception:
        return pd.DataFrame()


def afficher_home():
    """Affiche le contenu du tableau de bord d'accueil."""
    # Bouton de déconnexion dans la barre latérale
    st.sidebar.divider()
    utilisateur = st.session_state.get("utilisateur", "")
    st.sidebar.markdown(f"### 👤 Utilisateur\n**{utilisateur}**")

    if st.sidebar.button("🚪 Déconnexion", use_container_width=True):
        st.session_state.connecte = False
        st.session_state.pop("utilisateur", None)
        st.session_state.pop("login_error", None)
        st.rerun()

    # Style
    if BACKGROUND_PATH.exists():
        try:
            with open(BACKGROUND_PATH, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode(
                    "utf-8"
                )
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: linear-gradient(rgba(255,255,255,0.88), rgba(255,255,255,0.88)), url("data:image/jpeg;base64,{encoded_image}");
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
                .main-title {{ text-align: center; font-size: 38px; font-weight: 800; margin-top: 10px; }}
                .main-subtitle {{ text-align: center; font-size: 18px; color: #555; margin-bottom: 25px; }}
                .home-logo {{ text-align: center; margin-bottom: 5px; }}
                .home-logo img {{ width: 150px; max-width: 80%; height: auto; }}
                .footer {{ text-align: center; padding: 25px; margin-top: 30px; color: #666; font-size: 14px; }}
                </style>
                """,
                unsafe_allow_html=True,
            )
        except Exception:
            pass

    # Données
    df_om = lire_excel(FICHIER_OM)
    df_camions = lire_excel(FICHIER_CAMIONS)
    df_chauffeurs = lire_excel(FICHIER_CHAUFFEURS)
    df_clients = lire_excel(FICHIER_CLIENTS)

    # Logo
    if LOGO_PATH.exists():
        try:
            with open(LOGO_PATH, "rb") as image_file:
                logo_base64 = base64.b64encode(image_file.read()).decode(
                    "utf-8"
                )
            st.markdown(
                f'<div class="home-logo"><img src="data:image/png;base64,{logo_base64}"></div>',
                unsafe_allow_html=True,
            )
        except Exception:
            pass

    # Titre
    st.markdown(
        '<div class="main-title">🚛 TMF LOGISTICS</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="main-subtitle">Système de Gestion du Transport et des Ordres de Mission</div>',
        unsafe_allow_html=True,
    )
    st.divider()

    # Métriques
    st.header("📊 Tableau de bord")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📋 Ordres de Mission", len(df_om))
    col2.metric("🚚 Camions", len(df_camions))
    col3.metric("👷 Chauffeurs", len(df_chauffeurs))
    col4.metric("👥 Clients", len(df_clients))

    st.divider()
    st.header(f"Bienvenue, {utilisateur} 👋")
    st.write(
        "Bienvenue dans le système de gestion du transport de **TMF LOGISTICS**."
    )
