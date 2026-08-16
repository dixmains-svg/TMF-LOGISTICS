import streamlit as st
import pandas as pd
import base64
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TMF LOGISTICS - Accueil",
    page_icon="🚛",
    layout="wide"
)


# ============================================================
# CHEMINS
# ============================================================

# app_home.py se trouve à la racine du projet
BASE_DIR = Path(__file__).resolve().parent

# Dossier des données
DATA_DIR = BASE_DIR / "Data"

# Logo
LOGO = BASE_DIR / "logo.png"

# Image d'arrière-plan
BACKGROUND_PATH = BASE_DIR / "TMF.jpg"


# ============================================================
# FICHIERS EXCEL
# ============================================================

FICHIER_OM = DATA_DIR / "OM.xlsx"

FICHIER_CAMIONS = DATA_DIR / "Camions.xlsx"

FICHIER_CHAUFFEURS = DATA_DIR / "Chauffeurs.xlsx"

FICHIER_CLIENTS = DATA_DIR / "Clients.xlsx"


# ============================================================
# STYLE + ARRIÈRE-PLAN
# ============================================================

if BACKGROUND_PATH.exists():

    try:

        with open(
            BACKGROUND_PATH,
            "rb"
        ) as image_file:

            encoded_image = base64.b64encode(
                image_file.read()
            ).decode("utf-8")

        st.markdown(
            f"""
            <style>

            /* ==================================================
               ARRIÈRE-PLAN
               ================================================== */

            .stApp {{

                background-image:
                    linear-gradient(
                        rgba(255,255,255,0.88),
                        rgba(255,255,255,0.88)
                    ),
                    url(
                        "data:image/jpeg;base64,{encoded_image}"
                    );

                background-size: cover;

                background-position: center;

                background-repeat: no-repeat;

                background-attachment: fixed;
            }}


            /* ==================================================
               CARTES
               ================================================== */

            [data-testid="stMetric"] {{

                background: rgba(255,255,255,0.90);

                padding: 15px;

                border-radius: 12px;

                box-shadow:
                    0 2px 10px
                    rgba(0,0,0,0.08);
            }}


            /* ==================================================
               TITRE
               ================================================== */

            .tmf-title {{

                font-size: 50px;

                font-weight: bold;

                color: #1f4e79;
            }}


            .tmf-subtitle {{

                font-size: 25px;

                color: #555;

                margin-top: 5px;
            }}


            /* ==================================================
               FOOTER
               ================================================== */

            .tmf-footer {{

                text-align: center;

                margin-top: 40px;

                padding: 20px;

                color: #666;

                font-size: 13px;

                line-height: 1.7;

                border-top:
                    1px solid
                    rgba(0,0,0,0.10);
            }}

            .tmf-footer-title {{

                font-size: 20px;

                font-weight: bold;

                color: #1f4e79;
            }}

            .tmf-footer-subtitle {{

                font-size: 14px;

                margin-top: 3px;
            }}

            .tmf-footer-version {{

                font-size: 12px;

                margin-top: 5px;

                color: #888;
            }}

            </style>
            """,
            unsafe_allow_html=True
        )

    except Exception:
        pass


# ============================================================
# LECTURE EXCEL
# ============================================================

def lire_excel(fichier):

    """
    Lit un fichier Excel sans utiliser de cache.

    Les modifications enregistrées dans Excel seront
    récupérées lors de la prochaine exécution de la page.
    """

    if not fichier.exists():

        return pd.DataFrame()

    try:

        df = pd.read_excel(
            fichier,
            engine="openpyxl"
        )

        # Nettoyage des noms de colonnes
        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        # Suppression des lignes complètement vides
        df = df.dropna(
            how="all"
        )

        return df

    except Exception:

        return pd.DataFrame()


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

df_om = lire_excel(
    FICHIER_OM
)

df_camions = lire_excel(
    FICHIER_CAMIONS
)

df_chauffeurs = lire_excel(
    FICHIER_CHAUFFEURS
)

df_clients = lire_excel(
    FICHIER_CLIENTS
)


# ============================================================
# NOMBRE D'ÉLÉMENTS
# ============================================================

nombre_om = len(df_om)

nombre_camions = len(df_camions)

nombre_chauffeurs = len(df_chauffeurs)

