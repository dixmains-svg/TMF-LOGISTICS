import streamlit as st
from pathlib import Path

from database import init_database, statistiques


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TMF LOGISTICS",
    page_icon="🚛",
    layout="wide"
)


# ============================================================
# BASE DE DONNÉES
# ============================================================

init_database()


# ============================================================
# LOGO
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "logo.png"
page_title="TMF LOGISTICS",
if LOGO_PATH.exists():
    st.image(
        str(LOGO_PATH),
        width=200
    )
else:
    st.warning("⚠️ Logo introuvable")


# ============================================================
# TITRE
# ============================================================

st.title(" TMF LOGISTICS")

st.subheader(
    "Système de Gestion du Transport et des Ordres de Mission"
)

st.divider()


# ============================================================
# STATISTIQUES
# ============================================================

stats = statistiques()

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "📋 Ordres de Mission",
        stats["ordres_mission"]
    )


with col2:
    st.metric(
        "🚚 Camions",
        stats["camions"]
    )


with col3:
    st.metric(
        "👷 Chauffeurs",
        stats["chauffeurs"]
    )


with col4:
    st.metric(
        "👥 Clients",
        stats["clients"]
    )


st.divider()


# ============================================================
# BIENVENUE
# ============================================================

st.header("Azul Felawen dans TMF LOGISTICS 👋")

st.write(
    """
    Cette application permet de gérer les principales
    opérations de transport de TMF LOGISTICS.
    """
)


# ============================================================
# MODULES
# ============================================================

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


# ============================================================
# INFORMATION
# ============================================================

st.info(
    "💡 Utilisez le menu situé à gauche pour accéder "
    "aux différents modules."
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        text-align: center;
        padding: 20px;
    ">
        <b>TMF LOGISTICS</b><br>
        Système de Gestion du Transport<br>
        Version 2.0
    </div>
    """,
    unsafe_allow_html=True
)
