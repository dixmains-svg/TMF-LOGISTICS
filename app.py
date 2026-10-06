import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime


# ============================================================
# CONFIGURATION STREAMLIT
# ============================================================

st.set_page_config(
    page_title="TMF LOGISTICS - Rapports",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #f4f6f8;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    .tmf-header {
        background: linear-gradient(
            135deg,
            #0b5d3b,
            #15915f
        );
        padding: 25px 30px;
        border-radius: 14px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }

    .tmf-header h1 {
        margin: 0;
        font-size: 32px;
        font-weight: 700;
    }

    .tmf-header p {
        margin-top: 6px;
        margin-bottom: 0;
        font-size: 15px;
    }

    .metric-card {
        background: white;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
        border-left: 5px solid #15915f;
    }

    .metric-title {
        color: #666666;
        font-size: 14px;
        margin-bottom: 5px;
    }

    .metric-value {
        color: #0b5d3b;
        font-size: 28px;
        font-weight: bold;
    }

    .section-title {
        color: #0b5d3b;
        font-size: 22px;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        padding: 12px;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.07);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DOSSIER DATA
# ============================================================

DATA_DIR = "Data"

CAMIONS_FILE = os.path.join(
    DATA_DIR,
    "Camions.xlsx"
)

CHAUFFEURS_FILE = os.path.join(
    DATA_DIR,
    "Chauffeurs.xlsx"
)

CLIENTS_FILE = os.path.join(
    DATA_DIR,
    "Clients.xlsx"
)

COMMANDES_FILE = os.path.join(
    DATA_DIR,
    "Commande de vente.xlsx"
)

OM_FILE = os.path.join(
    DATA_DIR,
    "OM.xlsx"
)


# ============================================================
# FONCTIONS
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
def load_excel(file_path, sheet_name=None):

    if not os.path.exists(file_path):
        return pd.DataFrame()

    try:

        # Lecture d'une feuille précise
        if sheet_name:

            df = pd.read_excel(
                file_path,
                sheet_name=sheet_name,
                engine="openpyxl"
            )

        else:

            # Première feuille
            df = pd.read_excel(
                file_path,
                engine="openpyxl"
            )

        # Suppression lignes vides
        df = df.dropna(
            axis=0,
            how="all"
        )

        # Suppression colonnes vides
        df = df.dropna(
            axis=1,
            how="all"
        )

        # Nettoyage colonnes
        df.columns = [
            str(col).strip()
            for col in df.columns
        ]

        return df

    except Exception:

        return pd.DataFrame()


def load_main_file(file_path, preferred_sheet=None):

    sheets = get_excel_sheets(
        file_path
    )

    if not sheets:
        return pd.DataFrame(), []

    # Feuille demandée disponible
    if (
        preferred_sheet
        and preferred_sheet in sheets
    ):

        df = load_excel(
            file_path,
            preferred_sheet
        )

        return df, sheets

    # Première feuille
    df = load_excel(
        file_path,
        sheets[0]
    )

    return df, sheets


def normalize_text(value):

    if pd.isna(value):
        return ""

    return str(value).strip().lower()


def search_dataframe(df, search_text):

    if df.empty:
        return df

    if not search_text:
        return df

    search_text = str(
        search_text
    ).strip().lower()

    mask = df.astype(str).apply(
        lambda column:
        column.str.lower().str.contains(
            search_text,
            na=False,
            regex=False
        )
    )

    return df[
        mask.any(axis=1)
    ]


def filter_dataframe(
    df,
    column,
    value
):

    if df.empty:
        return df

    if (
        column is None
        or column == "Toutes les colonnes"
        or not value
    ):
        return df

    mask = (
        df[column]
        .astype(str)
        .str.contains(
            value,
            case=False,
            na=False,
            regex=False
        )
    )

    return df[mask]


def dataframe_to_excel(df):

    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ):

        df.to_excel(
            output,
            index=False,
            sheet_name="Rapport"
        )

    return output.getvalue()


