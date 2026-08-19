import streamlit as st
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TMF LOGISTICS",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CHEMIN DU PROJET
# ============================================================

# app.py se trouve à la racine du projet
BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# DOSSIERS
# ============================================================

DATA_DIR = BASE_DIR / "Data"
PAGES_DIR = BASE_DIR / "Pages"


# ============================================================
# FICHIERS DES PAGES
# ============================================================

PAGE_HOME = BASE_DIR / "app_home.py"

PAGE_OM = PAGES_DIR / "1_Ordres_de_Mission.py"

PAGE_CAMIONS = PAGES_DIR / "2_Camions.py"

PAGE_CHAUFFEURS = PAGES_DIR / "3_Chauffeurs.py"

PAGE_CLIENTS = PAGES_DIR / "4_Clients.py"

PAGE_RAPPORTS = PAGES_DIR / "5_Rapports.py"


# ============================================================
# STYLE GLOBAL
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       SIDEBAR
       ====================================================== */

    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }


    /* ======================================================
       TITRE SIDEBAR
       ====================================================== */

    .sidebar-title {
        text-align: center;
        font-size: 20px;
        font-weight: 700;
        color: #1f4e79;
        padding-top: 10px;
        padding-bottom: 10px;
    }


    /* ======================================================
       FOOTER SIDEBAR
       ====================================================== */

    .sidebar-footer {
        text-align: center;
        color: #777;
        font-size: 11px;
        padding-top: 30px;
    }


    /* ======================================================
       MASQUER MENU STREAMLIT INUTILE
       ====================================================== */

    #MainMenu {
        visibility: hidden;
    }


    /* ======================================================
       FOOTER STREAMLIT
       ====================================================== */

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# VÉRIFICATION DE LA STRUCTURE
# ============================================================

fichiers_pages = {
    "Accueil": PAGE_HOME,
    "Ordres de Mission": PAGE_OM,
    "Camions": PAGE_CAMIONS,
    "Chauffeurs": PAGE_CHAUFFEURS,
    "Clients": PAGE_CLIENTS,
    "Rapports": PAGE_RAPPORTS
}


# ============================================================
# VÉRIFICATION DES PAGES
# ============================================================

pages_manquantes = []

for nom, fichier in fichiers_pages.items():

    if not fichier.exists():

        pages_manquantes.append(
            f"{nom} → {fichier}"
        )


# ============================================================
# ERREUR SI UNE PAGE MANQUE
# ============================================================

if pages_manquantes:

    st.error(
        "❌ Une ou plusieurs pages de l'application sont introuvables."
    )

    st.markdown(
        "### 📁 Structure attendue"
    )

    st.code(
        """
tmf-logistics/
│
├── app.py
├── app_home.py
│
├── Data/
│   ├── OM.xlsx
│   ├── Camions.xlsx
│   ├── Chauffeurs.xlsx
│   └── Clients.xlsx
│
└── Pages/
    ├── 1_Ordres_de_Mission.py
    ├── 2_Camions.py
    ├── 3_Chauffeurs.py
    ├── 4_Clients.py
    └── 5_Rapports.py
        """
    )

    st.markdown(
        "### ❌ Fichiers manquants"
    )

    for fichier in pages_manquantes:

        st.error(
            fichier
        )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-title">
            🚛 TMF LOGISTICS
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.caption(
        "Système de Gestion du Transport"
    )

    st.caption(
        "Gestion des Ordres de Mission"
    )

    st.divider()


# ============================================================
# NAVIGATION
# ============================================================

pages = {

    "🏠 Accueil": st.Page(
        str(PAGE_HOME),
        title="Accueil",
        icon="🏠"
    ),

    "📋 Ordres de Mission": st.Page(
        str(PAGE_OM),
        title="Ordres de Mission",
        icon="📋"
    ),

    "🚚 Camions": st.Page(
        str(PAGE_CAMIONS),
        title="Camions",
        icon="🚚"
    ),

    "👷 Chauffeurs": st.Page(
        str(PAGE_CHAUFFEURS),
        title="Chauffeurs",
        icon="👷"
    ),

    "👥 Clients": st.Page(
        str(PAGE_CLIENTS),
        title="Clients",
        icon="👥"
    ),

    "📊 Rapports": st.Page(
        str(PAGE_RAPPORTS),
        title="Rapports",
        icon="📊"
    )
}


# ============================================================
# CRÉATION DE LA NAVIGATION
# ============================================================

navigation = st.navigation(
    pages,
    position="sidebar",
    expanded=True
)


# ============================================================
# EXÉCUTION DE LA PAGE
# ============================================================

navigation.run()