nombre_clients = len(df_clients)


# ============================================================
# LOGO + TITRE
# ============================================================

col_logo, col_titre = st.columns(
    [1, 5]
)


# ============================================================
# LOGO
# ============================================================

with col_logo:

    if LOGO.exists():

        st.image(
            str(LOGO),
            width=100
        )


# ============================================================
# TITRE
# ============================================================

with col_titre:

   st.markdown(
    """
    <div class="tmf-title">
        🚛 TMF LOGISTICS
    </div>

    <div class="tmf-subtitle">
        Système de Gestion du Transport et des Ordres de Mission
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TABLEAU DE BORD
# ============================================================

st.header(
    "📊 Tableau de bord"
)


col1, col2, col3, col4 = st.columns(
    4
)


# ============================================================
# ORDRES DE MISSION
# ============================================================

with col1:

    st.metric(
        "📋 Ordres de Mission",
        nombre_om
    )


# ============================================================
# CAMIONS
# ============================================================

with col2:

    st.metric(
        "🚚 Camions",
        nombre_camions
    )


# ============================================================
# CHAUFFEURS
# ============================================================

with col3:

    st.metric(
        "👷 Chauffeurs",
        nombre_chauffeurs
    )


# ============================================================
# CLIENTS
# ============================================================

with col4:

    st.metric(
        "👥 Clients",
        nombre_clients
    )


st.divider()


# ============================================================
# MESSAGE D'ACCUEIL
# ============================================================

st.header(
    "Azul Felawen dans TMF LOGISTICS 👋"
)


st.write(
    """
    Bienvenue dans le système de gestion du transport
    de **TMF LOGISTICS**.

    Cette application permet de centraliser et de suivre
    les principales données liées à l'activité de transport.
    """
)


# ============================================================
# MODULES
# ============================================================

st.subheader(
    "📌 Modules de l'application"
)


col1, col2 = st.columns(
    2
)


# ============================================================
# COLONNE GAUCHE
# ============================================================

with col1:

    st.markdown(
        """
        ### 📋 Ordres de Mission

        Gestion et suivi des ordres de mission,
        des trajets, des camions, des chauffeurs,
        des clients et des kilométrages.
        """
    )

    st.markdown(
        """
        ### 🚚 Gestion du parc

        Suivi des camions, remorques,
        affectations et disponibilité du parc.
        """
    )

    st.markdown(
        """
        ### 👷 Gestion des Chauffeurs

        Gestion des chauffeurs,
        matricules, fonctions,
        affectations et superviseurs.
        """
    )


# ============================================================
# COLONNE DROITE
# ============================================================

with col2:

    st.markdown(
        """
        ### 👥 Gestion des Clients

        Gestion des clients,
        informations commerciales,
        coordonnées et lieux de chargement.
        """
    )

    st.markdown(
        """
        ### 📊 Rapports

        Analyse des données de transport,
        indicateurs de gestion,
        performance des chauffeurs
        et utilisation de la flotte.
        """
    )

    st.markdown(
        """
        ### 🔄 Données actualisées

        Les données sont récupérées directement
        depuis les fichiers Excel présents dans
        le dossier **Data**.
        """
    )


st.divider()


# ============================================================
# ACTUALISATION
# ============================================================

st.subheader(
    "🔄 Actualisation des données"
)


col1, col2, col3 = st.columns(
    [1, 2, 1]
)


with col2:

    if st.button(
        "🔄 Actualiser les données",
        use_container_width=True
    ):

        st.rerun()


# ============================================================
# INFORMATION
# ============================================================

st.info(
    """
    💡 **Information :**

    Pour obtenir les dernières données des fichiers Excel,
    modifiez et enregistrez vos fichiers dans le dossier
    **Data**, puis cliquez sur **🔄 Actualiser les données**.
    """
)


# ============================================================
# FOOTER
# ============================================================
st.markdown(
  """
    <div class="tmf-footer">

        <div class="tmf-footer-title">
            TMF LOGISTICS
        </div>

        <div class="tmf-footer-subtitle">
            Système de Gestion du Transport
        </div>

        <div class="tmf-footer-version">
            Version 1.0 — By H.Redjdal
        </div>

    </div>
    """,
    unsafe_allow_html=True
)