def show_table(
    df,
    title=None,
    height=500
):

    if title:
        st.markdown(
            f'<div class="section-title">{title}</div>',
            unsafe_allow_html=True
        )

    if df.empty:

        st.info(
            "Aucune donnée disponible."
        )

        return

    st.dataframe(
        df,
        use_container_width=True,
        height=height,
        hide_index=True
    )


def file_status(
    file_path
):

    return os.path.exists(
        file_path
    )


# ============================================================
# CHARGEMENT DES 5 SOURCES
# ============================================================

camions, camions_sheets = load_main_file(
    CAMIONS_FILE
)

chauffeurs, chauffeurs_sheets = load_main_file(
    CHAUFFEURS_FILE,
    "Chauffeurs"
)

clients, clients_sheets = load_main_file(
    CLIENTS_FILE
)

commandes, commandes_sheets = load_main_file(
    COMMANDES_FILE
)

# OM : priorité à Input OM fini
om, om_sheets = load_main_file(
    OM_FILE,
    "Input OM fini"
)


# ============================================================
# DICTIONNAIRE DES DONNÉES
# ============================================================

DATASETS = {

    "Camions": {
        "file": CAMIONS_FILE,
        "data": camions,
        "sheets": camions_sheets
    },

    "Chauffeurs": {
        "file": CHAUFFEURS_FILE,
        "data": chauffeurs,
        "sheets": chauffeurs_sheets
    },

    "Clients": {
        "file": CLIENTS_FILE,
        "data": clients,
        "sheets": clients_sheets
    },

    "Commandes de vente": {
        "file": COMMANDES_FILE,
        "data": commandes,
        "sheets": commandes_sheets
    },

    "Ordres de mission": {
        "file": OM_FILE,
        "data": om,
        "sheets": om_sheets
    }
}


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="tmf-header">

        <h1>🚚 TMF LOGISTICS</h1>

        <p>
            Rapports • Transport • Exploitation •
            Planification • Suivi
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    "## 🚚 TMF LOGISTICS"
)

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "MENU PRINCIPAL",
    [
        "🏠 Tableau de bord",
        "📋 Ordres de mission",
        "🚛 Camions",
        "👨‍✈️ Chauffeurs",
        "🏢 Clients",
        "📦 Commandes de vente",
        "🔎 Recherche globale",
        "📊 Analyse",
        "⚙️ Données"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Application de suivi "
    "et de reporting transport"
)

st.sidebar.caption(
    "Dernière ouverture : "
    + datetime.now().strftime(
        "%d/%m/%Y %H:%M"
    )
)


# ============================================================
# TABLEAU DE BORD
# ============================================================

