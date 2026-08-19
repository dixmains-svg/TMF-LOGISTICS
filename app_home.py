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


# ============================================================
# CSS ACCUEIL SÉCURISÉ (Fixe le problème d'écran blanc)
# ============================================================
def appliquer_style_accueil():
    background_css = "background-color: #f8fafc;"

    if BACKGROUND_PATH.exists():
        try:
            with open(BACKGROUND_PATH, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            background_css = f"""
            background-image: linear-gradient(rgba(255, 255, 255, 0.92), rgba(255, 255, 255, 0.92)), url("data:image/jpeg;base64,{encoded_image}");
            """
        except Exception:
            pass

    st.markdown(
        f"""
        <style>
        /* Force le fond et la couleur du texte principal */
        .stApp {{
            {background_css}
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: #1e293b !important;
        }}
        
        .main-title {{ 
            text-align: center; 
            font-size: 38px; 
            font-weight: 800; 
            color: #0f172a !important; 
            margin-top: 10px; 
        }}
        
        .main-subtitle {{ 
            text-align: center; 
            font-size: 18px; 
            color: #475569 !important; 
            margin-bottom: 25px; 
        }}
        
        .home-logo {{ text-align: center; margin-bottom: 15px; }}
        .home-logo img {{ width: 140px; max-width: 80%; height: auto; }}
        
        .footer {{ 
            text-align: center; 
            padding: 25px; 
            margin-top: 30px; 
            color: #64748b !important; 
            font-size: 14px; 
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# Application du style
appliquer_style_accueil()

# --- RESTE DU CONTENU DE L'ACCUEIL ---
df_om = lire_excel(FICHIER_OM)
df_camions = lire_excel(FICHIER_CAMIONS)
df_chauffeurs = lire_excel(FICHIER_CHAUFFEURS)
df_clients = lire_excel(FICHIER_CLIENTS)

# Logo
if LOGO_PATH.exists():
    try:
        with open(LOGO_PATH, "rb") as image_file:
            logo_base64 = base64.b64encode(image_file.read()).decode("utf-8")
        st.markdown(
            f'<div class="home-logo"><img src="data:image/png;base64,{logo_base64}"></div>',
            unsafe_allow_html=True,
        )
    except Exception:
        pass

st.markdown('<div class="main-title">🚛 TMF LOGISTICS</div>', unsafe_allow_html=True)
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

# Message de bienvenue
utilisateur = st.session_state.get("utilisateur", "Utilisateur")
st.header(f"Bienvenue, {utilisateur} 👋")
st.write("Bienvenue dans le système de gestion du transport de **TMF LOGISTICS**.")

st.subheader("📌 Modules de l'application")
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("### 📋 Ordres de Mission\nSuivi des ordres de mission et trajets.")
    st.markdown("### 🚚 Gestion du parc\nSuivi des véhicules et disponibilités.")
    st.markdown("### 👷 Gestion des Chauffeurs\nSuivi des chauffeurs et affectations.")

with col_b:
    st.markdown("### 👥 Gestion des Clients\nInformations clients et coordonnées.")
    st.markdown("### 📊 Rapports\nAnalyse des indicateurs de gestion.")
    st.markdown("### 🔄 Données actualisées\nLecture des fichiers du dossier **Data**.")

st.divider()

# État des fichiers
st.subheader("📁 État des données")
c1, c2, c3, c4 = st.columns(4)
c1.success("📋 OM.xlsx") if FICHIER_OM.exists() else c1.error("❌ OM.xlsx")
c2.success("🚚 Camions.xlsx") if FICHIER_CAMIONS.exists() else c2.error("❌ Camions.xlsx")
c3.success("👷 Chauffeurs.xlsx") if FICHIER_CHAUFFEURS.exists() else c3.error("❌ Chauffeurs.xlsx")
c4.success("👥 Clients.xlsx") if FICHIER_CLIENTS.exists() else c4.error("❌ Clients.xlsx")

st.divider()

if st.button("🔄 Actualiser les données", use_container_width=True):
    st.rerun()

st.markdown(
    '<div class="footer"><b>TMF LOGISTICS</b><br>Système de Gestion du Transport<br>Version 2.0</div>',
    unsafe_allow_html=True,
)
