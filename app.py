import streamlit as st
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TMF LOGISTICS",
    page_icon="🚛",
    layout="wide"
)


# ============================================================
# CHEMIN RACINE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
PAGES_DIR = BASE_DIR / "Pages"


# ============================================================
# FICHIERS
# ============================================================

PAGE_HOME = BASE_DIR / "app_home.py"
PAGE_OM = PAGES_DIR / "1_Ordres_de_Mission.py"
PAGE_CAMIONS = PAGES_DIR / "2_Camions.py"
PAGE_CHAUFFEURS = PAGES_DIR / "3_Chauffeurs.py"
PAGE_CLIENTS = PAGES_DIR / "4_Clients.py"
PAGE_RAPPORTS = PAGES_DIR / "5_Rapports.py"


# ============================================================
# VÉRIFICATION
# ============================================================

fichiers = [
    PAGE_HOME,
    PAGE_OM,
    PAGE_CAMIONS,
    PAGE_CHAUFFEURS,
    PAGE_CLIENTS,
    PAGE_RAPPORTS
]


for fichier in fichiers:

    if not fichier.exists():

        st.error(
            f"❌ Fichier introuvable :\n\n`{fichier}`"
        )

        st.stop()


# ============================================================
# NAVIGATION
# ============================================================

pages = {

    "🏠 Accueil": [
        st.Page(
            PAGE_HOME,
            title="Accueil",
            icon="🏠"
        )
    ],

    "🚛 Gestion du transport": [

        st.Page(
            PAGE_OM,
            title="Ordres de Mission",
            icon="📋"
        ),

        st.Page(
            PAGE_CAMIONS,
            title="Camions",
            icon="🚚"
        ),

        st.Page(
            PAGE_CHAUFFEURS,
            title="Chauffeurs",
            icon="👷"
        ),

        st.Page(
            PAGE_CLIENTS,
            title="Clients",
            icon="👥"
        ),

        st.Page(
            PAGE_RAPPORTS,
            title="Rapports",
            icon="📊"
        )
    ]
]


# ============================================================
# NAVIGATION
# ============================================================

navigation = st.navigation(
    pages,
    position="sidebar"
)


# ============================================================
# LANCEMENT
# ============================================================

navigation.run()
