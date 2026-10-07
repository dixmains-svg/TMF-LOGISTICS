import streamlit as st
import pandas as pd
import os
import io
from datetime import datetime

# ============================================================
# CONFIGURATION DE LA PAGE
# ============================================================
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

# ============================================================
# STYLES CSS PERSONNALISÉS (DESIGN MODERNE)
# ============================================================
st.markdown(
    """
    <style>
    /* Marges principales */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    /* En-tête principal TMF */
    .tmf-header {
        background: linear-gradient(135deg, #0b5d3b 0%, #15915f 100%);
        padding: 25px 35px;
        border-radius: 14px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 6px 16px rgba(11, 93, 59, 0.2);
    }

    .tmf-header h1 {
        margin: 0;
        padding: 0;
        color: white;
        font-size: 32px;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    .tmf-header p {
        margin-top: 8px;
        margin-bottom: 0;
        color: #e0f2fe;
        font-size: 15px;
        opacity: 0.95;
    }

    /* Titres de section */
    .section-title {
        color: #0b5d3b;
        font-size: 24px;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Personnalisation de la Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }

    /* Style des cartes de métriques */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }

    /* Ajustement Dataframe */
    div[data-testid="stDataFrame"] {
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        overflow: hidden;
    }

    /* Bouton Télécharger */
    div.stDownloadButton > button {
        background-color: #0b5d3b;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 8px 16px;
        transition: background-color 0.2s ease;
    }
    
    div.stDownloadButton > button:hover {
        background-color: #15915f;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FONCTIONS UTILITAIRES & CHARGEMENT
# ============================================================

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

        df = df.dropna(axis=0, how="all")
        df = df.dropna(axis=1, how="all")

        df.columns = [
            str(column).strip()
            for column in df.columns
        ]

        return df

    except Exception:
        return pd.DataFrame()


def load_data(file_path, preferred_sheet=None):

    sheets = get_sheets(file_path)

    if not sheets:
        return pd.DataFrame(), []

    if preferred_sheet and preferred_sheet in sheets:
        return read_excel(file_path, preferred_sheet), sheets

    return read_excel(file_path, sheets[0]), sheets


def search_data(df, text):

    if df.empty or not text:
        return df

    text = str(text).strip()

    if not text:
        return df

    mask = df.astype(str).apply(
        lambda column: column.str.contains(
            text, case=False, na=False, regex=False
        )
    )

    return df[mask.any(axis=1)]


def filter_data(df, column, value):

    if df.empty:
        return df

    if column == "Toutes les colonnes" or not value:
        return df

    mask = (
        df[column]
        .astype(str)
        .str.contains(
            value, case=False, na=False, regex=False
        )
    )

    return df[mask]


def to_excel(df):

    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Rapport")

    return output.getvalue()


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


# ============================================================
# CHARGEMENT DES DONNÉES EN MÉMOIRE
# ============================================================

camions, camions_sheets = load_data(FILES["Camions"])
chauffeurs, chauffeurs_sheets = load_data(FILES["Chauffeurs"], "Chauffeurs")
clients, clients_sheets = load_data(FILES["Clients"])
commandes, commandes_sheets = load_data(FILES["Commandes"])
om, om_sheets = load_data(FILES["OM"], "Input OM fini")


# ============================================================
# MENU BARRE LATÉRALE (SIDEBAR)
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center; padding:10px 0 15px 0;">
            <div style="font-size:24px; font-weight:800; color:#0b5d3b; letter-spacing:-0.5px;">
                🚚 TMF LOGISTICS
            </div>
            <div style="margin-top:4px; color:#64748b; font-size:13px; font-weight:500;">
                Transport & Logistique
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    menu = st.radio(
        "NAVIGATION PRINCIPALE",
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

    st.caption("🟢 **Système Opérationnel**")
    st.caption(f"📅 Mise à jour : {datetime.now().strftime('%d/%m/%Y %H:%M')}")


# ============================================================
# EN-TÊTE PRINCIPAL (HEADER)
# ============================================================

st.markdown(
    """
    <div class="tmf-header">
        <h1>🚚 TMF LOGISTICS</h1>
        <p>Gestion du transport • Ordres de mission • Flotte & Chauffeurs • Suivi & Rapports</p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PAGE 1 : ACCUEIL / TABLEAU DE BORD
# ============================================================

if menu == "🏠 Accueil":

    st.markdown('<div class="section-title">🏠 Tableau de bord global</div>', unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("🚛 Camions", len(camions))

    with col2:
        st.metric("👨‍✈️ Chauffeurs", len(chauffeurs))

    with col3:
        st.metric("👥 Clients", len(clients))

    with col4:
        st.metric("📦 Commandes", len(commandes))

    with col5:
        st.metric("📋 Ordres Mission", len(om))

    st.markdown("---")

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("📁 Statut des fichiers de données")
        status = pd.DataFrame({
            "Source": ["Camions", "Chauffeurs", "Clients", "Commandes de vente", "Ordres de Mission"],
            "Fichier": ["Camions.xlsx", "Chauffeurs.xlsx", "Clients.xlsx", "Commande de vente.xlsx", "OM.xlsx"],
            "Statut": [
                "✅ Disponible" if os.path.exists(FILES["Camions"]) else "❌ Introuvable",
                "✅ Disponible" if os.path.exists(FILES["Chauffeurs"]) else "❌ Introuvable",
                "✅ Disponible" if os.path.exists(FILES["Clients"]) else "❌ Introuvable",
                "✅ Disponible" if os.path.exists(FILES["Commandes"]) else "❌ Introuvable",
                "✅ Disponible" if os.path.exists(FILES["OM"]) else "❌ Introuvable"
            ],
            "Lignes": [len(camions), len(chauffeurs), len(clients), len(commandes), len(om)]
        })
        st.dataframe(status, use_container_width=True, hide_index=True)

    with col_right:
        st.subheader("📊 Volume comparatif des données")
        graph = pd.DataFrame({
            "Source": ["Camions", "Chauffeurs", "Clients", "Commandes", "OM"],
            "Nombre": [len(camions), len(chauffeurs), len(clients), len(commandes), len(om)]
        })
        st.bar_chart(graph.set_index("Source"), color="#0b5d3b")


# ============================================================
# PAGE 2 : GESTION DU TRANSPORT
# ============================================================

elif menu == "🚚 Gestion du transport":

    st.markdown('<div class="section-title">🚚 Gestion globale du transport</div>', unsafe_allow_html=True)

    st.info("💡 Centre de contrôle principal pour la supervision des ressources de transport.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric
