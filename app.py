import streamlit as st
import pandas as pd
import os
import io


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
    "om": os.path.join(DATA_DIR, "OM.xlsx")
}


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>

    /* =========================
       PAGE
       ========================= */

    .main {
        background-color: #f7f9f8;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }


    /* =========================
       SIDEBAR
       ========================= */

    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #dfe7e3;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }


    /* =========================
       MENU
       ========================= */

    div[role="radiogroup"] {
        gap: 5px;
    }

    div[role="radiogroup"] label {
        border-radius: 8px;
        padding: 8px 10px;
    }

    div[role="radiogroup"] label:hover {
        background-color: #eaf5ef;
    }


    /* =========================
       HEADER CENTRAL
       ========================= */

    .tmf-header {
        background: linear-gradient(
            135deg,
            #087443,
            #0b5d3b
        );

        border-radius: 12px;

        padding: 20px 25px;

        margin-bottom: 22px;

        box-shadow:
            0 3px 10px rgba(0, 0, 0, 0.08);
    }


    /* =========================
       TITRES
       ========================= */

    .section-title {
        font-size: 25px;
        font-weight: 700;
        color: #0b5d3b;
        margin-top: 10px;
        margin-bottom: 15px;
    }

    .sub-title {
        font-size: 19px;
        font-weight: 600;
        color: #0b5d3b;
        margin-top: 15px;
        margin-bottom: 10px;
    }


    /* =========================
       CARTES
       ========================= */

    .info-card {
        background-color: white;
        border-radius: 12px;
        padding: 18px;
        border: 1px solid #e1e8e4;
        box-shadow: 0 2px 7px rgba(0, 0, 0, 0.05);
        min-height: 110px;
    }

    .info-card-title {
        font-size: 14px;
        color: #777;
        margin-bottom: 8px;
    }

    .info-card-value {
        font-size: 28px;
        font-weight: 700;
        color: #0b5d3b;
    }


    /* =========================
       BOUTONS
       ========================= */

    .stButton > button {
        border-radius: 8px;
        border: 1px solid #0b5d3b;
        font-weight: 600;
    }


    /* =========================
       FOOTER
       ========================= */

    .footer {
        text-align: center;
        color: #777;
        font-size: 12px;
        margin-top: 35px;
        padding-top: 15px;
        border-top: 1px solid #ddd;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FONCTIONS EXCEL
# ============================================================

@st.cache_data
def get_sheets(file_path):

    try:

        if not os.path.isfile(file_path):
            return []

        excel_file = pd.ExcelFile(
            file_path,
            engine="openpyxl"
        )

        return excel_file.sheet_names

    except Exception:
        return []


@st.cache_data
def read_excel(file_path, sheet_name=0):

    try:

        if not os.path.isfile(file_path):
            return pd.DataFrame()

        return pd.read_excel(
            file_path,
            sheet_name=sheet_name,
            engine="openpyxl"
        )

    except Exception:
        return pd.DataFrame()


def load_data(file_path, preferred_sheet=None):

    if not os.path.isfile(file_path):
        return pd.DataFrame()

    sheets = get_sheets(file_path)

    if not sheets:
        return pd.DataFrame()

    if preferred_sheet and preferred_sheet in sheets:

        return read_excel(
            file_path,
            preferred_sheet
        )

    return read_excel(
        file_path,
        sheets[0]
    )


def search_data(df, search_text):

    if df.empty or not search_text:
        return df

    search_text = str(
        search_text
    ).lower().strip()

    mask = df.astype(str).apply(
        lambda column:
        column.str.lower().str.contains(
            search_text,
            na=False
        )
    ).any(axis=1)

    return df[mask]


def filter_data(df, column, value):

    if df.empty:
        return df

    if column not in df.columns:
        return df

    if value in [
        "Tous",
        "",
        None
    ]:
        return df

    return df[
        df[column].astype(str) == str(value)
    ]


def dataframe_to_excel(df):

    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Données"
        )

    return output.getvalue()


def show_table(df, key):

    if df.empty:

        st.info(
            "Aucune donnée disponible."
        )

        return

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        key=key
    )

    excel_data = dataframe_to_excel(df)

    st.download_button(
        label="📥 Télécharger Excel",
        data=excel_data,
        file_name="export_tmf_logistics.xlsx",
        mime=(
            "application/vnd.openxmlformats-"
            "officedocument.spreadsheetml.sheet"
        ),
        key=f"download_{key}"
    )


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

camions = load_data(
    FILES["camions"]
)

chauffeurs = load_data(
    FILES["chauffeurs"],
    "Chauffeurs"
)

clients = load_data(
    FILES["clients"]
)

commandes = load_data(
    FILES["commandes"]
)

