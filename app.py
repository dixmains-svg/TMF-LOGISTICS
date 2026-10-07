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

FILES = {
    "camions": os.path.join(DATA_DIR, "Camions.xlsx"),
    "chauffeurs": os.path.join(DATA_DIR, "Chauffeurs.xlsx"),
    "clients": os.path.join(DATA_DIR, "Clients.xlsx"),
    "commandes": os.path.join(DATA_DIR, "Commande de vente.xlsx"),
    "om": os.path.join(DATA_DIR, "OM.xlsx")
}

# ============================================================
# DONNÉES CHIFFRE D'AFFAIRES (CA PAR SECTION)
# ============================================================

CA_DATA = {
    "CA PAR SECTION": ["BACHE", "CELLULE", "PORTE", "MANUTENTION", "LOCAT CHAMB FROIDE", "CAMION BENNE"],
    "Janvier": [65790896, 26872885, 18541291, 1175393, 3500000, 183070],
    "Février": [70823963, 28267513, 15974862, 1786342, 3780000, 183070],
    "Mars": [71277544, 26882050, 15629191, 1531753, 3780000, 183070],
    "Avril": [77027604, 17865590, 19240045, 1701066, 4266000, 183070],
    "Mai": [78494854, 25301009, 17853736, 1308388, 4266000, 183070],
    "Juin": [84376783, 22643195, 18068699, 1688118, 4266000, 183070],
    "Juillet": [84697674, 23774702, 20280769, 1933157, 4266000, 183070],
    "Août": [72111796, 27935676, 16775939, 1329655, 4266000, 183070],
    "Septembre": [71257015, 28800241, 15249130, 1360031, 4266000, 183070],
    "Octobre": [73247943, 27140775, 20891640, 1792889, 4266000, 183070],
    "Novembre": [68137126, 23562378, 23882778, 1574037, 4266000, 183070],
    "Décembre": [70880695, 26275402, 19988767, 1575652, 4266000, 183070],
    "GLOBAL": [888123893, 305321416, 222376847, 18756481, 49454000, 2196840]
}

df_ca = pd.DataFrame(CA_DATA)

# ============================================================
# STYLE CSS CUSTOM
# ============================================================

st.markdown("""
<style>
.main { background-color: #f7f9f8; }
.block-container { padding-top: 1rem; padding-bottom: 2rem; }

section[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #dfe7e3;
}

div[role="radiogroup"] label {
    border-radius: 8px;
    padding: 8px 10px;
    transition: 0.2s;
}

div[role="radiogroup"] label:hover {
    background-color: #eaf5ef;
}

.tmf-header {
    background: linear-gradient(135deg, #087443, #0b5d3b);
    border-radius: 12px;
    padding: 20px 25px;
    margin-bottom: 22px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.08);
}

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

.info-card {
    background-color: white;
    border-radius: 12px;
    padding: 18px;
    border: 1px solid #e1e8e4;
    box-shadow: 0 2px 7px rgba(0,0,0,0.05);
    min-height: 110px;
}

.info-card-title { font-size: 14px; color: #777; margin-bottom: 8px; }
.info-card-value { font-size: 24px; font-weight: 700; color: #0b5d3b; }

.stButton > button {
    border-radius: 8px;
    border: 1px solid #0b5d3b;
    font-weight: 600;
}

.footer {
    text-align: center;
    color: #777;
    font-size: 12px;
    margin-top: 35px;
    padding-top: 15px;
    border-top: 1px solid #ddd;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# LECTURE ET CACHE
# ============================================================

@st.cache_data
def get_sheets(file_path):
    try:
        if not os.path.isfile(file_path):
            return []
        excel_file = pd.ExcelFile(file_path, engine="openpyxl")
        return excel_file.sheet_names
    except Exception:
        return []

@st.cache_data
def read_excel(file_path, sheet_name=0):
    try:
        if not os.path.isfile(file_path):
            return pd.DataFrame()
        return pd.read_excel(file_path, sheet_name=sheet_name, engine="openpyxl")
    except Exception:
        return pd.DataFrame()

def load_data(file_path, preferred_sheet=None):
    if not os.path.isfile(file_path):
        return pd.DataFrame()
    sheets = get_sheets(file_path)
    if not sheets:
        return pd.DataFrame()
    if preferred_sheet and preferred_sheet in sheets:
        return read_excel(file_path, preferred_sheet)
    return read_excel(file_path, sheets[0])

# ============================================================
# FONCTIONS UTILITAIRES
# ============================================================

def search_data(df, search_text):
    if df.empty or not search_text:
        return df
    search_text = str(search_text).lower().strip()
    mask = (
        df.astype(str)
        .apply(lambda column: column.str.lower().str.contains(search_text, na=False))
        .any(axis=1)
    )
    return df[mask]

def filter_data(df, column, value):
    if df.empty or column not in df.columns or value in ["Tous", "", None]:
        return df
    return df[df[column].astype(str) == str(value)]

def dataframe_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Données")
    return output.getvalue()

def show_table(df, key):
    if df.empty:
        st.info("Aucune donnée disponible.")
        return

    st.dataframe(df, use_container_width=True, hide_index=True, key=key)

    excel_data = dataframe_to_excel(df)
    st.download_button(
        label="📥 Télécharger Excel",
        data=excel_data,
        file_name="export_tmf_logistics.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key=f"download_{key}"
    )

def format_currency(amount):
    return f"{amount:,.0f} DA".replace(",", " ")

# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

camions = load_data(FILES["camions"])
chauffeurs = load_data(FILES["chauffeurs"], "Chauffeurs")
clients = load_data(FILES["clients"])
commandes = load_data(FILES["commandes"])
om = load_data(FILES["om"], "Input OM fini")

nb_camions = len(camions)
nb_chauffeurs = len(chauffeurs)
nb_clients = len(clients)
nb_commandes =
