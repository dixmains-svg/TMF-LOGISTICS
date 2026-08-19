
import streamlit as st
from login import afficher_login
from app_home import afficher_home

# Configuration de la page
st.set_page_config(
    page_title="TMF LOGISTICS",
    page_icon="🚛",
    layout="wide",
)

# 1. Vérification : Si l'utilisateur n'est PAS connecté -> Afficher Login
if not st.session_state.get("connecte", False):
    afficher_login()
    st.stop()  # Empêche l'affichage de la suite

# 2. Si l'utilisateur EST connecté -> Afficher la page d'accueil
afficher_home()

# ============================================================
# CHEMINS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

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
# VÉRIFICATION DES FICHIERS
# ============================================================

fichiers = {
    "Accueil": PAGE_HOME,
    "Ordres de Mission": PAGE_OM,
    "Camions": PAGE_CAMIONS,
    "Chauffeurs": PAGE_CHAUFFEURS,
    "Clients": PAGE_CLIENTS,
    "Rapports": PAGE_RAPPORTS,
}


fichiers_manquants = []

for nom, chemin in fichiers.items():

    if not chemin.is_file():

        fichiers_manquants.append(
            f"{nom} → {chemin}"
        )


if fichiers_manquants:

    st.error(
        "❌ Fichiers de navigation introuvables"
    )

    st.markdown(
        "### Fichiers manquants"
    )

    for fichier in fichiers_manquants:

        st.error(fichier)

    st.stop()


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       SIDEBAR
       ======================================================== */

    [data-testid="stSidebar"] {
        background-color: #f7f9fc;
    }


    /* ========================================================
       TITRE SIDEBAR
       ======================================================== */

    .tmf-sidebar-title {
        text-align: center;
        font-size: 23px;
        font-weight: 800;
        color: #1f4e79;
        margin-top: 10px;
        margin-bottom: 5px;
    }


    /* ========================================================
       SOUS-TITRE SIDEBAR
       ======================================================== */

    .tmf-sidebar-subtitle {
        text-align: center;
        font-size: 12px;
        color: #666666;
        margin-bottom: 15px;
    }


    /* ========================================================
       MASQUER MENU STREAMLIT
       ======================================================== */

    #MainMenu {
        visibility: hidden;
    }


    /* ========================================================
       MASQUER FOOTER STREAMLIT
       ======================================================== */

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
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
        unsafe_allow_html=True
    )

    st.divider()


# ============================================================
# NAVIGATION
# ============================================================
#
# IMPORTANT :
# Les valeurs du dictionnaire sont des LISTES.
#
# Correct :
#
# "Accueil": [
#     st.Page(...)
# ]
#
# et non :
#
# "Accueil": st.Page(...)
#
# ============================================================

pages = {

    "🏠 Accueil": [

        st.Page(
            str(PAGE_HOME),
            title="Accueil",
            icon="🏠",
            default=True
        )

    ],

    "🚛 Gestion du transport": [

        st.Page(
            str(PAGE_OM),
            title="Ordres de Mission",
            icon="📋"
        ),

        st.Page(
            str(PAGE_CAMIONS),
            title="Camions",
            icon="🚚"
        ),

        st.Page(
            str(PAGE_CHAUFFEURS),
            title="Chauffeurs",
            icon="👷"
        ),

        st.Page(
            str(PAGE_CLIENTS),
            title="Clients",
            icon="👥"
        ),

        st.Page(
            str(PAGE_RAPPORTS),
            title="Rapports",
            icon="📊"
        )

    ]

}


# ============================================================
# CRÉATION DE LA NAVIGATION
# ============================================================

navigation = st.navigation(
    pages,
    position="sidebar"
)


# ============================================================
# EXÉCUTION DE LA PAGE
# ============================================================

navigation.run()