if menu == "🏠 Tableau de bord":

    st.markdown(
        '<div class="section-title">'
        '📊 Tableau de bord'
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
            "🏢 Clients",
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
    # ÉTAT DES FICHIERS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '📁 État des fichiers'
        '</div>',
        unsafe_allow_html=True
    )

    status_data = []

    for name, info in DATASETS.items():

        df = info["data"]

        status_data.append(
            {
                "Source": name,

                "Fichier": os.path.basename(
                    info["file"]
                ),

                "Statut":
                    "✅ Disponible"
                    if file_status(info["file"])
                    else "❌ Introuvable",

                "Lignes":
                    len(df),

                "Colonnes":
                    len(df.columns),

                "Feuilles":
                    len(info["sheets"])
            }
        )

    status_df = pd.DataFrame(
        status_data
    )

    st.dataframe(
        status_df,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # GRAPHIQUE
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '📈 Volume des données'
        '</div>',
        unsafe_allow_html=True
    )

    chart_df = pd.DataFrame(
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

    chart_df = chart_df.set_index(
        "Source"
    )

    st.bar_chart(
        chart_df
    )


# ============================================================
# ORDRES DE MISSION
# ============================================================

elif menu == "📋 Ordres de mission":

    st.markdown(
        '<div class="section-title">'
        '📋 Ordres de mission'
        '</div>',
        unsafe_allow_html=True
    )

    if om.empty:

        st.error(
            "Aucune donnée OM disponible."
        )

    else:

        st.success(
            f"{len(om)} ligne(s) chargée(s) "
            f"depuis OM.xlsx"
        )

        # ----------------------------------------------------
        # FEUILLE
        # ----------------------------------------------------

        if om_sheets:

            selected_sheet = st.selectbox(
                "📄 Feuille",
                om_sheets,
                index=(
                    om_sheets.index("Input OM fini")
                    if "Input OM fini" in om_sheets
                    else 0
                )
            )

            om_view = load_excel(
                OM_FILE,
                selected_sheet
            )

        else:

            om_view = om.copy()

        # ----------------------------------------------------
        # RECHERCHE
        # ----------------------------------------------------

        search = st.text_input(
            "🔎 Rechercher dans les OM"
        )

        result = search_dataframe(
            om_view,
            search
        )

        # ----------------------------------------------------
        # FILTRE
        # ----------------------------------------------------

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

        show_table(
            result,
            height=550
        )

        # ----------------------------------------------------
        # EXPORT
        # ----------------------------------------------------

        if not result.empty:

            st.download_button(
                "⬇️ Télécharger le rapport OM",
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
        '🚛 Gestion des camions'
        '</div>',
        unsafe_allow_html=True
    )

    if camions.empty:

        st.error(
            "Camions.xlsx est vide "
            "ou introuvable."
        )

    else:

        st.success(
            f"{len(camions)} ligne(s) "
            "chargée(s)"
        )

        # ----------------------------------------------------
        # FEUILLES
        # ----------------------------------------------------

        if camions_sheets:

            sheet = st.selectbox(
                "📄 Feuille",
                camions_sheets,
                key="camions_sheet"
            )

            data = load_excel(
                CAMIONS_FILE,
                sheet
            )

        else:

            data = camions.copy()

        # ----------------------------------------------------
        # RECHERCHE
        # ----------------------------------------------------

        search = st.text_input(
            "🔎 Rechercher un camion",
            key="search_camions"
        )

        result = search_dataframe(
            data,
            search
        )

        # ----------------------------------------------------
        # TABLE
        # ----------------------------------------------------

        st.write(
            f"**{len(result)} résultat(s)**"
        )

        show_table(
            result
        )

        if not result.empty:

            st.download_button(
                "⬇️ Télécharger Camions",
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
        '👨‍✈️ Gestion des chauffeurs'
        '</div>',
        unsafe_allow_html=True
    )

    if chauffeurs.empty:

        st.error(
            "Chauffeurs.xlsx est vide "
            "ou introuvable."
        )

    else:

        st.success(
            f"{len(chauffeurs)} chauffeur(s)"
        )

        if chauffeurs_sheets:

            sheet = st.selectbox(
                "📄 Feuille",
                chauffeurs_sheets,
                key="chauffeurs_sheet"
            )

            data = load_excel(
                CHAUFFEURS_FILE,
                sheet
            )

        else:

            data = chauffeurs.copy()

        search = st.text_input(
            "🔎 Rechercher un chauffeur",
            key="search_chauffeurs"
        )

        result = search_dataframe(
            data,
            search
        )

        st.write(
            f"**{len(result)} résultat(s)**"
        )

        show_table(
            result
        )

        if not result.empty:

            st.download_button(
                "⬇️ Télécharger Chauffeurs",
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

elif menu == "🏢 Clients":

    st.markdown(
        '<div class="section-title">'
        '🏢 Gestion des clients'
        '</div>',
        unsafe_allow_html=True
    )

    if clients.empty:

        st.error(
            "Clients.xlsx est vide "
            "ou introuvable."
        )

    else:

        st.success(
            f"{len(clients)} client(s)"
        )

        if clients_sheets:

            sheet = st.selectbox(
                "📄 Feuille",
                clients_sheets,
                key="clients_sheet"
            )

            data = load_excel(
                CLIENTS_FILE,
                sheet
            )

        else:

            data = clients.copy()

        search = st.text_input(
            "🔎 Rechercher un client",
            key="search_clients"
        )

        result = search_dataframe(
            data,
            search
        )

        st.write(
            f"**{len(result)} résultat(s)**"
        )

        show_table(
            result
        )

        if not result.empty:

            st.download_button(
                "⬇️ Télécharger Clients",
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

    if commandes.empty:

        st.error(
            "Commande de vente.xlsx est vide "
            "ou introuvable."
        )

    else:

        st.success(
            f"{len(commandes)} ligne(s) chargée(s)"
        )

        if commandes_sheets:

            sheet = st.selectbox(
                "📄 Feuille",
                commandes_sheets,
                key="commandes_sheet"
            )

            data = load_excel(
                COMMANDES_FILE,
                sheet
            )

        else:

            data = commandes.copy()

        search = st.text_input(
            "🔎 Rechercher une commande",
            key="search_commandes"
        )

        result = search_dataframe(
            data,
            search
        )

        # ----------------------------------------------------
        # FILTRE COLONNE
        # ----------------------------------------------------

        if not result.empty:

            col1, col2 = st.columns(2)

            with col1:

                filter_column = st.selectbox(
                    "Filtrer par",
                    [
                        "Toutes les colonnes"
                    ] + list(result.columns),
                    key="commande_filter_col"
                )

            with col2:

                filter_value = st.text_input(
                    "Valeur",
                    key="commande_filter_value"
                )

            result = filter_dataframe(
                result,
                filter_column,
                filter_value
            )

        st.write(
            f"**{len(result)} résultat(s)**"
        )

        show_table(
            result,
            height=550
        )

        if not result.empty:

            st.download_button(
                "⬇️ Télécharger Commandes",
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
# RECHERCHE GLOBALE
# ============================================================

elif menu == "🔎 Recherche globale":

    st.markdown(
        '<div class="section-title">'
        '🔎 Recherche globale TMF'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Recherchez un camion, chauffeur, client, "
        "commande, OM ou toute autre information."
    )

    search = st.text_input(
        "🔎 Recherche",
        placeholder=(
            "Exemple : TR301, client, OM, commande..."
        )
    )

    if search:

        all_results = []

        for name, info in DATASETS.items():

            df = info["data"]

            if df.empty:
                continue

            result = search_dataframe(
                df,
                search
            )

            if not result.empty:

                result = result.copy()

                result.insert(
                    0,
                    "SOURCE",
                    name
                )

                all_results.append(
                    result
                )

        if all_results:

            final_result = pd.concat(
                all_results,
                ignore_index=True
            )

            st.success(
                f"{len(final_result)} résultat(s) trouvé(s)."
            )

            show_table(
                final_result,
                height=600
            )

            st.download_button(
                "⬇️ Télécharger les résultats",
                data=dataframe_to_excel(
                    final_result
                ),
                file_name="TMF_Recherche_Globale.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                )
            )

        else:

            st.warning(
                "Aucun résultat trouvé."
            )


# ============================================================
# ANALYSE
# ============================================================

elif menu == "📊 Analyse":

    st.markdown(
        '<div class="section-title">'
        '📊 Analyse des données'
        '</div>',
        unsafe_allow_html=True
    )

    source_name = st.selectbox(
        "Choisir une source",
        list(DATASETS.keys())
    )

    data = DATASETS[
        source_name
    ]["data"]

    if data.empty:

        st.warning(
            "Cette source ne contient aucune donnée."
        )

    else:

        st.write(
            f"### Analyse : {source_name}"
        )

        # ----------------------------------------------------
        # INFORMATIONS
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
                data.shape[0] * data.shape[1]
            )

        # ----------------------------------------------------
        # COLONNES
        # ----------------------------------------------------

        st.markdown("### 📋 Colonnes")

        columns_info = []

        for col in data.columns:

            columns_info.append(
                {
                    "Colonne": col,

                    "Type":
                        str(data[col].dtype),

                    "Valeurs":
                        data[col].notna().sum(),

                    "Vides":
                        data[col].isna().sum(),

                    "Valeurs uniques":
                        data[col].nunique()
                }
            )

        info_df = pd.DataFrame(
            columns_info
        )

        show_table(
            info_df,
            height=450
        )

        # ----------------------------------------------------
        # ANALYSE NUMÉRIQUE
        # ----------------------------------------------------

        numeric_cols = data.select_dtypes(
            include="number"
        ).columns.tolist()

        if numeric_cols:

            st.markdown(
                "### 📈 Analyse numérique"
            )

            selected_numeric = st.selectbox(
                "Choisir une colonne",
                numeric_cols
            )

            series = pd.to_numeric(
                data[selected_numeric],
                errors="coerce"
            ).dropna()

            if not series.empty:

                c1, c2, c3, c4 = st.columns(4)

                with c1:

                    st.metric(
                        "Total",
                        f"{series.sum():,.2f}"
                    )

                with c2:

                    st.metric(
                        "Moyenne",
                        f"{series.mean():,.2f}"
                    )

                with c3:

                    st.metric(
                        "Minimum",
                        f"{series.min():,.2f}"
                    )

                with c4:

                    st.metric(
                        "Maximum",
                        f"{series.max():,.2f}"
                    )

                chart = pd.DataFrame(
                    {
                        selected_numeric:
                            series.reset_index(
                                drop=True
                            )
                    }
                )

                st.line_chart(
                    chart
                )


# ============================================================
# DONNÉES
# ============================================================

elif menu == "⚙️ Données":

    st.markdown(
        '<div class="section-title">'
        '⚙️ Gestion des données'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # TABLEAU DES FICHIERS
    # --------------------------------------------------------

    rows = []

    for name, info in DATASETS.items():

        rows.append(
            {
                "Source": name,

                "Fichier":
                    os.path.basename(
                        info["file"]
                    ),

                "Existe":
                    "Oui"
                    if os.path.exists(
                        info["file"]
                    )
                    else "Non",

                "Feuilles":
                    ", ".join(
                        info["sheets"]
                    ),

                "Lignes":
                    len(info["data"]),

                "Colonnes":
                    len(info["data"].columns)
            }
        )

    files_df = pd.DataFrame(
        rows
    )

    show_table(
        files_df,
        height=400
    )

    # --------------------------------------------------------
    # EXPLORATION DES COLONNES
    # --------------------------------------------------------

    st.markdown(
        "### 📋 Structure des fichiers"
    )

    source = st.selectbox(
        "Choisir le fichier",
        list(DATASETS.keys()),
        key="structure_source"
    )

    selected_data = DATASETS[
        source
    ]["data"]

    if not selected_data.empty:

        structure = pd.DataFrame(
            {
                "N°": range(
                    1,
                    len(selected_data.columns) + 1
                ),

                "Nom de colonne":
                    selected_data.columns,

                "Type":
                    [
                        str(
                            selected_data[col].dtype
                        )
                        for col in selected_data.columns
                    ],

                "Valeurs":
                    [
                        selected_data[col].notna().sum()
                        for col in selected_data.columns
                    ],

                "Vides":
                    [
                        selected_data[col].isna().sum()
                        for col in selected_data.columns
                    ],

                "Uniques":
                    [
                        selected_data[col].nunique()
                        for col in selected_data.columns
                    ]
            }
        )

        show_table(
            structure,
            height=500
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#777;">
        <b>TMF LOGISTICS</b><br>
        Application de rapports et suivi transport
    </div>
    """,
    unsafe_allow_html=True
)
