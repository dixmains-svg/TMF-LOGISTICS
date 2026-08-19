import base64
from pathlib import Path
import pandas as pd
import streamlit as st

# Import de la fonction d'authentification (adaptez le nom du fichier si nécessaire)
try:
    from login import ecran_connexion
except ImportError:
    # Si login.py n'existe pas encore, fonction temporaire pour éviter de faire crasher l'app
    def ecran_connexion():
        st.error("❌ Fichier 'login.py' introuvable.")
        return False

# ============================================================
# CONFIGURATION DE LA PAGE (Doit être la toute première commande Streamlit)
# ============================================================
st.set_page_config(
    page_title="TMF LOGISTICS",
    page_icon="🚛",
    layout="wide",
)

# ============================================================
# VERIFICATION DE L'AUTHENTIFICATION
# ============================================================
if not ecran_connexion():
    st.stop()  # Stoppe le script si l'utilisateur n'est pas connecté

# ============================================================
# CHEMINS DES PAGES
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
PAGES_DIR = BASE_DIR / "Pages"

PAGE_HOME = BASE_DIR / "app_home.py"
PAGE_OM = PAGES_DIR / "1_Ordres_de_Mission.py"
PAGE_CAMIONS = PAGES_DIR / "2_Camions.py"
PAGE_CHAUFFEURS = PAGES_DIR / "3_Chauffeurs.py"
PAGE_CLIENTS = PAGES_DIR / "4_Clients.py"
PAGE_RAPPORTS = PAGES_DIR / "5_Rapports.py"

# ============================================================
# VÉRIFICATION DE L'EXISTENCE DES FICHIERS
# ============================================================
fichiers = {
    "Accueil": PAGE_HOME,
    "Ordres de Mission": PAGE_OM,
    "Camions": PAGE_CAMIONS,
    "Chauffeurs": PAGE_CHAUFFEURS,
    "Clients": PAGE_CLIENTS,
    "Rapports": PAGE_RAPPORTS,
}

fichiers_manquants = [
    f"{nom} → {chemin}" for nom, chemin in fichiers.items() if not chemin.is_file()
]

if fichiers_manquants:
    st.error("❌ Fichiers de navigation introuvables")
    st.markdown("### Fichiers manquants")
    for fichier in fichiers_manquants:
        st.error(fichier)
    st.stop()

# ============================================================
# STYLE CSS PERSONNALISÉ
# ============================================================
st.markdown(
    """
    <style>
    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #f7f9fc;
    }

    /* TITRE SIDEBAR */
    .tmf-sidebar-title {
        text-align: center;
        font-size: 23px;
        font-weight: 800;
        color: #1f4e79;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    /* SOUS-TITRE SIDEBAR */
    .tmf-sidebar-subtitle {
        text-align: center;
        font-size: 12px;
        color: #666666;
        margin-bottom: 15px;
    }

    /* MASQUER MENU & FOOTER STREAMLIT */
    #MainMenu, footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# EN-TÊTE SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown(
        """
        <div class="tmf-sidebar-title">
            🚛 TMF LOGISTICS
        </div>
        <div class="tmf-sidebar-subtitle">
            Système de Gestion du Transport
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

# ============================================================
# CONFIGURATION DE LA NAVIGATION
# ============================================================

home_page = st.Page(str(PAGE_HOME), title="Accueil", icon="🏠", default=True)

# Arborescence de navigation
pages = {
    "": [home_page],
    "🚚 Gestion du transport": [
        st.Page(str(PAGE_OM), title="Ordres de Mission", icon="📋"),
        st.Page(str(PAGE_CAMIONS), title="Camions", icon="🚚"),
        st.Page(str(PAGE_CHAUFFEURS), title="Chauffeurs", icon="👷"),
        st.Page(str(PAGE_CLIENTS), title="Clients", icon="👥"),
        st.Page(str(PAGE_RAPPORTS), title="Rapports", icon="📊"),
    ],
}

# ============================================================
# EXECUTION DE LA NAVIGATION
# ============================================================
navigation = st.navigation(pages, position="sidebar")
navigation.run()
