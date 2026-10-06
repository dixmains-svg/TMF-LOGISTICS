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
# DOSSIER DATA
# ============================================================

DATA_DIR = "Data"

FILES = {
    "Camions": os.path.join(DATA_DIR, "Camions.xlsx"),
    "Chauffeurs": os.path.join(DATA_DIR, "Chauffeurs.xlsx"),
    "Clients": os.path.join(DATA_DIR, "Clients.xlsx"),
    "Commandes": os.path.join(DATA_DIR, "Commande de vente.xlsx"),
    "OM": os.path.join(DATA_DIR, "OM.xlsx")
}


# ============================================================
# STYLE
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* HEADER */

.tmf-header {
    background: linear-gradient(
        135deg,
        #0b5d3b,
        #15915f
    );

    padding: 22px 30px;

    border-radius: 12px;

    color: white;

    margin-bottom: 25px;

    box-shadow:
        0 3px 10px rgba(0,0,0,0.12);
}

.tmf-header h1 {
    margin: 0;
    font-size: 32px;
}

.tmf-header p {
    margin-top: 5px;
    margin-bottom: 0;
    font-size: 15px;
}

/* TITRES */

.section-title {
    color: #0b5d3b;
    font-size: 24px;
    font-weight: 700;
    margin-top: 10px;
    margin-bottom: 20px;
}

/* CARTES */

.metric-card {
    background: white;

    padding: 18px;

    border-radius: 10px;

    border-left: 5px solid #15915f;

    box-shadow:
        0 2px 8px rgba(0,0,0,0.08);

    text-align: center;
}

.metric-title {
    color: #666;
    font-size: 14px;
}

.metric-value {
    color: #0b5d3b;
    font-size: 28px;
    font-weight: bold;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background-color: #f0f2f6;
}

/* BOUTONS */

.stButton > button {
    border-radius: 7px;
}

/* TABLE */

div[data-testid="stDataFrame"] {
    border-radius: 8px;
}

/* SEPARATION */

