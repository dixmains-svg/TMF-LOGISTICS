import streamlit as st
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
# INITIALISER LA BASE
# ============================================================

init_database()

# ============================================================
# STYLE - ARRIÈRE-PLAN
# ============================================================

st.markdown(
    """
    <style>

    /* Arrière-plan */
    .stApp {
        background-image:
            linear-gradient(
                rgba(255, 255, 255, 0.90),
                rgba(255, 255, 255, 0.90)
            ),
            url("assets/background.jpg");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Contenu principal */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Cartes */
    .card {
        background-color: rgba(255, 255, 255, 0.93);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.12);
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 25px;
        margin-top: 30px;
        background-color: rgba(255,255,255,0.90);
        border-radius: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# EN-TÊTE AVEC LOGO
# ============================================================

col_logo, col_titre = st.columns([1, 6])

with col_logo:

    st.image(
        "assets/logo.png",
        width=120
    )

with col_titre:

    st.title("🚛 TMF LOGISTICS")

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

    st.markdown(
        """
        <div class="card">

        <h3>📋 Ordres de Mission</h3>

        <p>
        Gestion des missions, camions, chauffeurs,
        clients, dates et kilométrages.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="card">

        <h3>🚚 Gestion du parc</h3>

        <p>
        Suivi des camions, remorques, chauffeurs
        et affectations.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        """
        <div class="card">

        <h3>👷 Gestion des Chauffeurs</h3>

        <p>
        Gestion des badges, fonctions,
        affectations et superviseurs.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="card">

        <h3>👥 Gestion des Clients</h3>

        <p>
        Gestion des clients, coordonnées,
        contacts et informations commerciales.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

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
    <div class="footer">

        <b>🚛 TMF LOGISTICS</b><br>

        Système de Gestion du Transport<br>

        Version 2.0

    </div>
    """,
    unsafe_allow_html=True
)
