import streamlit as st

from login import connexion, deconnexion


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
# CONNEXION
# ============================================================

if not connexion():

    # Ne rien afficher tant que l'utilisateur
    # n'est pas connecté
    st.stop()


# ============================================================
# DÉCONNEXION
# ============================================================

deconnexion()


# ============================================================
# NAVIGATION
# ============================================================

pages = {

    "🏠 Accueil": [
        st.Page(
            "app_home.py",
            title="Tableau de bord",
            icon="🏠"
        )
    ],

    "📋 Gestion du Transport": [

        st.Page(
            "Pages/1_Ordres_de_Mission.py",
            title="Ordres de Mission",
            icon="📋"
        ),

        st.Page(
            "Pages/2_Camions.py",
            title="Camions",
            icon="🚚"
        ),

        st.Page(
            "Pages/3_Chauffeurs.py",
            title="Chauffeurs",
            icon="👷"
        ),

        st.Page(
            "Pages/4_Clients.py",
            title="Clients",
            icon="👥"
        )
    ],

    "📊 Analyse": [

        st.Page(
            "Pages/5_Rapports.py",
            title="Rapports",
            icon="📊"
        )
    ]
}


# ============================================================
# NAVIGATION STREAMLIT
# ============================================================

navigation = st.navigation(
    pages
)


# ============================================================
# LANCEMENT
# ============================================================

navigation.run()