hr {
    margin-top: 20px;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# FONCTIONS EXCEL
# ============================================================

@st.cache_data
def get_sheets(file_path):

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
def read_excel(
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

        # Supprimer lignes vides
        df = df.dropna(
            axis=0,
            how="all"
        )

        # Supprimer colonnes vides
        df = df.dropna(
            axis=1,
            how="all"
        )

        # Nettoyer les noms des colonnes
        df.columns = [
            str(c).strip()
            for c in df.columns
        ]

        return df

    except Exception as e:

        return pd.DataFrame()


def load_file(
    file_path,
    preferred_sheet=None
):

    sheets = get_sheets(
        file_path
    )

    if not sheets:

        return pd.DataFrame(), []

    # Priorité à la feuille demandée
    if (
        preferred_sheet
        and preferred_sheet in sheets
    ):

        df = read_excel(
            file_path,
            preferred_sheet
        )

        return df, sheets

    # Sinon première feuille
    df = read_excel(
        file_path,
        sheets[0]
    )

    return df, sheets


def search_data(
    df,
    search
):

    if df.empty:
        return df

    if not search:
        return df

    search = str(
        search
    ).strip()

    if not search:
        return df

    mask = df.astype(str).apply(
        lambda col:
        col.str.contains(
            search,
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

    if (
        column == "Toutes les colonnes"
        or not value
    ):
        return df

    mask = df[column].astype(str).str.contains(
        value,
        case=False,
        na=False,
        regex=False
    )

    return df[mask]


def excel_download(df):

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


def show_data(
    df,
    height=500
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

camions, camions_sheets = load_file(
    FILES["Camions"]
)

chauffeurs, chauffeurs_sheets = load_file(
    FILES["Chauffeurs"],
    "Chauffeurs"
)

clients, clients_sheets = load_file(
    FILES["Clients"]
)

commandes, commandes_sheets = load_file(
    FILES["Commandes"]
)

# OM : priorité à Input OM fini
om, om_sheets = load_file(
    FILES["OM"],
    "Input OM fini"
)


# ============================================================
# SIDEBAR — UN SEUL MENU
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:10px 0 20px 0;
        ">
            <h2 style="
                color:#0b5d3b;
                margin-bottom:5px;
            ">
                🚚 TMF LOGISTICS
            </h2>

            <small>
                Transport & Logistique
            </small>
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

    st.caption(
        "TMF LOGISTICS"
    )

    st.caption(
        datetime.now().strftime(
            "%d/%m/%Y %H:%M"
        )
    )


# ============================================================
# HEADER
# ============================================================

st.markdown("""
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
""", unsafe_allow_html=True)


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

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:

        st.metric(
            "🚛 Camions",
            len(camions)
        )

    with c2:

        st.metric(
            "👨‍✈️ Chauffeurs",
            len(chauffeurs)
        )

    with c3:

        st.metric(
            "👥 Clients",
            len(clients)
        )

    with c4:

        st.metric(
            "📦 Commandes",
            len(commandes)
        )

    with c5:

        st.metric(
            "📋 OM",
            len(om)
        )

    st.markdown("---")

    # --------------------------------------------------------
    # ÉTAT DES FICHIERS
    # --------------------------------------------------------

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
            if os.path.exists(FILES["Camions"])
            else "❌ Introuvable",

            "✅ Disponible"
            if os.path.exists(FILES["Chauffeurs"])
            else "❌ Introuvable",

            "✅ Disponible"
            if os.path.exists(FILES["Clients"])
            else "❌ Introuvable",

            "✅ Disponible"
            if os.path.exists(FILES["Commandes"])
            else "❌ Introuvable",

            "✅ Disponible"
            if os.path.exists(FILES["OM"])
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

    # --------------------------------------------------------
    # GRAPHIQUE
    # --------------------------------------------------------

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
        """
        Cette section constitue le centre de gestion
        de l'activité transport.

        Les données disponibles sont :

        • 🚛 Camions
        • 👨‍✈️ Chauffeurs
        • 📋 Ordres de Mission
        • 👥 Clients
        • 📦 Commandes de vente
        """
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "🚛 Parc camions",
            len(camions)
        )

    with c2:

        st.metric(
            "👨‍✈️ Chauffeurs",
            len(chauffeurs)
        )

    with c3:

        st.metric(
            "📋 Ordres de Mission",
            len(om)
        )

    st.markdown("---")

    st.subheader(
        "📈 Données disponibles"
    )

    transport_data = pd.DataFrame({

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
        transport_data,
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

    if om.empty:

        st.error(
            "Aucune donnée trouvée dans OM.xlsx."
        )

    else:

        st.success(
            f"{len(om)} ligne(s) chargée(s)"
        )

        # Sélection de feuille
        if om_sheets:

            sheet = st.selectbox(
                "📄 Feuille",
                om_sheets,
                index=(
                    om_sheets.index(
                        "Input OM fini"
                    )
                    if "Input OM fini"
                    in om_sheets
                    else 0
                )
            )

            data = read_excel(
                FILES["OM"],
                sheet
            )

        else:

            data = om.copy()

        # Recherche
        search = st.text_input(
            "🔎 Rechercher dans les OM"
        )

        result = search_data(
            data,
            search
        )

        # Filtre
        if not result.empty:

            c1, c2 = st.columns(2)

            with c1:

                column = st.selectbox(
                    "Filtrer par",
                    [
                        "Toutes les colonnes"
                    ] + list(result.columns)
                )

            with c2:

                value = st.text_input(
                    "Valeur"
                )

            result = filter_data(
                result,
                column,
                value
            )

        st.write(
            f"**{len(result)} résultat(s)**"
        )

        show_data(
            result,
            600
        )

        if not result.empty:

            st.download_button(
                "⬇️ Exporter le rapport OM",
                data=excel_download(
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
            "Aucune donnée trouvée dans Camions.xlsx."
        )

    else:

        st.metric(
            "Nombre de lignes",
            len(camions)
        )

        if camions_sheets:

            sheet = st.selectbox(
                "📄 Feuille",
                camions_sheets
            )

            data = read_excel(
                FILES["Camions"],
                sheet
            )

        else:

            data = camions.copy()

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

        show_data(
            result
        )

        if not result.empty:

            st.download_button(
                "⬇️ Exporter Camions",
                data=excel_download(
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
            "Aucune donnée trouvée dans Chauffeurs.xlsx."
        )

    else:

        st.metric(
            "Nombre de chauffeurs",
            len(chauffeurs)
        )

        if chauffeurs_sheets:

            sheet = st.selectbox(
                "📄 Feuille",
                chauffeurs_sheets
            )

            data = read_excel(
                FILES["Chauffeurs"],
                sheet
            )

        else:

            data = chauffeurs.copy()

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

        show_data(
            result
        )

        if not result.empty:

            st.download_button(
                "⬇️ Exporter Chauffeurs",
                data=excel_download(
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
        '👥 Gestion des clients'
        '</div>',
        unsafe_allow_html=True
    )

    if clients.empty:

        st.error(
            "Aucune donnée trouvée dans Clients.xlsx."
        )

    else:

        st.metric(
            "Nombre de clients",
            len(clients)
        )

        if clients_sheets:

            sheet = st.selectbox(
                "📄 Feuille",
                clients_sheets
            )

            data = read_excel(
                FILES["Clients"],
                sheet
            )

        else:

            data = clients.copy()

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

        show_data(
            result
        )

        if not result.empty:

            st.download_button(
                "⬇️ Exporter Clients",
                data=excel_download(
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
            "Aucune donnée trouvée dans "
            "Commande de vente.xlsx."
        )

    else:

        st.metric(
            "Nombre de lignes",
            len(commandes)
        )

        if commandes_sheets:

            sheet = st.selectbox(
                "📄 Feuille",
                commandes_sheets
            )

            data = read_excel(
                FILES["Commandes"],
                sheet
            )

        else:

            data = commandes.copy()

        search = st.text_input(
            "🔎 Rechercher une commande"
        )

        result = search_data(
            data,
            search
        )

        if not result.empty:

            c1, c2 = st.columns(2)

            with c1:

                column = st.selectbox(
                    "Filtrer par",
                    [
                        "Toutes les colonnes"
                    ] + list(result.columns)
                )

            with c2:

                value = st.text_input(
                    "Valeur"
                )

            result = filter_data(
                result,
                column,
                value
            )

        st.write(
            f"**{len(result)} résultat(s)**"
        )

        show_data(
            result,
            600
        )

        if not result.empty:

            st.download_button(
                "⬇️ Exporter Commandes",
                data=excel_download(
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

    # --------------------------------------------------------
    # CHOIX DE LA SOURCE
    # --------------------------------------------------------

    source = st.selectbox(
        "📂 Choisir les données à analyser",
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

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "Lignes",
                len(data)
            )

        with c2:

            st.metric(
                "Colonnes",
                len(data.columns)
            )

        with c3:

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

        result = search_data(
            data,
            search
        )

        # ----------------------------------------------------
        # FILTRE
        # ----------------------------------------------------

        if not result.empty:

            c1, c2 = st.columns(2)

            with c1:

                column = st.selectbox(
                    "Filtrer par colonne",
                    [
                        "Toutes les colonnes"
                    ] + list(result.columns)
                )

            with c2:

                value = st.text_input(
                    "Valeur du filtre"
                )

            result = filter_data(
                result,
                column,
                value
            )

        # ----------------------------------------------------
        # TABLEAU
        # ----------------------------------------------------

        st.write(
            f"### Résultat : {len(result)} ligne(s)"
        )

        show_data(
            result,
            600
        )

        # ----------------------------------------------------
        # EXPORT
        # ----------------------------------------------------

        if not result.empty:

            st.download_button(
                "⬇️ Télécharger le rapport Excel",
                data=excel_download(
                    result
                ),
                file_name="TMF_Rapport.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                )
            )


# ============================================================
# FIN
# ============================================================

st.markdown("---")

st.caption(
    "TMF LOGISTICS • Gestion du transport et rapports"
)
