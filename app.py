import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Gestion de la flotte TMF Logistics",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CHEMINS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "Data")

LOGO_FILE = os.path.join(BASE_DIR, "logo.png")


# ============================================================
# FICHIERS EXCEL
# ============================================================

FILES = {
    "camions": os.path.join(DATA_DIR, "Camions.xlsx"),
    "chauffeurs": os.path.join(DATA_DIR, "Chauffeurs.xlsx"),
    "clients": os.path.join(DATA_DIR, "Clients.xlsx"),
    "commandes": os.path.join(DATA_DIR, "Commande de vente.xlsx"),
    "om": os.path.join(DATA_DIR, "OM.xlsx"),
}


# ============================================================
# STYLE CSS
# ============================================================

st.markdown(
    """
    <style>

    /* --------------------------------------------------------
       GLOBAL
       -------------------------------------------------------- */

    .stApp {
        background-color: #f5f7f6;
    }

    /* --------------------------------------------------------
       SIDEBAR
       -------------------------------------------------------- */

    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #d9e2dd;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .sidebar-title {
        font-size: 21px;
        font-weight: 700;
        color: #0b5d3b;
        line-height: 1.2;
        margin-top: 8px;
    }

    .sidebar-subtitle {
        color: #666666;
        font-size: 13px;
        margin-top: 4px;
        margin-bottom: 15px;
    }

    /* --------------------------------------------------------
       HEADER
       -------------------------------------------------------- */

    .tmf-header {
        background: linear-gradient(
            135deg,
            #0b5d3b 0%,
            #0e754a 100%
        );

        padding: 18px 24px;
        border-radius: 12px;
        margin-bottom: 22px;

        box-shadow:
            0 4px 12px rgba(0, 0, 0, 0.08);
    }

    .tmf-title {
        font-size: 32px;
        font-weight: 700;
        color: white;
        margin-left: 10px;
        line-height: 1.2;
    }

    .tmf-subtitle {
        margin-top: 7px;
        margin-left: 10px;
        font-size: 15px;
        color: #e8f5ef;
    }

    /* --------------------------------------------------------
       SECTION
       -------------------------------------------------------- */

    .section-title {
        background-color: #0b5d3b;
        color: white;
        padding: 10px 15px;
        border-radius: 8px;
        font-size: 19px;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    /* --------------------------------------------------------
       CARDS
       -------------------------------------------------------- */

    .dashboard-card {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        min-height: 120px;

        border: 1px solid #e0e7e3;

        box-shadow:
            0 2px 8px rgba(0, 0, 0, 0.05);
    }

    .card-title {
        color: #666666;
        font-size: 14px;
        margin-bottom: 7px;
    }

    .card-value {
        color: #0b5d3b;
        font-size: 30px;
        font-weight: 700;
    }

    /* --------------------------------------------------------
       DATAFRAME
       -------------------------------------------------------- */

    div[data-testid="stDataFrame"] {
        border-radius: 8px;
    }

    /* --------------------------------------------------------
       BUTTONS
       -------------------------------------------------------- */

    .stButton > button {
        border-radius: 7px;
        font-weight: 600;
    }

    /* --------------------------------------------------------
       FOOTER
       -------------------------------------------------------- */

    .tmf-footer {
        text-align: center;
        color: #777777;
        font-size: 12px;
        margin-top: 40px;
        padding: 15px;
        border-top: 1px solid #dddddd;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FONCTIONS
# ============================================================

@st.cache_data
def get_sheets(file_path):
    """
    Retourne la liste des feuilles Excel.
    """
    if not os.path.isfile(file_path):
        return []

    try:
        excel_file = pd.ExcelFile(file_path)
        return excel_file.sheet_names
    except Exception:
        return []


@st.cache_data
def read_excel(file_path, sheet_name=0):
    """
    Lecture sécurisée d'une feuille Excel.
    """

    if not os.path.isfile(file_path):
        return pd.DataFrame()

    try:
        return pd.read_excel(
            file_path,
            sheet_name=sheet_name,
            engine="openpyxl"
        )

    except Exception:
        return pd.DataFrame()


def load_data(file_key, preferred_sheet=None):
    """
    Charge les données d'un fichier Excel.
    """

    file_path = FILES.get(file_key)

    if not file_path:
        return pd.DataFrame()

    if not os.path.isfile(file_path):
        return pd.DataFrame()

    sheets = get_sheets(file_path)

    if not sheets:
        return pd.DataFrame()

    # Feuille demandée
    if preferred_sheet and preferred_sheet in sheets:
        sheet = preferred_sheet
    else:
        sheet = sheets[0]

    return read_excel(file_path, sheet)


def search_data(df, search_text):
    """
    Recherche un texte dans toutes les colonnes.
    """

    if df.empty or not search_text:
        return df

    search_text = str(search_text).lower()

    mask = df.astype(str).apply(
        lambda column: column.str.lower().str.contains(
            search_text,
            na=False
        )
    )

    return df[mask.any(axis=1)]


def filter_data(df, column, value):
    """
    Filtre un DataFrame sur une colonne.
    """

    if df.empty:
        return df

    if column not in df.columns:
        return df

    if value == "Tous":
        return df

    return df[df[column].astype(str) == str(value)]


def dataframe_to_excel(df):
    """
    Transforme un DataFrame en fichier Excel.
    """

    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Export"
        )

    output.seek(0)

    return output


def show_table(df, height=500):

    if df.empty:
        st.info("Aucune donnée disponible.")
        return

    st.dataframe(
        df,
        use_container_width=True,
        height=height,
        hide_index=True
    )

    excel_file = dataframe_to_excel(df)

    st.download_button(
        label="📥 Télécharger en Excel",
        data=excel_file,
        file_name="export_tmf_logistics.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )


def file_status(file_key):
    """
    Vérifie l'existence d'un fichier.
    """

    file_path = FILES.get(file_key)

    if not file_path:
        return False

    return os.path.isfile(file_path)


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

camions = load_data("camions")

chauffeurs = load_data(
    "chauffeurs",
    "Chauffeurs"
)

clients = load_data("clients")

commandes = load_data("commandes")

om = load_data(
    "om",
    "Input OM fini"
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # LOGO
    # --------------------------------------------------------

    if os.path.isfile(LOGO_FILE):

        st.image(
            LOGO_FILE,
            width=120
        )

    else:

        st.markdown(
            """
            <div style="
                font-size:55px;
                text-align:center;
            ">
                🚚
            </div>
            """,
            unsafe_allow_html=True
        )

        st.warning(
            "logo.png introuvable dans le dossier de l'application."
        )

    # --------------------------------------------------------
    # TITRE SIDEBAR
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="sidebar-title">
            Gestion de la flotte TMF Logistics
        </div>

        <div class="sidebar-subtitle">
            Transport & Logistique
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # --------------------------------------------------------
    # MENU UNIQUE
    # --------------------------------------------------------

    menu = st.radio(
        "MENU",
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
        label_visibility="collapsed"
    )


# ============================================================
# HEADER PRINCIPAL
# ============================================================

st.markdown(
    '<div class="tmf-header">',
    unsafe_allow_html=True
)

col_logo, col_title = st.columns(
    [1, 6],
    vertical_alignment="center"
)

with col_logo:

    if os.path.isfile(LOGO_FILE):

        st.image(
            LOGO_FILE,
            width=100
        )

    else:

        st.markdown(
            """
            <div style="
                font-size:60px;
                text-align:center;
            ">
                🚚
            </div>
            """,
            unsafe_allow_html=True
        )


with col_title:

    st.markdown(
        """
        <div class="tmf-title">
            Gestion de la flotte TMF Logistics
        </div>

        <div class="tmf-subtitle">
            Transport & Logistique
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# ACCUEIL
# ============================================================

if menu == "🏠 Accueil":

    st.markdown(
        '<div class="section-title">🏠 Tableau de bord</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # INDICATEURS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="dashboard-card">

                <div class="card-title">
                    🚛 Camions
                </div>

                <div class="card-value">
                    {len(camions)}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="dashboard-card">

                <div class="card-title">
                    👨‍✈️ Chauffeurs
                </div>

                <div class="card-value">
                    {len(chauffeurs)}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="dashboard-card">

                <div class="card-title">
                    👥 Clients
                </div>

                <div class="card-value">
                    {len(clients)}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:

        st.markdown(
            f"""
            <div class="dashboard-card">

                <div class="card-title">
                    📋 Ordres de Mission
                </div>

                <div class="card-value">
                    {len(om)}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # --------------------------------------------------------
    # INFORMATIONS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">📌 Informations</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Bienvenue dans l'application "
        "Gestion de la flotte TMF Logistics."
    )

    st.write(
        """
        Cette application permet de consulter et d'exploiter
        les données relatives au transport, aux camions,
        aux chauffeurs, aux clients, aux commandes de vente
        et aux ordres de mission.
        """
    )


# ============================================================
# GESTION DU TRANSPORT
# ============================================================

elif menu == "🚚 Gestion du transport":

    st.markdown(
        '<div class="section-title">🚚 Gestion du transport</div>',
        unsafe_allow_html=True
    )

    st.write(
        """
        Module de suivi et de gestion des opérations
        de transport.
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class="dashboard-card">

                <div class="card-title">
                    Camions disponibles dans la base
                </div>

                <div class="card-value">
                    {len(camions)}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="dashboard-card">

                <div class="card-title">
                    Chauffeurs
                </div>

                <div class="card-value">
                    {len(chauffeurs)}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="dashboard-card">

                <div class="card-title">
                    Ordres de Mission
                </div>

                <div class="card-value">
                    {len(om)}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    if not om.empty:

        st.subheader("📋 Données de transport")

        search = st.text_input(
            "🔎 Rechercher",
            key="transport_search"
        )

        filtered_om = search_data(
            om,
            search
        )

        show_table(
            filtered_om,
            height=500
        )

    else:

        st.warning(
            "Le fichier OM.xlsx ne contient aucune donnée "
            "ou n'est pas disponible."
        )


# ============================================================
# ORDRES DE MISSION
# ============================================================

elif menu == "📋 Ordres de Mission":

    st.markdown(
        '<div class="section-title">📋 Ordres de Mission</div>',
        unsafe_allow_html=True
    )

    if om.empty:

        st.warning(
            "Aucune donnée disponible dans OM.xlsx."
        )

    else:

        st.write(
            f"Nombre total d'enregistrements : **{len(om)}**"
        )

        # Recherche
        search = st.text_input(
            "🔎 Rechercher dans les ordres de mission",
            key="om_search"
        )

        filtered_om = search_data(
            om,
            search
        )

        # Filtre colonne
        if len(om.columns) > 0:

            filter_col = st.selectbox(
                "Filtrer par colonne",
                ["Aucun filtre"] + list(om.columns),
                key="om_filter_column"
            )

            if filter_col != "Aucun filtre":

                values = (
                    om[filter_col]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                values = sorted(values)

                selected_value = st.selectbox(
                    "Valeur",
                    ["Tous"] + values,
                    key="om_filter_value"
                )

                filtered_om = filter_data(
                    filtered_om,
                    filter_col,
                    selected_value
                )

        show_table(
            filtered_om,
            height=600
        )


# ============================================================
# CAMIONS
# ============================================================

elif menu == "🚛 Camions":

    st.markdown(
        '<div class="section-title">🚛 Gestion des camions</div>',
        unsafe_allow_html=True
    )

    if camions.empty:

        st.warning(
            "Aucune donnée disponible dans Camions.xlsx."
        )

    else:

        st.write(
            f"Nombre total de camions : **{len(camions)}**"
        )

        search = st.text_input(
            "🔎 Rechercher un camion",
            key="camion_search"
        )

        filtered_camions = search_data(
            camions,
            search
        )

        show_table(
            filtered_camions,
            height=600
        )


# ============================================================
# CHAUFFEURS
# ============================================================

elif menu == "👨‍✈️ Chauffeurs":

    st.markdown(
        '<div class="section-title">👨‍✈️ Gestion des chauffeurs</div>',
        unsafe_allow_html=True
    )

    if chauffeurs.empty:

        st.warning(
            "Aucune donnée disponible dans Chauffeurs.xlsx."
        )

    else:

        st.write(
            f"Nombre total de chauffeurs : **{len(chauffeurs)}**"
        )

        search = st.text_input(
            "🔎 Rechercher un chauffeur",
            key="chauffeur_search"
        )

        filtered_chauffeurs = search_data(
            chauffeurs,
            search
        )

        show_table(
            filtered_chauffeurs,
            height=600
        )


# ============================================================
# CLIENTS
# ============================================================

elif menu == "👥 Clients":

    st.markdown(
        '<div class="section-title">👥 Gestion des clients</div>',
        unsafe_allow_html=True
    )

    if clients.empty:

        st.warning(
            "Aucune donnée disponible dans Clients.xlsx."
        )

    else:

        st.write(
            f"Nombre total de clients : **{len(clients)}**"
        )

        search = st.text_input(
            "🔎 Rechercher un client",
            key="client_search"
        )

        filtered_clients = search_data(
            clients,
            search
        )

        show_table(
            filtered_clients,
            height=600
        )


# ============================================================
# COMMANDES DE VENTE
# ============================================================

elif menu == "📦 Commandes de vente":

    st.markdown(
        '<div class="section-title">📦 Commandes de vente</div>',
        unsafe_allow_html=True
    )

    if commandes.empty:

        st.warning(
            "Aucune donnée disponible dans "
            "Commande de vente.xlsx."
        )

    else:

        st.write(
            f"Nombre total de commandes : **{len(commandes)}**"
        )

        search = st.text_input(
            "🔎 Rechercher une commande",
            key="commande_search"
        )

        filtered_commandes = search_data(
            commandes,
            search
        )

        show_table(
            filtered_commandes,
            height=600
        )


# ============================================================
# RAPPORTS
# ============================================================

elif menu == "📊 Rapports":

    st.markdown(
        '<div class="section-title">📊 Rapports</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Sélectionnez les données que vous souhaitez consulter."
    )

    rapport_type = st.selectbox(
        "Type de rapport",
        [
            "Ordres de Mission",
            "Camions",
            "Chauffeurs",
            "Clients",
            "Commandes de vente"
        ]
    )

    if rapport_type == "Ordres de Mission":

        df_rapport = om

    elif rapport_type == "Camions":

        df_rapport = camions

    elif rapport_type == "Chauffeurs":

        df_rapport = chauffeurs

    elif rapport_type == "Clients":

        df_rapport = clients

    else:

        df_rapport = commandes

    # --------------------------------------------------------
    # RECHERCHE
    # --------------------------------------------------------

    search = st.text_input(
        "🔎 Rechercher dans le rapport",
        key="rapport_search"
    )

    df_rapport = search_data(
        df_rapport,
        search
    )

    # --------------------------------------------------------
    # STATISTIQUES
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Nombre de lignes",
            len(df_rapport)
        )

    with col2:

        st.metric(
            "Nombre de colonnes",
            len(df_rapport.columns)
        )

    with col3:

        if not df_rapport.empty:

            memory = (
                df_rapport.memory_usage(
                    deep=True
                ).sum()
                / 1024
                / 1024
            )

            st.metric(
                "Taille mémoire",
                f"{memory:.2f} MB"
            )

        else:

            st.metric(
                "Taille mémoire",
                "0 MB"
            )

    st.write("")

    show_table(
        df_rapport,
        height=600
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="tmf-footer">
        © 2026 TMF LOGISTICS —
        Gestion de la flotte TMF Logistics
        <br>
        Transport & Logistique
    </div>
    """,
    unsafe_allow_html=True
)
