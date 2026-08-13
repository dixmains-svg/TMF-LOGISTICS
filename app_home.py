import streamlit as st
import pandas as pd
import base64
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
# CHEMIN DU PROJET
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "Data"

EXCEL_OM = DATA_DIR / "OM.xlsx"
EXCEL_CAMIONS = DATA_DIR / "Camions.xlsx"
EXCEL_CHAUFFEURS = DATA_DIR / "Chauffeurs.xlsx"
EXCEL_CLIENTS = DATA_DIR / "Clients.xlsx"

BACKGROUND_PATH = BASE_DIR / "TMF.jpg"


# ============================================================
# FONCTION LECTURE EXCEL
# ============================================================

@st.cache_data
def charger_excel(fichier):

    if not fichier.exists():
        return pd.DataFrame()

    try:

        df = pd.read_excel(
            fichier,
            engine="openpyxl"
        )

        # Supprimer les lignes complètement vides
        df = df.dropna(how="all")

        return df

    except Exception as e:

        st.error(
            f"❌ Erreur lors de la lecture de {fichier.name} : {e}"
        )

        return pd.DataFrame()


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

df_om = charger_excel(EXCEL_OM)

df_camions = charger_excel(EXCEL_CAMIONS)

df_chauffeurs = charger_excel(EXCEL_CHAUFFEURS)

df_clients = charger_excel(EXCEL_CLIENTS)


# ============================================================
# NOMBRE D'ÉLÉMENTS
# ============================================================

nombre_om = len(df_om)

nombre_camions = len(df_camions)

nombre_chauffeurs = len(df_chauffeurs)

nombre_clients = len(df_clients)


# ============================================================
# ARRIÈRE-PLAN
# ============================================================

if BACKGROUND_PATH.exists():

    try:

        with open(BACKGROUND_PATH, "rb") as image_file:

            encoded_image = base64.b64encode(
                image_file.read()
            ).decode("utf-8")

        st.markdown(
            f"""
            <style>

            .stApp {{
                background-image:
                    linear-gradient(
                        rgba(255, 255, 255, 0.88),
                        rgba(255, 255, 255, 0.88)
                    ),
                    url("data:image/jpeg;base64,{encoded_image}");

                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}

            </style>
            """,
            unsafe_allow_html=True
        )

    except Exception:
        pass


# ============================================================
# TITRE
# ============================================================

st.title("🚛 TMF LOGISTICS")

st.subheader(
    "Système de Gestion du Transport et des Ordres de Mission"
)

st.divider()


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
        """)


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
        """)


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
