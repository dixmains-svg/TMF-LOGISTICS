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
# RACINE DU PROJET
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
# VÉRIFICATION DU DOSSIER PAGES
# ============================================================

if not PAGES_DIR.exists():

    st.error(
        f"""
        ❌ Le dossier Pages est introuvable.

        Emplacement recherché :

        {PAGES_DIR}
        """
    )

    st.stop()


# ============================================================
# VÉRIFICATION DES FICHIERS
# ============================================================

fichiers = {
    "Accueil": PAGE_HOME,
    "Ordres de Mission": PAGE_OM,
    "Camions": PAGE_CAMIONS,
    "Chauffeurs": PAGE_CHAUFFEURS,
    "Clients": PAGE_CLIENTS,
    "Rapports": PAGE_RAPPORTS
}


fichiers_manquants = []


for nom, fichier in fichiers.items():

    if not fichier.is_file():

        fichiers_manquants.append(
            f"{nom} : {fichier}"
        )


# ============================================================
# AFFICHAGE DES FICHIERS MANQUANTS
# ============================================================

if fichiers_manquants:

    st.error(
        "❌ Certains fichiers de navigation sont introuvables."
    )

    st.write(
        "Fichiers recherchés :"
    )

    for fichier in fichiers_manquants:

        st.error(
            fichier
        )

    st.stop()


# ============================================================
# CSS
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
        font-size: 22px;
        font-weight: 700;
        color: #1f4e79;
        padding: 10px 0;
    }


    /* SOUS-TITRE */

    .tmf-sidebar-subtitle {
        text-align: center;
        font-size: 12px;
        color: #666;
        margin-bottom: 10px;
    }


    /* MASQUER MENU STREAMLIT */

    #MainMenu {
        visibility: hidden;
    }


    /* FOOTER STREAMLIT */

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
# NAVIGATION STREAMLIT
# ============================================================

navigation = st.navigation(
    pages,
    position="sidebar"
)


# ============================================================
# LANCEMENT
# ============================================================

navigation.run()
