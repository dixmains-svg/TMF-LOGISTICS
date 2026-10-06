import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TMF LOGISTICS",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CHEMINS DES FICHIERS
# ============================================================

DATA_DIR = "Data"

CAMIONS_FILE = os.path.join(DATA_DIR, "Camions.xlsx")
CHAUFFEURS_FILE = os.path.join(DATA_DIR, "Chauffeurs.xlsx")
CLIENTS_FILE = os.path.join(DATA_DIR, "Clients.xlsx")
COMMANDES_FILE = os.path.join(DATA_DIR, "Commande de vente.xlsx")
OM_FILE = os.path.join(DATA_DIR, "OM.xlsx")


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>

    /* ================================
       PAGE
       ================================ */

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }


    /* ================================
       HEADER
       ================================ */

    .tmf-header {
        background: linear-gradient(
            135deg,
            #0b5d3b,
            #15915f
        );

        padding: 25px 35px;

        border-radius: 12px;

        color: white;

        margin-bottom: 25px;

        box-shadow:
            0 4px 12px rgba(0, 0, 0, 0.12);
    }

    .tmf-header h1 {
        margin: 0;
        padding: 0;

        color: white;

        font-size: 32px;
        font-weight: 700;
    }

    .tmf-header p {
        margin-top: 8px;
        margin-bottom: 0;

        color: white;

        font-size: 15px;
    }


    /* ================================
       TITRES
       ================================ */

    .section-title {
        color: #0b5d3b;

        font-size: 24px;

        font-weight: 700;

        margin-top: 10px;

        margin-bottom: 20px;
    }


    /* ================================
       CARTES
       ================================ */

    .metric-card {
        background: white;

        padding: 18px;

        border-radius: 10px;

        border-left: 5px solid #15915f;

        box-shadow:
            0 2px 8px rgba(0, 0, 0, 0.08);

        text-align: center;
    }

    .metric-title {
        color: #666666;

        font-size: 14px;
    }

    .metric-value {
        color: #0b5d3b;

        font-size: 28px;

        font-weight: bold;
    }


    /* ================================
       SIDEBAR
       ================================ */

    section[data-testid="stSidebar"] {
        background-color: #f0f2f6;
    }


    /* ================================
       TABLEAUX
       ================================ */

    div[data-testid="stDataFrame"] {
        border-radius: 8px;
    }


    /* ================================
       BOUTONS
       ================================ */

    .stButton > button {
        border-radius: 7px;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FONCTIONS EXCEL
# ============================================================

@st.cache_data
def get_excel_sheets(file_path):

    if not os.path.exists(file_path):
        return []

    try:

        excel = pd.ExcelFile(
            file_path,
            engine="openpyxl"
        )

        return excel.sheet_names

    except Exception:

        return []


@st.cache_data
def read_excel_file(
    file_path,
    sheet_name=None
):

    if not os.path.exists(file_path):
        return pd.DataFrame()

    try:

        if sheet_name:

            df = pd.read_excel(
                file_path,
                sheet_name=sheet_name,
                engine="openpyxl"
            )

        else:

            df = pd.read_excel(
                file_path,
                engine="openpyxl"
            )

        # Supprimer les lignes entièrement vides
        df = df.dropna(
            axis=0,
            how="all"
        )

        # Supprimer les colonnes entièrement vides
        df = df.dropna(
            axis=1,
            how="all"
        )

        # Nettoyer les noms des colonnes
        df.columns = [
            str(column).strip()
            for column in df.columns
        ]

        return df

    except Exception:

        return pd.DataFrame()


def load_file(
    file_path,
    preferred_sheet=None
):

    sheets = get_excel_sheets(
        file_path
    )

    if not sheets:

        return pd.DataFrame(), []

    # Utiliser la feuille demandée si elle existe
    if (
        preferred_sheet
        and preferred_sheet in sheets
    ):

        df = read_excel_file(
            file_path,
            preferred_sheet
        )

        return df, sheets

    # Sinon utiliser la première feuille
    df = read_excel_file(
        file_path,
        sheets[0]
    )

    return df, sheets


def search_dataframe(
    dataframe,
    search
):

    if dataframe.empty:
        return dataframe

    if search is None:
        return dataframe

    search = str(search).strip()

    if search == "":
        return dataframe

    mask = dataframe.astype(str).apply(
        lambda column:
        column.str.contains(
            search,
            case=False,
            na=False,
            regex=False
        )
    )

    return dataframe[
        mask.any(axis=1)
    ]


def filter_dataframe(
    dataframe,
    column,
    value
):

    if dataframe.empty:
        return dataframe

    if column == "Toutes les colonnes":
        return dataframe

    if not value:
        return dataframe

    mask = (
        dataframe[column]
        .astype(str)
        .str.contains(
            value,
            case=False,
            na=False,
            regex=False
        )
    )

    return dataframe[mask]


def dataframe_to_excel(
    dataframe
):

    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        dataframe.to_excel(
            writer,
            index=False,
            sheet_name="Rapport"
        )

    return output.getvalue()


def show_dataframe(
    dataframe,
    height=500
):

    if dataframe.empty:

        st.info(
            "Aucune donnée disponible."
        )

        return

    st.dataframe(
        dataframe,
        use_container_width=True,
        height=height,
        hide_index=True
    )


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

camions, camions_sheets = load_file(
    CAMIONS_FILE
)

chauffeurs, chauffeurs_sheets = load_file(
    CHAUFFEURS_FILE,
    "Chauffeurs"
)

clients, clients_sheets = load_file(
    CLIENTS_FILE
)

commandes, commandes_sheets = load_file(
    COMMANDES_FILE
)

# OM : priorité à "Input OM fini"
om, om_sheets = load_file(
    OM_FILE,
    "Input OM fini"
)


# ============================================================
# MENU UNIQUE
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:10px 0 20px 0;
        ">

            <div style="
                font-size:24px;
                font-weight:700;
                color:#0b5d3b;
            ">
                🚚 TMF LOGISTICS
            </div>

            <div style="
                margin-top:5px;
                color:#666;
                font-size:13px;
            ">
                Transport & Logistique
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown(
        "### MENU PRINCIPAL"
    )

    menu = st.radio(
        "",
        [
            "🏠 Accueil",
            "🚚 Gestion du transport",
            "📋 Ordres de Mission",
            "🚛 Camions",
            "👨‍✈️ Chauffeurs",
            "👥 Clients",
            "📦 Commandes de vente",
            "📊 Rapports"
        ],
        index=0
    )

    st.markdown("---")

    st.caption(
        "TMF LOGISTICS"
    )

    st.caption(
        datetime.now().strftime(
            "%d/%m/%Y %H:%M"
        )
    )


# ============================================================
# HEADER PRINCIPAL
# ============================================================

st.markdown(
    """
    <div class="tmf-header">

        <h1>🚚 TMF LOGISTICS</h1>

        <p>
            Gestion du transport •
            Ordres de mission •
            Camions •
            Chauffeurs •
            Clients •
            Rapports
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ACCUEIL
# ============================================================

if menu == "🏠 Accueil":

    st.markdown(
        '<div class="section-title">'
        '🏠 Tableau de bord'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # INDICATEURS
    # --------------------------------------------------------

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        st.metric(
            "🚛 Camions",
            len(camions)
        )

    with col2:

        st.metric(
            "👨‍✈️ Chauffeurs",
            len(chauffeurs)
        )

    with col3:

        st.metric(
            "👥 Clients",
            len(clients)
        )

    with col4:

        st.metric(
            "📦 Commandes",
            len(commandes)
        )

    with col5:

        st.metric(
            "📋 OM",
            len(om)
        )

    st.markdown("---")

    # --------------------------------------------------------
    # ÉTAT DES DONNÉES
    # --------------------------------------------------------

    st.markdown(
        "### 📁 État des données"
    )

    status = pd.DataFrame(
        {
            "Source": [
                "Camions",
                "Chauffeurs",
                "Clients",
                "Commandes de vente",
                "Ordres de Mission"
            ],

            "Fichier": [
                "Camions.xlsx",
                "Chauffeurs.xlsx",
                "Clients.xlsx",
                "Commande de vente.xlsx",
                "OM.xlsx"
            ],

            "Statut": [
                (
                    "✅ Disponible"
                    if os.path.exists(CAMIONS_FILE)
                    else "❌ Introuvable"
                ),

                (
                    "✅ Disponible"
                    if os.path.exists(CHAUFFEURS_FILE)
                    else "❌ Introuvable"
                ),

                (
                    "✅ Disponible"
                    if os.path.exists(CLIENTS_FILE)
                    else "❌ Introuvable"
                ),

                (
                    "✅ Disponible"
                    if os.path.exists(COMMANDES_FILE)
                    else "❌ Introuvable"
                ),

                (
                    "✅ Disponible"
                    if os.path.exists(OM_FILE)
                    else "❌ Introuvable"
                )
            ],

            "Lignes": [
                len(camions),
                len(chauffeurs),
                len(clients),
                len(commandes),
                len(om)
            ],

            "Colonnes": [
                len(camions.columns),
                len(chauffeurs.columns),
                len(clients.columns),
                len(commandes.columns),
                len(om.columns)
            ]
        }
    )

    st.dataframe(
        status,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # --------------------------------------------------------
    # GRAPHIQUE
    # --------------------------------------------------------

    st.markdown(
        "### 📊 Volume des données"
    )

    graph = pd.DataFrame(
        {
            "Source": [
                "Camions",
                "Chauffeurs",
                "Clients",
                "Commandes",
                "OM"
            ],

            "Nombre": [
                len(camions),
                len(chauffeurs),
                len(clients),
                len(commandes),
                len(om)
            ]
        }
    )

    st.bar_chart(
        graph.set_index("Source")
    )


# ============================================================
# GESTION DU TRANSPORT
# ============================================================

elif menu == "🚚 Gestion du transport":

    st.markdown(
        '<div class="section-title">'
        '🚚 Gestion du transport'
        '</div>',
        unsafe_allow_html=True
    )

    st.info(
        """
        Centre de gestion de l'activité transport.

        Les données disponibles sont :
        • Camions
        • Chauffeurs
        • Ordres de Mission
        • Clients
        • Commandes de vente
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "🚛 Parc camions",
            len(camions)
        )

    with col2:

        st.metric(
            "👨‍✈️ Chauffeurs",
            len(chauffeurs)
        )

    with col3:

        st.metric(
            "📋 Ordres de Mission",
            len(om)
        )

    st.markdown("---")

    st.subheader(
        "📊 Synthèse transport"
    )

    transport = pd.DataFrame(
        {
            "Élément": [
                "Camions",
                "Chauffeurs",
                "Clients",
                "Commandes",
                "Ordres de Mission"
            ],

            "Nombre": [
                len(camions),
                len(chauffeurs),
                len(clients),
                len(commandes),
                len(om)
            ]
        }
    )

    st.dataframe(
        transport,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# ORDRES DE MISSION
# ============================================================

elif menu == "📋 Ordres de Mission":

    st.markdown(
        '<div class="section-title">'
        '📋 Ordres de Mission'
        '</div>',
        unsafe_allow_html=True
    )

    if not om_sheets:

        st.error(
            "Impossible de lire OM.xlsx."
        )

    else:

        # ----------------------------------------------------
        # CHOIX FEUILLE
        # ----------------------------------------------------

        default_index = 0

        if "Input OM fini" in om_sheets:

            default_index = om_sheets.index(
                "Input OM fini"
            )

        sheet = st.selectbox(
            "📄 Feuille",
            om_sheets,
            index=default_index
        )

        data = read_excel_file(
            OM_FILE,
            sheet
        )

        st.success(
            f"{len(data)} ligne(s) chargée(s)"
        )

        # ----------------------------------------------------
        # RECHERCHE
        # ----------------------------------------------------

        search = st.text_input(
            "🔎 Rechercher dans les Ordres de Mission"
        )

        result = search_dataframe(
            data,
            search
        )

        # ----------------------------------------------------
        # FILTRE
        # ----------------------------------------------------

        if not result.empty:

            col1, col2 = st.columns(2)

            with col1:

                filter_column = st.selectbox(
                    "Filtrer par colonne",
                    [
                        "Toutes les colonnes"
                    ] + list(result.columns)
                )

            with col2:

                filter_value = st.text_input(
                    "Valeur du filtre"
                )

            result = filter_dataframe(
                result,
                filter_column,
                filter_value
            )

        st.write(
            f"**{len(result)} résultat(s)**"
        )

        show_dataframe(
            result,
            600
        )

        # ----------------------------------------------------
        # EXPORT
        # ----------------------------------------------------

        if not result.empty:

            st.download_button(
                label="⬇️ Télécharger le rapport OM",
                data=dataframe_to_excel(
                    result
                ),
                file_name="TMF_Rapport_OM.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                )
            )


# ============================================================
# CAMIONS
# ============================================================

elif menu == "🚛 Camions":

    st.markdown(
        '<div class="section-title">'
        '🚛 Camions'
        '</div>',
        unsafe_allow_html=True
    )

    if not camions_sheets:

        st.error(
            "Impossible de lire Camions.xlsx."
        )

    else:

        sheet = st.selectbox(
            "📄 Feuille",
            camions_sheets
        )

        data = read_excel_file(
            CAMIONS_FILE,
            sheet
        )

        st.metric(
            "Nombre de lignes",
            len(data)
        )

        search = st.text_input(
            "🔎 Rechercher un camion"
        )

        result = search_dataframe(
            data,
            search
        )

        st.write(
            f"**{len(result)} résultat(s)**"
        )

        show_dataframe(
            result,
            600
        )

        if not result.empty:

            st.download_button(
                label="⬇️ Télécharger les camions",
                data=dataframe_to_excel(
                    result
                ),
                file_name="TMF_Camions.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                )
            )


# ============================================================
# CHAUFFEURS
# ============================================================

elif menu == "👨‍✈️ Chauffeurs":

    st.markdown(
        '<div class="section-title">'
        '👨‍✈️ Chauffeurs'
        '</div>',
        unsafe_allow_html=True
    )

    if not chauffeurs_sheets:

        st.error(
            "Impossible de lire Chauffeurs.xlsx."
        )

    else:

        default_index = 0

        if "Chauffeurs" in chauffeurs_sheets:

            default_index = chauffeurs_sheets.index(
                "Chauffeurs"
            )

        sheet = st.selectbox(
            "📄 Feuille",
            chauffeurs_sheets,
            index=default_index
        )

        data = read_excel_file(
            CHAUFFEURS_FILE,
            sheet
        )

        st.metric(
            "Nombre de lignes",
            len(data)
        )

        search = st.text_input(
            "🔎 Rechercher un chauffeur"
        )

        result = search_dataframe(
            data,
            search
        )

        st.write(
            f"**{len(result)} résultat(s)**"
        )

        show_dataframe(
            result,
            600
        )

        if not result.empty:

            st.download_button(
                label="⬇️ Télécharger les chauffeurs",
                data=dataframe_to_excel(
                    result
                ),
                file_name="TMF_Chauffeurs.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                )
            )


# ============================================================
# CLIENTS
# ============================================================

elif menu == "👥 Clients":

    st.markdown(
        '<div class="section-title">'
        '👥 Clients'
        '</div>',
        unsafe_allow_html=True
    )

    if not clients_sheets:

        st.error(
            "Impossible de lire Clients.xlsx."
        )

    else:

        sheet = st.selectbox(
            "📄 Feuille",
            clients_sheets
        )

        data = read_excel_file(
            CLIENTS_FILE,
            sheet
        )

        st.metric(
            "Nombre de lignes",
            len(data)
        )

        search = st.text_input(
            "🔎 Rechercher un client"
        )

        result = search_dataframe(
            data,
            search
        )

        st.write(
            f"**{len(result)} résultat(s)**"
        )

        show_dataframe(
            result,
            600
        )

        if not result.empty:

            st.download_button(
                label="⬇️ Télécharger les clients",
                data=dataframe_to_excel(
                    result
                ),
                file_name="TMF_Clients.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                )
            )


# ============================================================
# COMMANDES DE VENTE
# ============================================================

elif menu == "📦 Commandes de vente":

    st.markdown(
        '<div class="section-title">'
        '📦 Commandes de vente'
        '</div>',
        unsafe_allow_html=True
    )

    if not commandes_sheets:

        st.error(
            "Impossible de lire "
            "Commande de vente.xlsx."
        )

    else:

        sheet = st.selectbox(
            "📄 Feuille",
            commandes_sheets
        )

        data = read_excel_file(
            COMMANDES_FILE,
            sheet
        )

        st.metric(
            "Nombre de lignes",
            len(data)
        )

        search = st.text_input(
            "🔎 Rechercher une commande"
        )

        result = search_dataframe(
            data,
            search
        )

        if not result.empty:

            col1, col2 = st.columns(2)

            with col1:

                filter_column = st.selectbox(
                    "Filtrer par colonne",
                    [
                        "Toutes les colonnes"
                    ] + list(result.columns)
                )

            with col2:

                filter_value = st.text_input(
                    "Valeur"
                )

            result = filter_dataframe(
                result,
                filter_column,
                filter_value
            )

        st.write(
            f"**{len(result)} résultat(s)**"
        )

        show_dataframe(
            result,
            600
        )

        if not result.empty:

            st.download_button(
                label="⬇️ Télécharger les commandes",
                data=dataframe_to_excel(
                    result
                ),
                file_name="TMF_Commandes_Vente.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                )
            )


# ============================================================
# RAPPORTS
# ============================================================

elif menu == "📊 Rapports":

    st.markdown(
        '<div class="section-title">'
        '📊 Rapports TMF LOGISTICS'
        '</div>',
        unsafe_allow_html=True
    )

    source = st.selectbox(
        "📂 Choisir la source",
        [
            "Ordres de Mission",
            "Camions",
            "Chauffeurs",
            "Clients",
            "Commandes de vente"
        ]
    )

    if source == "Ordres de Mission":

        data = om

    elif source == "Camions":

        data = camions

    elif source == "Chauffeurs":

        data = chauffeurs

    elif source == "Clients":

        data = clients

    else:

        data = commandes

    if data.empty:

        st.warning(
            "Aucune donnée disponible."
        )

    else:

        # ----------------------------------------------------
        # INDICATEURS
        # ----------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Lignes",
                len(data)
            )

        with col2:

            st.metric(
                "Colonnes",
                len(data.columns)
            )

        with col3:

            st.metric(
                "Cellules",
                data.shape[0] *
                data.shape[1]
            )

        st.markdown("---")

        # ----------------------------------------------------
        # RECHERCHE
        # ----------------------------------------------------

        search = st.text_input(
            "🔎 Rechercher dans le rapport"
        )

        result = search_dataframe(
            data,
            search
        )

        # ----------------------------------------------------
        # FILTRE
        # ----------------------------------------------------

        if not result.empty:

            col1, col2 = st.columns(2)

            with col1:

                filter_column = st.selectbox(
                    "Filtrer par colonne",
                    [
                        "Toutes les colonnes"
                    ] + list(result.columns)
                )

            with col2:

                filter_value = st.text_input(
                    "Valeur du filtre"
                )

            result = filter_dataframe(
                result,
                filter_column,
                filter_value
            )

        # ----------------------------------------------------
        # RÉSULTAT
        # ----------------------------------------------------

        st.subheader(
            f"Résultat : {len(result)} ligne(s)"
        )

        show_dataframe(
            result,
            600
        )

        # ----------------------------------------------------
        # EXPORT
        # ----------------------------------------------------

        if not result.empty:

            st.download_button(
                label="⬇️ Télécharger le rapport Excel",
                data=dataframe_to_excel(
                    result
                ),
                file_name="TMF_Rapport.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                )
            )


# ============================================================
# PIED DE PAGE
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#777;
        padding:10px;
    ">

        <b>TMF LOGISTICS</b><br>

        Application de gestion du transport
        et de reporting

    </div>
    """,
    unsafe_allow_html=True
)
