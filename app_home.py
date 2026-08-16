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
# CHEMIN PRINCIPAL
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "Data"

BACKGROUND_PATH = BASE_DIR / "TMF.jpg"


# ============================================================
# FICHIERS EXCEL
# ============================================================

FICHIER_OM = DATA_DIR / "OM.xlsx"

FICHIER_CAMIONS = DATA_DIR / "Camions.xlsx"

FICHIER_CHAUFFEURS = DATA_DIR / "Chauffeurs.xlsx"

FICHIER_CLIENTS = DATA_DIR / "Clients.xlsx"


# ============================================================
# ARRIÈRE-PLAN
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


            /* ================================
               TITRE PRINCIPAL
               ================================ */

            .main-title {{

                text-align: center;

                font-size: 38px;

                font-weight: 800;

                margin-top: 10px;

                margin-bottom: 5px;

            }}


            .main-subtitle {{

                text-align: center;

                font-size: 18px;

                color: #555;

                margin-bottom: 25px;

            }}


            /* ================================
               LOGO
               ================================ */

            .home-logo {{

                text-align: center;

                margin-bottom: 5px;

            }}

            .home-logo img {{

                width: 150px;

                max-width: 80%;

                height: auto;

            }}


            /* ================================
               CARTES
               ================================ */

            .info-box {{

                background: rgba(255,255,255,0.94);

                border-radius: 15px;

                padding: 20px;

                margin-top: 10px;

                margin-bottom: 10px;

                box-shadow:
                    0 3px 15px
                    rgba(0,0,0,0.10);

            }}


            /* ================================
               FOOTER
               ================================ */

            .footer {{

                text-align: center;

                padding: 25px;

                margin-top: 30px;

                color: #666;

                font-size: 14px;

            }}

            </style>
            """,
            unsafe_allow_html=True
        )

    except Exception:
        pass


# ============================================================
# FONCTION LECTURE EXCEL
# ============================================================

def lire_excel(fichier):

    """
    Lit un fichier Excel sans utiliser le cache.
    Les modifications du fichier Excel sont donc
    récupérées lors du rechargement de la page.
    """

    if not fichier.exists():

        return pd.DataFrame()


    try:

        df = pd.read_excel(
            fichier,
            engine="openpyxl"
        )


        # Nettoyage des colonnes

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
# CHARGEMENT DES 4 FICHIERS
# ============================================================

df_om = lire_excel(FICHIER_OM)

df_camions = lire_excel(FICHIER_CAMIONS)

df_chauffeurs = lire_excel(FICHIER_CHAUFFEURS)

df_clients = lire_excel(FICHIER_CLIENTS)


# ============================================================
# NOMBRE D'ÉLÉMENTS
# ============================================================

nombre_om = len(df_om)

nombre_camions = len(df_camions)

nombre_chauffeurs = len(df_chauffeurs)

nombre_clients = len(df_clients)

# ============================================================
# TITRE
# ============================================================

st.markdown(
    """
    <div class="main-title">
        🚛 TMF LOGISTICS
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="main-subtitle">
        Système de Gestion du Transport et des Ordres de Mission
    </div>
    """,
    unsafe_allow_html=True
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

st.subheader("📌 Modules de l'application")


col1, col2 = st.columns(2)


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
# ÉTAT DES FICHIERS
# ============================================================

st.subheader("📁 État des données")


col1, col2, col3, col4 = st.columns(4)


with col1:

    if FICHIER_OM.exists():

        st.success("📋 OM.xlsx")

    else:

        st.error("❌ OM.xlsx")


with col2:

    if FICHIER_CAMIONS.exists():

        st.success("🚚 Camions.xlsx")

    else:

        st.error("❌ Camions.xlsx")


with col3:

    if FICHIER_CHAUFFEURS.exists():

        st.success("👷 Chauffeurs.xlsx")

    else:

        st.error("❌ Chauffeurs.xlsx")


with col4:

    if FICHIER_CLIENTS.exists():

        st.success("👥 Clients.xlsx")

    else:

        st.error("❌ Clients.xlsx")


# ============================================================
# ACTUALISATION
# ============================================================

st.divider()


col1, col2, col3 = st.columns([1, 2, 1])


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
    <div style="
        text-align:center;
        margin-top:30px;
        padding:15px;
        color:#666;
        font-size:13px;
        line-height:1.6;
    ">
        <b style="font-size:18px; color:#1f4e79;">
            TMF LOGISTICS
        </b>
        <br>
        Système de Gestion du Transport
        <br>
        <span style="font-size:12px;">
            Version 1.0 — By H.Redjdal
        </span>
    </div>
    """,
    unsafe_allow_html=True
)