om = load_data(
    FILES["om"],
    "Input OM fini"
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # Logo dans la barre latérale
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
                padding:10px;
            ">
                🚚
            </div>
            """,
            unsafe_allow_html=True
        )


    # Titre de la barre latérale
    st.markdown(
        """
        <div style="
            font-size:20px;
            font-weight:700;
            color:#0b5d3b;
            line-height:1.2;
        ">
            Gestion de la flotte
        </div>

        <div style="
            font-size:20px;
            font-weight:700;
            color:#0b5d3b;
            line-height:1.2;
        ">
            TMF Logistics
        </div>

        <div style="
            margin-top:5px;
            color:#666;
            font-size:13px;
        ">
            Transport & Logistique
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")


    # ========================================================
    # UN SEUL MENU
    # ========================================================

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
        index=0
    )


    st.markdown("---")


    # ========================================================
    # ÉTAT DES FICHIERS
    # ========================================================

    st.markdown(
        """
        <div style="
            font-size:13px;
            font-weight:600;
            color:#0b5d3b;
            margin-bottom:8px;
        ">
            📁 Fichiers de données
        </div>
        """,
        unsafe_allow_html=True
    )

    for name, path in FILES.items():

        if os.path.isfile(path):

            st.markdown(
                f"""
                <div style="
                    font-size:11px;
                    color:#16834b;
                    margin-bottom:3px;
                ">
                    ✓ {os.path.basename(path)}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div style="
                    font-size:11px;
                    color:#c0392b;
                    margin-bottom:3px;
                ">
                    ✗ {os.path.basename(path)}
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# HEADER CENTRAL
# LOGO + TITRE
# ============================================================

st.markdown(
    '<div class="tmf-header">',
    unsafe_allow_html=True
)


col_logo, col_title = st.columns(
    [1, 6],
    vertical_alignment="center"
)


# ============================================================
# LOGO CENTRAL
# ============================================================

with col_logo:

    if os.path.isfile(LOGO_FILE):

        st.image(
            LOGO_FILE,
            width=110
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


# ============================================================
# TITRE CENTRAL À DROITE DU LOGO
# ============================================================

with col_title:

    st.markdown(
        """
        <div style="
            font-size:32px;
            font-weight:700;
            color:white;
            margin-left:10px;
            text-align:left;
            line-height:1.2;
        ">
            Gestion de la flotte TMF Logistics
        </div>

        <div style="
            margin-top:8px;
            margin-left:10px;
            font-size:15px;
            color:#e8f5ef;
            text-align:left;
        ">
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

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-card-title">
                    🚛 Camions
                </div>

                <div class="info-card-value">
                    {len(camions)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-card-title">
                    👨‍✈️ Chauffeurs
                </div>

                <div class="info-card-value">
                    {len(chauffeurs)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-card-title">
                    👥 Clients
                </div>

                <div class="info-card-value">
                    {len(clients)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col4:

        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-card-title">
                    📋 Ordres de mission
                </div>

                <div class="info-card-value">
                    {len(om)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown("")


    st.markdown(
        '<div class="sub-title">📌 Présentation</div>',
        unsafe_allow_html=True
    )

    st.info(
        """
        Bienvenue dans l'application **Gestion de la flotte TMF Logistics**.

        Cette application permet de consulter et d'exploiter les données
        relatives au transport, aux camions, aux chauffeurs, aux clients,
        aux commandes de vente et aux ordres de mission.
        """
    )


    st.markdown(
        '<div class="sub-title">📁 État des fichiers</div>',
        unsafe_allow_html=True
    )

    file_status = []

    for name, path in FILES.items():

        file_status.append(
            {
                "Fichier": os.path.basename(path),
                "Statut": (
                    "Disponible"
                    if os.path.isfile(path)
                    else "Introuvable"
                )
            }
        )

    status_df = pd.DataFrame(
        file_status
    )

    st.dataframe(
        status_df,
        use_container_width=True,
        hide_index=True
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
        "Suivi et analyse des données liées à l'activité de transport."
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Camions",
            len(camions)
        )


    with col2:

        st.metric(
            "Chauffeurs",
            len(chauffeurs)
        )


    with col3:

        st.metric(
            "Ordres de mission",
            len(om)
        )


    st.markdown(
        '<div class="sub-title">🔎 Recherche dans les données</div>',
        unsafe_allow_html=True
    )


    search_text = st.text_input(
        "Rechercher",
        placeholder=(
            "Saisissez une référence, "
            "un camion, un client..."
        )
    )


    if search_text:

        datasets = {
            "Camions": camions,
            "Chauffeurs": chauffeurs,
            "Clients": clients,
            "Commandes": commandes,
            "Ordres de Mission": om
        }

        for name, df in datasets.items():

            if not df.empty:

                result = search_data(
                    df,
                    search_text
                )

                if not result.empty:

                    st.markdown(
                        f"### {name}"
                    )

                    show_table(
                        result,
                        f"transport_{name}"
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
            "Aucune donnée OM disponible."
        )

    else:

        st.write(
            f"Nombre de lignes : **{len(om)}**"
        )


        search_om = st.text_input(
            "🔎 Rechercher dans les Ordres de Mission",
            key="search_om"
        )


        filtered_om = search_data(
            om,
            search_om
        )


        filter_col1, filter_col2 = st.columns(2)


        with filter_col1:

            selected_column = st.selectbox(
                "Filtrer par colonne",
                ["Aucun"] + list(
                    filtered_om.columns
                ),
                key="om_filter_column"
            )


        with filter_col2:

            if (
                selected_column != "Aucun"
                and selected_column in filtered_om.columns
            ):

                values = (
                    filtered_om[
                        selected_column
                    ]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                selected_value = st.selectbox(
                    "Valeur",
                    ["Tous"] + sorted(values),
                    key="om_filter_value"
                )


                filtered_om = filter_data(
                    filtered_om,
                    selected_column,
                    selected_value
                )


        show_table(
            filtered_om,
            "om_table"
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
            "Le fichier Camions.xlsx est vide ou introuvable."
        )

    else:

        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Nombre de camions",
                len(camions)
            )


        with col2:

            st.metric(
                "Nombre de colonnes",
                len(camions.columns)
            )


        search_camions = st.text_input(
            "🔎 Rechercher un camion",
            key="search_camions"
        )


        filtered_camions = search_data(
            camions,
            search_camions
        )


        show_table(
            filtered_camions,
            "camions_table"
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
            "Le fichier Chauffeurs.xlsx est vide ou introuvable."
        )

    else:

        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Nombre de chauffeurs",
                len(chauffeurs)
            )


        with col2:

            st.metric(
                "Nombre de colonnes",
                len(chauffeurs.columns)
            )


        search_chauffeurs = st.text_input(
            "🔎 Rechercher un chauffeur",
            key="search_chauffeurs"
        )


        filtered_chauffeurs = search_data(
            chauffeurs,
            search_chauffeurs
        )


        show_table(
            filtered_chauffeurs,
            "chauffeurs_table"
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
            "Le fichier Clients.xlsx est vide ou introuvable."
        )

    else:

        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Nombre de clients",
                len(clients)
            )


        with col2:

            st.metric(
                "Nombre de colonnes",
                len(clients.columns)
            )


        search_clients = st.text_input(
            "🔎 Rechercher un client",
            key="search_clients"
        )


        filtered_clients = search_data(
            clients,
            search_clients
        )


        show_table(
            filtered_clients,
            "clients_table"
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
            "Le fichier Commande de vente.xlsx est vide ou introuvable."
        )

    else:

        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Commandes",
                len(commandes)
            )


        with col2:

            st.metric(
                "Nombre de colonnes",
                len(commandes.columns)
            )


        search_commandes = st.text_input(
            "🔎 Rechercher une commande",
            key="search_commandes"
        )


        filtered_commandes = search_data(
            commandes,
            search_commandes
        )


        show_table(
            filtered_commandes,
            "commandes_table"
        )


# ============================================================
# RAPPORTS
# ============================================================

elif menu == "📊 Rapports":

    st.markdown(
        '<div class="section-title">📊 Rapports</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="sub-title">📈 Synthèse générale</div>',
        unsafe_allow_html=True
    )


    report_data = pd.DataFrame(
        {
            "Indicateur": [
                "Camions",
                "Chauffeurs",
                "Clients",
                "Commandes de vente",
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
        report_data,
        use_container_width=True,
        hide_index=True
    )


    st.markdown(
        '<div class="sub-title">📋 Aperçu des données</div>',
        unsafe_allow_html=True
    )


    report_choice = st.selectbox(
        "Sélectionner les données à afficher",
        [
            "Camions",
            "Chauffeurs",
            "Clients",
            "Commandes de vente",
            "Ordres de Mission"
        ]
    )


    report_datasets = {
        "Camions": camions,
        "Chauffeurs": chauffeurs,
        "Clients": clients,
        "Commandes de vente": commandes,
        "Ordres de Mission": om
    }


    selected_report = report_datasets[
        report_choice
    ]


    if selected_report.empty:

        st.info(
            "Aucune donnée disponible."
        )

    else:

        report_search = st.text_input(
            "🔎 Rechercher",
            key="report_search"
        )


        selected_report = search_data(
            selected_report,
            report_search
        )


        show_table(
            selected_report,
            "report_table"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        © 2026 TMF Logistics — Gestion de la flotte

        <br>

        Transport & Logistique

    </div>
    """,
    unsafe_allow_html=True
)
