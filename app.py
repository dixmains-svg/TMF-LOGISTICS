import streamlit as st
import pandas as pd
from database import init_database, statistiques


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
# INITIALISATION
# ============================================================

init_database()


# ============================================================
# LOGO
# ============================================================

st.logo(
    "https://img.icons8.com/color/96/truck.png"
)


# ============================================================
# TITRE
# ============================================================

st.title("🚛 TMF LOGISTICS")

st.subheader(
    "Système de Gestion du Transport et des Ordres de Mission"
)

st.divider()


# ============================================================
# STATISTIQUES
# ============================================================

stats = statistiques()

nombre_om = stats["ordres_mission"]
nombre_camions = stats["camions"]
nombre_chauffeurs = stats["chauffeurs"]
nombre_clients = stats["clients"]


# ============================================================
# TABLEAU DE BORD
# ============================================================

st.header("📊 Tableau de bord")


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "📋 Ordres de Mission",
        nombre_om
    )


with col2:
    st.metric(
        "🚚 Camions",
        nombre_camions
    )


with col3:
    st.metric(
        "👷 Chauffeurs",
        nombre_chauffeurs
    )


with col4:
    st.metric(
        "👥 Clients",
        nombre_clients
    )


st.divider()


# ============================================================
# BIENVENUE
# ============================================================

st.header("Bienvenue dans TMF LOGISTICS 👋")

st.write(
    """
Cette application permet de gérer les principales opérations
de transport de TMF LOGISTICS.
"""
)


col1, col2 = st.columns(2)


with col1:

    st.subheader("📋 Ordres de Mission")

    st.write(
        """
        Gestion des missions, camions, chauffeurs,
        clients, dates et kilométrages.
        """
    )

    st.subheader("🚚 Gestion du parc")

    st.write(
        """
        Suivi des camions, remorques, chauffeurs
        et affectations.
        """
    )


with col2:

    st.subheader("👷 Gestion des Chauffeurs")

    st.write(
        """
        Gestion des badges, fonctions,
        affectations et superviseurs.
        """
    )

    st.subheader("👥 Gestion des Clients")

    st.write(
        """
        Gestion des clients, coordonnées,
        contacts et informations commerciales.
        """
    )


st.divider()


st.info(
    "💡 Utilisez le menu situé à gauche pour accéder "
    "aux différents modules."
)


st.markdown(
    """
    <div style="text-align:center; padding:20px;">
        <b>TMF LOGISTICS</b><br>
        Système de Gestion du Transport<br>
        Version 2.0
    </div>
    """,
    unsafe_allow_html=True
)
