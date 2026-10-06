import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime

st.set_page_config(
    page_title="TMF LOGISTICS",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_DIR = "Data"

FILES = {
    "Camions": os.path.join(DATA_DIR, "Camions.xlsx"),
    "Chauffeurs": os.path.join(DATA_DIR, "Chauffeurs.xlsx"),
    "Clients": os.path.join(DATA_DIR, "Clients.xlsx"),
    "Commandes": os.path.join(DATA_DIR, "Commande de vente.xlsx"),
    "OM": os.path.join(DATA_DIR, "OM.xlsx")
}

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    .tmf-header {
        background: linear-gradient(135deg, #0b5d3b, #15915f);
        padding: 25px 35px;
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
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

    .section-title {
        color: #0b5d3b;
        font-size: 24px;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 20px;
    }

    section[data-testid="stSidebar"] {
        background-color: #f0f2f6;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


@st.cache_data
def get_sheets(file_path):

    if not os.path.exists(file_path):
        return []

    try:
        return pd.ExcelFile(
            file_path,
            engine="openpyxl"
        ).sheet_names
    except Exception:
        return []


@st.cache_data
def read_excel(file_path, sheet_name=None):

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

        df = df.dropna(
            axis=0,
            how="all"
        )

        df = df.dropna(
            axis=1,
            how="all"
        )

        df.columns = [
            str(column).strip()
            for column in df.columns
        ]

        return df

    except Exception:
        return pd.DataFrame()


def load_data(
    file_path,
    preferred_sheet=None
):

    sheets = get_sheets(file_path)

    if not sheets:
        return pd.DataFrame(), []

    if (
        preferred_sheet
        and preferred_sheet in sheets
    ):

        return (
            read_excel(
                file_path,
                preferred_sheet
            ),
            sheets
        )

    return (
        read_excel(
            file_path,
            sheets[0]
        ),
        sheets
    )


def search_data(
    df,
    text
):

    if df.empty:
        return df

    if not text:
        return df

    text = str(text).strip()

    if not text:
        return df

    mask = df.astype(str).apply(
        lambda column:
        column.str.contains(
            text,
            case=False,
            na=False,
            regex=False
        )
    )

    return df[
        mask.any(axis=1)
    ]


def filter_data(
    df,
    column,
    value
):

    if df.empty:
        return df

    if column == "Toutes les colonnes":
        return df

    if not value:
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


def to_excel(df):

    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Rapport"
        )

    return output.getvalue()


def show_table(
    df,
    height=600
):

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


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

camions, camions_sheets = load_data(
    FILES["Camions"]
)

chauffeurs, chauffeurs_sheets = load_data(
    FILES["Chauffeurs"],
    "Chauffeurs"
)

clients, clients_sheets = load_data(
    FILES["Clients"]
)

commandes, commandes_sheets = load_data(
    FILES["Commandes"]
)

om, om_sheets = load_data(
    FILES["OM"],
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

    menu = st.radio(
        "MENU PRINCIPAL",
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

    st.caption("TMF LOGISTICS")

    st.caption(
        datetime.now().strftime(
            "%d/%m/%Y %H:%M"
        )
    )


# ============================================================
# HEADER
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

    st.subheader(
        "📁 État des données"
    )

    status = pd.DataFrame({

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

            "✅ Disponible"
            if os.path.exists(
                FILES["Camions"]
            )
            else "❌ Introuvable",

            "✅ Disponible"
            if os.path.exists(
                FILES["Chauffeurs"]
            )
            else "❌ Introuvable",

            "✅ Disponible"
            if os.path.exists(
                FILES["Clients"]
            )
            else "❌ Introuvable",

            "✅ Disponible"
            if os.path.exists(
                FILES["Commandes"]
            )
            else "❌ Introuvable",

            "✅ Disponible"
            if os.path.exists(
                FILES["OM"]
            )
            else "❌ Introuvable"
        ],

        "Lignes": [
            len(camions),
            len(chauffeurs),
            len(clients),
            len(commandes),
            len(om)
        ]
    })

    st.dataframe(
        status,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    st.subheader(
        "📊 Volume des données"
    )

    graph = pd.DataFrame({

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
    })

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
        "Centre de gestion de l'activité transport."
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
        "📊 Synthèse"
    )

    synthese = pd.DataFrame({

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
    })

    st.dataframe(
        synthese,
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

        index = 0

        if "Input OM fini" in om_sheets:

            index = om_sheets.index(
                "Input OM fini"
            )

        sheet = st.selectbox(
            "📄 Feuille",
            om_sheets,
            index=index
        )

        data = read_excel(
            FILES["OM"],
            sheet
        )

        st.success(
            f"{len(data)} ligne(s) chargée(s)"
        )

        search = st.text_input(
            "🔎 Rechercher dans les OM"
        )

        result = search_data(
            data,
            search
        )

        if not result.empty:

            col1, col2 = st.columns(2)

            with col1:

                column = st.selectbox(
                    "Filtrer par colonne",
                    [
                        "Toutes les colonnes"
                    ]
                    + list(result.columns)
                )

            with col2:

                value = st.text_input(
                    "Valeur du filtre"
                )

            result = filter_data(
                result,
                column,
                value
            )

        st.write(
            f"**{len(result)} résultat(s)**"
        )

        show_table(
            result
        )

        if not result.empty:

            st.download_button(
                "⬇️ Télécharger le rapport OM",
                to_excel(result),
                "TMF_Rapport_OM.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
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

        data = read_excel(
            FILES["Camions"],
            sheet
        )

        st.metric(
            "Nombre de lignes",
            len(data)
        )

        search = st.text_input(
            "🔎 Rechercher un camion"
        )

        result = search_data(
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
                "⬇️ Télécharger les camions",
                to_excel(result),
                "TMF_Camions.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
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

        index = 0

        if "Chauffeurs" in chauffeurs_sheets:

            index = chauffeurs_sheets.index(
                "Chauffeurs"
            )

        sheet = st.selectbox(
            "📄 Feuille",
            chauffeurs_sheets,
            index=index
        )

        data = read_excel(
            FILES["Chauffeurs"],
            sheet
        )

        st.metric(
            "Nombre de lignes",
            len(data)
        )

        search = st.text_input(
            "🔎 Rechercher un chauffeur"
        )

        result = search_data(
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
                "⬇️ Télécharger les chauffeurs",
                to_excel(result),
                "TMF_Chauffeurs.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
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

        data = read_excel(
            FILES["Clients"],
            sheet
        )

        st.metric(
            "Nombre de lignes",
            len(data)
        )

        search = st.text_input(
            "🔎 Rechercher un client"
        )

        result = search_data(
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
                "⬇️ Télécharger les clients",
                to_excel(result),
                "TMF_Clients.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
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
            "Impossible de lire Commande de vente.xlsx."
        )

    else:

        sheet = st.selectbox(
            "📄 Feuille",
            commandes_sheets
        )

        data = read_excel(
            FILES["Commandes"],
            sheet
        )

        st.metric(
            "Nombre de lignes",
            len(data)
        )

        search = st.text_input(
            "🔎 Rechercher une commande"
        )

        result = search_data(
            data,
            search
        )

        if not result.empty:

            col1, col2 = st.columns(2)

            with col1:

                column = st.selectbox(
                    "Filtrer par colonne",
                    [
                        "Toutes les colonnes"
                    ]
                    + list(result.columns)
                )

            with col2:

                value = st.text_input(
                    "Valeur du filtre"
                )

            result = filter_data(
                result,
                column,
                value
            )

        st.write(
            f"**{len(result)} résultat(s)**"
        )

        show_table(
            result
        )

        if not result.empty:

            st.download_button(
                "⬇️ Télécharger les commandes",
                to_excel(result),
                "TMF_Commandes_Vente.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
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
        "📂 Choisir les données",
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
                data.shape[0]
                * data.shape[1]
            )

        st.markdown("---")

        search = st.text_input(
            "🔎 Rechercher dans le rapport"
        )

        result = search_data(
            data,
            search
        )

        if not result.empty:

            col1, col2 = st.columns(2)

            with col1:

                column = st.selectbox(
                    "Filtrer par colonne",
                    [
                        "Toutes les colonnes"
                    ]
                    + list(result.columns)
                )

            with col2:

                value = st.text_input(
                    "Valeur du filtre"
                )

            result = filter_data(
                result,
                column,
                value
            )

        st.subheader(
            f"Résultat : {len(result)} ligne(s)"
        )

        show_table(
            result
        )

        if not result.empty:

            st.download_button(
                "⬇️ Télécharger le rapport Excel",
                to_excel(result),
                "TMF_Rapport.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
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
        Application de gestion du transport et de reporting
    </div>
    """,
    unsafe_allow_html=True
)
