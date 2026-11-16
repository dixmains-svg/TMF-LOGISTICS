import io
import os
from datetime import datetime
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ============================================================
# CONFIGURATION DE LA PAGE
# ============================================================

st.set_page_config(
    page_title="Analytics & Rapport Croisé — TMF Logistics",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CHEMINS DES FICHIERS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "Data")
LOGO_FILE = os.path.join(BASE_DIR, "logo.png")

FILES = {
    "camions": os.path.join(DATA_DIR, "Camions.xlsx"),
    "chauffeurs": os.path.join(DATA_DIR, "Chauffeurs.xlsx"),
    "clients": os.path.join(DATA_DIR, "Clients.xlsx"),
    "commandes": os.path.join(DATA_DIR, "Commande de vente.xlsx"),
    "om": os.path.join(DATA_DIR, "OM.xlsx"),
}

# ============================================================
# DONNÉES CHIFFRE D'AFFAIRES PRÉVISIONNEL (À RÉALISER)
# ============================================================

CA_DATA = {
    "CA PAR SECTION": [
        "BACHE",
        "FRIGO",
        "PORTE",
        "MANUTENTION",
        "LOCAT CHAMB FROIDE",
        "CAMION BENNE",
    ],
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
}

df_ca_raw = pd.DataFrame(CA_DATA)
df_ca_raw["GLOBAL"] = df_ca_raw.drop(columns=["CA PAR SECTION"]).sum(axis=1)

# ============================================================
# STYLE CSS CUSTOM
# ============================================================

st.markdown(
    """
<style>
.main { background-color: #f8faf9; }
.block-container { padding-top: 1rem; padding-bottom: 2rem; }

section[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #dfe7e3;
}

.tmf-header {
    background: linear-gradient(135deg, #087443, #0b5d3b);
    border-radius: 12px;
    padding: 20px 25px;
    margin-bottom: 22px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.section-title {
    font-size: 24px;
    font-weight: 800;
    color: #000000;
    margin-top: 15px;
    margin-bottom: 15px;
}

.sub-title {
    font-size: 18px;
    font-weight: 600;
    color: #0b5d3b;
    margin-top: 20px;
    margin-bottom: 10px;
}

.kpi-card {
    background-color: white;
    border-radius: 10px;
    padding: 15px;
    border-left: 5px solid #087443;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    margin-bottom: 10px;
}

.kpi-title { font-size: 13px; color: #666; font-weight: 600; text-transform: uppercase; }
.kpi-value { font-size: 22px; font-weight: 700; color: #0b5d3b; margin-top: 4px; }
.kpi-sub { font-size: 11px; color: #888; margin-top: 2px; }

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
    unsafe_allow_html=True,
)

# ============================================================
# FONCTIONS UTILITAIRES & CACHE
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
    except Exception as e:
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

def find_column_by_keywords(df, keywords):
    if df is None or df.empty:
        return None
    for col in df.columns:
        col_str = str(col).lower()
        if any(kw in col_str for kw in keywords):
            return col
    return None

def extract_unique_options(df, keywords):
    if df is None or df.empty:
        return []
    col = find_column_by_keywords(df, keywords)
    if col:
        vals = df[col].dropna().astype(str).str.strip().unique().tolist()
        vals = [v for v in vals if v and v.lower() != "nan"]
        return sorted(vals)
    return []

def apply_text_filter(df, keywords, selected_value):
    if df is None or df.empty or not selected_value or selected_value == "Tous":
        return df
    col = find_column_by_keywords(df, keywords)
    if col:
        return df[df[col].astype(str).str.strip() == str(selected_value).strip()]
    return df

def format_currency(amount, currency="DA"):
    return f"{amount:,.2f} {currency}".replace(",", " ").replace(".", ",")

def kpi_card(title, value, subtext="", color="#087443"):
    st.markdown(
        f"""
    <div class="kpi-card" style="border-left-color: {color};">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{subtext}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

def show_table(df, key):
    if df is None or df.empty:
        st.info("Aucune donnée disponible pour cette sélection.")
        return
    st.dataframe(df, use_container_width=True, key=key)

# ============================================================
# CHARGEMENT DES BASES DE DONNÉES
# ============================================================

camions = load_data(FILES["camions"])
chauffeurs = load_data(FILES["chauffeurs"], "Chauffeurs")
clients = load_data(FILES["clients"])
commandes = load_data(FILES["commandes"])
om = load_data(FILES["om"], "Input OM fini")

# ============================================================
# STANDARDISATION / ENRICHISSEMENT DES CLIENTS & FUSION PAR OM
# ============================================================

try:
    col_cli_id_clients = find_column_by_keywords(clients, ["id", "code", "client_id"])
    col_cli_name_clients = find_column_by_keywords(clients, ["nom", "client", "raison", "societé", "societe"])

    if col_cli_name_clients and not clients.empty:
        if col_cli_id_clients:
            client_mapping = dict(zip(clients[col_cli_id_clients].astype(str).str.strip(), clients[col_cli_name_clients].astype(str).str.strip()))
            reverse_client_mapping = dict(zip(clients[col_cli_name_clients].astype(str).str.strip(), clients[col_cli_id_clients].astype(str).str.strip()))
        else:
            client_mapping = {}
            reverse_client_mapping = {}

        col_cli_om = find_column_by_keywords(om, ["client", "société", "nom"])
        if col_cli_om and not om.empty:
            om["Client_Code_Standard"] = om[col_cli_om].astype(str).str.strip().map(lambda x: x if x in client_mapping else reverse_client_mapping.get(x, "N/A"))
            om["Client_Nom_Standard"] = om[col_cli_om].astype(str).str.strip().map(lambda x: client_mapping.get(x, x))
        else:
            om["Client_Code_Standard"] = "N/A"
            om["Client_Nom_Standard"] = "Inconnu"

        col_cli_cmd = find_column_by_keywords(commandes, ["client", "société", "nom", "raison"])
        if col_cli_cmd and not commandes.empty:
            commandes["Client_Nom_Standard"] = commandes[col_cli_cmd].astype(str).str.strip().map(lambda x: client_mapping.get(x, x))
        else:
            commandes["Client_Nom_Standard"] = "Inconnu"
    else:
        if not om.empty:
            col_cli_om = find_column_by_keywords(om, ["client", "société", "nom"])
            om["Client_Code_Standard"] = "N/A"
            om["Client_Nom_Standard"] = om[col_cli_om].astype(str).str.strip() if col_cli_om else "Inconnu"
        if not commandes.empty:
            col_cli_cmd = find_column_by_keywords(commandes, ["client", "société", "nom", "raison"])
            commandes["Client_Nom_Standard"] = commandes[col_cli_cmd].astype(str).str.strip() if col_cli_cmd else "Inconnu"

    # --- FUSION CROISÉE (OM <-> COMMANDES DE VENTE VIA LE NUMÉRO D'OM) ---
    col_om_num_om = find_column_by_keywords(om, ["om", "ordre", "mission", "n° om", "numéro d'ordre"])
    col_om_num_cmd = find_column_by_keywords(commandes, ["om", "ordre", "mission", "n° om", "numéro d'ordre"])

    if col_om_num_om and col_om_num_cmd and not om.empty and not commandes.empty:
        om_clean = om.copy()
        cmd_clean = commandes.copy()
        om_clean['join_key'] = om_clean[col_om_num_om].astype(str).str.strip()
        cmd_clean['join_key'] = cmd_clean[col_om_num_cmd].astype(str).str.strip()
        df_merged = pd.merge(om_clean, cmd_clean, on='join_key', how='left', suffixes=('_om', '_cmd'))
    else:
        df_merged = om.copy()
except Exception as e:
    df_merged = om.copy() if not om.empty else pd.DataFrame()

# Options dynamiques pour filtres
opts_affectations = ["Akbou", "Setif", "Alger", "Oran"]
opts_camions = extract_unique_options(camions, ["immatriculation", "matricule", "camion", "code", "véhicule"])
if not opts_camions:
    opts_camions = extract_unique_options(om, ["camion", "immatriculation", "matricule", "tracteur", "code"])

opts_clients = sorted(om["Client_Nom_Standard"].dropna().unique().tolist()) if not om.empty and "Client_Nom_Standard" in om.columns else []
if not opts_clients:
    opts_clients = extract_unique_options(clients, ["nom", "client", "raison", "societé"])

opts_chauffeurs = extract_unique_options(chauffeurs, ["nom", "chauffeur", "conducteur", "agent"])
if not opts_chauffeurs:
    opts_chauffeurs = extract_unique_options(om, ["chauffeur", "conducteur", "nom"])

# ============================================================
# BARRE LATÉRALE (SIDEBAR) & FILTRES
# ============================================================

with st.sidebar:
    if os.path.isfile(LOGO_FILE):
        st.image(LOGO_FILE, width=120)
    else:
        st.markdown('<div style="font-size:50px; text-align:center;">🚚</div>', unsafe_allow_html=True)

    st.markdown("### **TMF LOGISTICS**")
    st.markdown("---")

    menu = st.radio(
        "MENU PRINCIPAL",
        [
            "🏢 Détail & Analyse par Client",
            "📊 Analyse Mensuelle (OM & Ventes)",
            "📈 Rapport & Analyse Croisée",
            "📋 Ordres de Mission (OM)",
            "📦 Commandes de Vente",
            "🚛 Flotte & Chauffeurs",
            "💰 Objectifs CA à Réaliser",
        ],
        index=0,
    )

    st.markdown("---")
    st.markdown("### 🔍 **FILTRES DU MOIS**")

    sel_affectation = st.selectbox("📌 Affectation / Agence", ["Tous"] + opts_affectations)
    sel_camion = st.selectbox("🚛 Numéro de Camion", ["Tous"] + opts_camions)
    sel_client = st.selectbox("🏢 Client", ["Tous"] + opts_clients)
    sel_chauffeur = st.selectbox("👨‍✈️ Chauffeur", ["Tous"] + opts_chauffeurs)

    st.markdown("---")
    st.markdown("**📁 Fichiers Source :**")
    for name, path in FILES.items():
        status = "✓" if os.path.isfile(path) else "✗"
        color = "#16834b" if os.path.isfile(path) else "#c0392b"
        st.markdown(f"<span style='color:{color}; font-size:12px;'>{status} {os.path.basename(path)}</span>", unsafe_allow_html=True)

# ============================================================
# APPLICATION DES FILTRES
# ============================================================

om_filtered = apply_text_filter(om, ["affectation", "type", "prestation", "agence", "site", "parc", "wilaya"], sel_affectation)
om_filtered = apply_text_filter(om_filtered, ["camion", "immatriculation", "matricule", "tracteur", "code"], sel_camion)
if sel_client != "Tous" and not om_filtered.empty and "Client_Nom_Standard" in om_filtered.columns:
    om_filtered = om_filtered[om_filtered["Client_Nom_Standard"].astype(str).str.strip() == str(sel_client).strip()]
om_filtered = apply_text_filter(om_filtered, ["chauffeur", "conducteur", "agent"], sel_chauffeur)

if sel_client != "Tous" and not commandes.empty and "Client_Nom_Standard" in commandes.columns:
    commandes_filtered = commandes[commandes["Client_Nom_Standard"].astype(str).str.strip() == str(sel_client).strip()]
else:
    commandes_filtered = apply_text_filter(commandes, ["client", "société", "nom"], sel_client)

if sel_client != "Tous" and not df_merged.empty and "Client_Nom_Standard" in df_merged.columns:
    df_merged_filtered = df_merged[df_merged["Client_Nom_Standard"].astype(str).str.strip() == str(sel_client).strip()]
else:
    df_merged_filtered = apply_text_filter(df_merged, ["client", "société", "nom"], sel_client)

camions_filtered = apply_text_filter(camions, ["immatriculation", "matricule", "camion", "code"], sel_camion)
chauffeurs_filtered = apply_text_filter(chauffeurs, ["nom", "chauffeur", "conducteur", "agent"], sel_chauffeur)

nb_om_mois = len(om_filtered) if not om_filtered.empty else 0
nb_commandes_mois = len(commandes_filtered) if not commandes_filtered.empty else 0
total_ca_objectif_annuel = df_ca_raw["GLOBAL"].sum()

# ============================================================
# EN-TÊTE DE L'APPLICATION
# ============================================================

st.markdown('<div class="tmf-header">', unsafe_allow_html=True)
col_l, col_t = st.columns(2)
with col_l:
    if os.path.isfile(LOGO_FILE):
        st.image(LOGO_FILE, width=200)
    else:
        st.markdown('<div style="font-size:50px; text-align:center;">🚚</div>', unsafe_allow_html=True)
with col_t:
    st.markdown(
        """
    <div style="border: 2px solid #087443; border-radius: 10px; padding: 18px; background-color: #f0f7f4;">
        <div style="font-size:24px; font-weight:700; color:#000000;">
            Tableau de Bord Mensuel — Activité Transport & Rapport Croisé
        </div>
        <div style="font-size:15px; color:#333333; margin-top: 4px;">
            Suivi croisé des Ordres de Mission, Commandes de Vente, Camions et Chauffeurs
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# 0. PAGE : DÉTAIL & ANALYSE PAR CLIENT (MODÈLE EXACT)
# ============================================================

if menu == "🏢 Détail & Analyse par Client":
    st.markdown('<div class="section-title">🏢 Détail des données clients — Analyse par Clients</div>', unsafe_allow_html=True)

    if not df_merged_filtered.empty:
        df_c = df_merged_filtered.copy()

        col_km_tot = find_column_by_keywords(df_c, ["km parcouru", "km total", "kilométrage", "km", "distance"])
        col_km_charge = find_column_by_keywords(df_c, ["km à charge", "km charge", "charge"])
        col_km_vide = find_column_by_keywords(df_c, ["km à vide", "km vide", "roulage à vide", "vide"])
        col_ca = find_column_by_keywords(df_c, ["montant", "ca", "prix", "valeur", "chiffre"])
        col_immob_chg = find_column_by_keywords(df_c, ["immob au chargement", "immob chargement", "chargement"])
        col_immob_dechg = find_column_by_keywords(df_c, ["immob au déchargement", "immob dechargement", "déchargement", "dechargement"])

        df_c["_km_tot"] = pd.to_numeric(df_c[col_km_tot], errors="coerce").fillna(0) if col_km_tot else 0.0
        df_c["_km_vide"] = pd.to_numeric(df_c[col_km_vide], errors="coerce").fillna(0) if col_km_vide else 0.0
        
        if col_km_charge:
            df_c["_km_charge"] = pd.to_numeric(df_c[col_km_charge], errors="coerce").fillna(0)
        else:
            df_c["_km_charge"] = (df_c["_km_tot"] - df_c["_km_vide"]).clip(lower=0)

        df_c["_ca"] = pd.to_numeric(df_c[col_ca], errors="coerce").fillna(0) if col_ca else 0.0
        df_c["_immob_chg"] = pd.to_numeric(df_c[col_immob_chg], errors="coerce").fillna(0) if col_immob_chg else 0.0
        df_c["_immob_dechg"] = pd.to_numeric(df_c[col_immob_dechg], errors="coerce").fillna(0) if col_immob_dechg else 0.0

        # Tranches kilométriques
        df_c["<=100km"] = (df_c["_km_tot"] <= 100).astype(int)
        df_c["101→200km"] = ((df_c["_km_tot"] > 100) & (df_c["_km_tot"] <= 200)).astype(int)
        df_c["201→300km"] = ((df_c["_km_tot"] > 200) & (df_c["_km_tot"] <= 300)).astype(int)
        df_c["301→400km"] = ((df_c["_km_tot"] > 300) & (df_c["_km_tot"] <= 400)).astype(int)
        df_c["401→500km"] = ((df_c["_km_tot"] > 400) & (df_c["_km_tot"] <= 500)).astype(int)
        df_c["501→600km"] = ((df_c["_km_tot"] > 500) & (df_c["_km_tot"] <= 600)).astype(int)
        df_c[">600km"] = (df_c["_km_tot"] > 600).astype(int)

        code_col = "Client_Code_Standard" if "Client_Code_Standard" in df_c.columns else "Client_Nom_Standard"
        name_col = "Client_Nom_Standard" if "Client_Nom_Standard" in df_c.columns else code_col

        df_grouped = df_c.groupby([code_col, name_col], as_index=False).agg(
            Nombre_de_Mission=("_km_tot", "count"),
            Km_Parcouru=("_km_tot", "sum"),
            KM_a_Charge=("_km_charge", "sum"),
            KM_a_Vide=("_km_vide", "sum"),
            CA_Genere=("_ca", "sum"),
            t_100=("<=100km", "sum"),
            t_200=("101→200km", "sum"),
            t_300=("201→300km", "sum"),
            t_400=("301→400km", "sum"),
            t_500=("401→500km", "sum"),
            t_600=("501→600km", "sum"),
            t_plus600=(">600km", "sum"),
            Immob_Chargement=("_immob_chg", "sum"),
            Immob_Dechargement=("_immob_dechg", "sum"),
        )

        df_grouped["CA_moy_Mission"] = np.where(
            df_grouped["Nombre_de_Mission"] > 0,
            df_grouped["CA_Genere"] / df_grouped["Nombre_de_Mission"],
            0.0,
        )
        df_grouped["CA_moy_Km"] = np.where(
            df_grouped["Km_Parcouru"] > 0,
            df_grouped["CA_Genere"] / df_grouped["Km_Parcouru"],
            0.0,
        )

        df_grouped.insert(0, "N°", range(1, len(df_grouped) + 1))

        tot_missions = int(df_grouped["Nombre_de_Mission"].sum())
        tot_km = df_grouped["Km_Parcouru"].sum()
        tot_km_chg = df_grouped["KM_a_Charge"].sum()
        tot_km_vide = df_grouped["KM_a_Vide"].sum()
        tot_ca = df_grouped["CA_Genere"].sum()
        moy_ca_mission = (tot_ca / tot_missions) if tot_missions > 0 else 0
        moy_ca_km = (tot_ca / tot_km) if tot_km > 0 else 0

        # KPI Synthèse
        k1, k2, k3, k4, k5 = st.columns(5)
        with k1:
            kpi_card("Total Missions", f"{tot_missions:,} Missions".replace(",", " "))
        with k2:
            kpi_card("Total Km", f"{tot_km:,.0f} Km".replace(",", " "), f"Chg: {tot_km_chg:,.0f} | Vid: {tot_km_vide:,.0f}".replace(",", " "))
        with k3:
            kpi_card("Total CA", format_currency(tot_ca, "DZD"))
        with k4:
            kpi_card("CA moy / Mission", format_currency(moy_ca_mission, "DZD"))
        with k5:
            kpi_card("CA moy / Km", format_currency(moy_ca_km, "DZD"))

        # Construction du tableau principal
        df_display = pd.DataFrame({
            "N°": df_grouped["N°"],
            "Code Client": df_grouped[code_col],
            "Nom Client": df_grouped[name_col],
            "Nombre de Mission": df_grouped["Nombre_de_Mission"],
            "Km Parcouru": df_grouped["Km_Parcouru"].round(0).astype(int),
            "KM à Charge": df_grouped["KM_a_Charge"].round(0).astype(int),
            "KM à Vide": df_grouped["KM_a_Vide"].round(0).astype(int),
            "CA Généré (DZD)": df_grouped["CA_Genere"].apply(lambda x: f"{x:,.2f}".replace(",", " ").replace(".", ",")),
            "CA moy/Mission": df_grouped["CA_moy_Mission"].apply(lambda x: f"{x:,.2f}".replace(",", " ").replace(".", ",")),
            "CA moy/Km": df_grouped["CA_moy_Km"].apply(lambda x: f"{x:,.2f}".replace(",", " ").replace(".", ",")),
            "<=100km": df_grouped["t_100"],
            "101→200km": df_grouped["t_200"],
            "201→300km": df_grouped["t_300"],
            "301→400km": df_grouped["t_400"],
            "401→500km": df_grouped["t_500"],
            "501→600km": df_grouped["t_600"],
            ">600km": df_grouped["t_plus600"],
            "Immob Au Chargement (H)": df_grouped["Immob_Chargement"].apply(lambda x: f"{x:,.2f}".replace(".", ",")),
            "Immob Au Déchargement (H)": df_grouped["Immob_Dechargement"].apply(lambda x: f"{x:,.2f}".replace(".", ",")),
        })

        total_row = pd.DataFrame([{
            "N°": "TOTAL",
            "Code Client": "-",
            "Nom Client": "SYNTHÈSE GLOBALE",
            "Nombre de Mission": tot_missions,
            "Km Parcouru": int(round(tot_km)),
            "KM à Charge": int(round(tot_km_chg)),
            "KM à Vide": int(round(tot_km_vide)),
            "CA Généré (DZD)": f"{tot_ca:,.2f}".replace(",", " ").replace(".", ","),
            "CA moy/Mission": f"{moy_ca_mission:,.2f}".replace(",", " ").replace(".", ","),
            "CA moy/Km": f"{moy_ca_km:,.2f}".replace(",", " ").replace(".", ","),
            "<=100km": int(df_grouped["t_100"].sum()),
            "101→200km": int(df_grouped["t_200"].sum()),
            "201→300km": int(df_grouped["t_300"].sum()),
            "301→400km": int(df_grouped["t_400"].sum()),
            "401→500km": int(df_grouped["t_500"].sum()),
            "501→600km": int(df_grouped["t_600"].sum()),
            ">600km": int(df_grouped["t_plus600"].sum()),
            "Immob Au Chargement (H)": f"{df_grouped['Immob_Chargement'].sum():,.2f}".replace(".", ","),
            "Immob Au Déchargement (H)": f"{df_grouped['Immob_Dechargement'].sum():,.2f}".replace(".", ","),
        }])

        df_final_table = pd.concat([total_row, df_display], ignore_index=True)

        st.markdown('<div class="sub-title">📋 Tableau Analytique Complet par Client & Tranches Kilométriques</div>', unsafe_allow_html=True)
        st.dataframe(df_final_table, use_container_width=True, key="table_detail_clients")

        st.markdown("---")

        col_top10, col_tranches = st.columns(2)

        with col_top10:
            st.markdown('<div class="sub-title">🏆 Top 10 Clients par CA Réalisé</div>', unsafe_allow_html=True)
            top10_df = df_grouped.sort_values(by="CA_Genere", ascending=False).head(10).reset_index(drop=True)
            badges = ["①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩"]
            top10_display = pd.DataFrame({
                "N°": [badges[i] for i in range(len(top10_df))],
                "Nom Client": top10_df[name_col],
                "CA Réalisé (DZD)": top10_df["CA_Genere"].apply(lambda x: f"{x:,.2f}".replace(",", " ").replace(".", ",")),
            })
            show_table(top10_display, "table_top10_clients")

        with col_tranches:
            st.markdown('<div class="sub-title">🚛 Répartition des missions clients par plage kilométrique</div>', unsafe_allow_html=True)
            client_inspect = st.selectbox(
                "Sélectionnez un client :",
                options=df_grouped[name_col].tolist(),
                index=0,
            )
            row_sel = df_grouped[df_grouped[name_col] == client_inspect].iloc[0]
            tranche_data = pd.DataFrame({
                "Plage Kilométrique": ["<=100km", "101→200km", "201→300km", "301→400km", "401→500km", "501→600km", ">600km"],
                "Nombre de Missions": [
                    row_sel["t_100"], row_sel["t_200"], row_sel["t_300"],
                    row_sel["t_400"], row_sel["t_500"], row_sel["t_600"], row_sel["t_plus600"]
                ]
            })
            show_table(tranche_data.T, "table_tranches_client_sel")
            fig_tr = px.bar(
                tranche_data,
                x="Plage Kilométrique",
                y="Nombre de Missions",
                title=f"Distribution — {client_inspect}",
                color="Nombre de Missions",
                color_continuous_scale="Greens",
            )
            fig_tr.update_layout(height=280, margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig_tr, use_container_width=True)

    else:
        st.warning("⚠️ Aucune donnée d'Ordre de Mission ou de Vente disponible ou les fichiers source (OM.xlsx, Commande de vente.xlsx) sont introuvables dans le dossier 'Data'.")

# ============================================================
# 1. PAGE : ANALYSE MENSUELLE (OM & VENTES)
# ============================================================

elif menu == "📊 Analyse Mensuelle (OM & Ventes)":
    st.markdown('<div class="section-title">📊 Synthèse Générale de l\'Activité du Mois</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Total Missions (OM)", f"{nb_om_mois:,}", "Ordres de mission exécutés ce mois")
    with c2:
        kpi_card("Total Commandes", f"{nb_commandes_mois:,}", "Commandes enregistrées ce mois")
    with c3:
        ratio_execution = (nb_om_mois / nb_commandes_mois * 100) if nb_commandes_mois > 0 else 0
        kpi_card("Taux d'Exécution OM/Commandes", f"{ratio_execution:.1f} %", "Couverture des commandes")
    with c4:
        kpi_card("Objectif CA Annuel", format_currency(total_ca_objectif_annuel, "DA"), "Global sections à réaliser")

    st.markdown("---")

    col_m1, col_m2 = st.columns(2)

    with col_m1:
        st.markdown('<div class="sub-title">🚛 Activité par Camion (Missions réalisées)</div>', unsafe_allow_html=True)
        col_cam_om = find_column_by_keywords(om_filtered, ["camion", "immatriculation", "matricule", "code", "tracteur"])
        if col_cam_om and not om_filtered.empty:
            cam_counts = om_filtered[col_cam_om].value_counts().reset_index().head(10)
            cam_counts.columns = ["Camion", "Nombre d'OM"]
            fig_cam = px.bar(cam_counts, x="Camion", y="Nombre d'OM", title="Top 10 Camions les plus sollicités ce mois", color="Nombre d'OM")
            st.plotly_chart(fig_cam, use_container_width=True)
        else:
            st.info("Données insuffisantes pour afficher l'activité des camions.")

    with col_m2:
        st.markdown('<div class="sub-title">🏢 Portefeuille Clients (Commandes du Mois)</div>', unsafe_allow_html=True)
        col_cli_cmd = "Client_Nom_Standard" if not commandes_filtered.empty and "Client_Nom_Standard" in commandes_filtered.columns else find_column_by_keywords(commandes_filtered, ["client", "société", "nom", "raison"])
        if col_cli_cmd and not commandes_filtered.empty:
            cli_counts = commandes_filtered[col_cli_cmd].value_counts().reset_index().head(10)
            cli_counts.columns = ["Client", "Nombre de Commandes"]
            fig_cli = px.pie(cli_counts, names="Client", values="Nombre de Commandes", title="Top Clients par volume de commandes", hole=0.3)
            st.plotly_chart(fig_cli, use_container_width=True)
        else:
            st.info("Données insuffisantes pour la répartition par client.")

# ============================================================
# 2. PAGE : RAPPORT & ANALYSE CROISÉE
# ============================================================

elif menu == "📈 Rapport & Analyse Croisée":
    st.markdown('<div class="section-title">📈 Analyse Croisée Intégrée (OM, Commandes, Camions, Sections & Superviseurs)</div>', unsafe_allow_html=True)
    st.markdown("Ce tableau croisé dynamique fusionne les **Ordres de Mission (`OM.xlsx`)** et les **Commandes de Vente (`Commande de vente.xlsx`)** en utilisant le **numéro d'ordre de mission** comme clé de liaison.")

    col_cam_om = find_column_by_keywords(df_merged_filtered, ["camion", "tracteur", "immatriculation", "code"])
    col_section = find_column_by_keywords(df_merged_filtered, ["section", "activité", "activite", "type"])
    col_superviseur = find_column_by_keywords(df_merged_filtered, ["superviseur", "responsable", "exploitant", "agent"])
    col_km_om = find_column_by_keywords(df_merged_filtered, ["km", "kilometre", "kilométrage", "distance"])
    col_montant_om = find_column_by_keywords(df_merged_filtered, ["montant", "prix", "valeur", "ca", "chiffre"])
    col_vide_om = find_column_by_keywords(df_merged_filtered, ["vide", "roulage à vide", "km vide", "kilometrage vide"])

    if not df_merged_filtered.empty:
        df_work = df_merged_filtered.copy()
        df_work['__count_col__'] = 1
        df_work['__km_col__'] = pd.to_numeric(df_work[col_km_om], errors='coerce').fillna(0) if col_km_om else 0
        df_work['__montant_col__'] = pd.to_numeric(df_work[col_montant_om], errors='coerce').fillna(0) if col_montant_om else 0
        df_work['__vide_col__'] = pd.to_numeric(df_work[col_vide_om], errors='coerce').fillna(0) if col_vide_om else 0

        st.markdown('<div class="sub-title">⚙️ Paramètres du Tableau Croisé Dynamique</div>', unsafe_allow_html=True)
        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            axes_disponibles = []
            if col_cam_om: axes_disponibles.append("Camion")
            if col_section: axes_disponibles.append("Section")
            if col_superviseur: axes_disponibles.append("Superviseur")
            if "Client_Nom_Standard" in df_work.columns: axes_disponibles.append("Client")

            choix_groupes = st.multiselect(
                "Sélectionnez les axes de regroupement (Lignes du tableau) :",
                options=axes_disponibles,
                default=["Camion", "Section"] if "Camion" in axes_disponibles and "Section" in axes_disponibles else axes_disponibles[:2]
            )
        with col_opt2:
            st.info("💡 **Astuce :** Le tableau regroupe automatiquement le kilométrage, le montant réalisé et le roulage à vide.")

        mapping_axes = {
            "Camion": col_cam_om,
            "Section": col_section,
            "Superviseur": col_superviseur,
            "Client": "Client_Nom_Standard"
        }
        group_cols = [mapping_axes[ax] for ax in choix_groupes if ax in mapping_axes]

        if group_cols:
            df_pivot = df_work.groupby(group_cols).agg(
                {
                    '__count_col__': 'count',
                    '__km_col__': 'sum',
                    '__montant_col__': 'sum',
                    '__vide_col__': 'sum'
                }
            ).reset_index()

            rename_mapping = {
                col_cam_om: 'Camion' if col_cam_om else 'Camion',
                col_section: 'Section' if col_section else 'Section',
                col_superviseur: 'Superviseur' if col_superviseur else 'Superviseur',
                'Client_Nom_Standard': 'Client',
                '__count_col__': 'Nombre de Missions',
                '__km_col__': 'Kilométrage Total (Km)',
                '__montant_col__': 'Montant Réalisé (DA)',
                '__vide_col__': 'Roulage à Vide (Km)'
            }
            df_pivot = df_pivot.rename(columns=rename_mapping)

            if 'Kilométrage Total (Km)' in df_pivot.columns and 'Roulage à Vide (Km)' in df_pivot.columns:
                df_pivot['% Roulage à Vide'] = np.where(
                    df_pivot['Kilométrage Total (Km)'] > 0,
                    (df_pivot['Roulage à Vide (Km)'] / df_pivot['Kilométrage Total (Km)'] * 100).round(2),
                    0
                )

            st.markdown('<div class="sub-title">📋 Résultat du Tableau Croisé Dynamique</div>', unsafe_allow_html=True)
            show_table(df_pivot, "table_croisee_dynamique")
        else:
            st.warning("Veuillez sélectionner au moins un axe de regroupement.")
    else:
        st.info("Données insuffisantes pour établir l'analyse croisée.")

# ============================================================
# 3. PAGE : ORDRES DE MISSION (OM)
# ============================================================

elif menu == "📋 Ordres de Mission (OM)":
    st.markdown('<div class="section-title">📋 Liste des Ordres de Mission du Mois</div>', unsafe_allow_html=True)
    if om_filtered.empty:
        st.warning("Aucun Ordre de Mission trouvé pour ce filtre.")
    else:
        st.write(f"Nombre total de missions enregistrées : **{len(om_filtered)}**")
        show_table(om_filtered, "table_om_mois")

# ============================================================
# 4. PAGE : COMMANDES DE VENTE
# ============================================================

elif menu == "📦 Commandes de Vente":
    st.markdown('<div class="section-title">📦 Liste des Commandes de Vente du Mois</div>', unsafe_allow_html=True)
    if commandes_filtered.empty:
        st.warning("Aucune Commande de vente trouvée.")
    else:
        st.write(f"Nombre total de commandes enregistrées : **{len(commandes_filtered)}**")
        show_table(commandes_filtered, "table_cmd_mois")

# ============================================================
# 5. PAGE : FLOTTE & CHAUFFEURS
# ============================================================

elif menu == "🚛 Flotte & Chauffeurs":
    st.markdown('<div class="section-title">🚛 Parc Camions & Chauffeurs Engagés</div>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["🚛 Camions", "👨‍✈️ Chauffeurs"])
    with t1:
        show_table(camions_filtered, "table_camions_mois")
    with t2:
        show_table(chauffeurs_filtered, "table_chauffeurs_mois")

# ============================================================
# 6. PAGE : OBJECTIFS CA À RÉALISER
# ============================================================

elif menu == "💰 Objectifs CA à Réaliser":
    st.markdown('<div class="section-title">💰 Chiffre d\'Affaires Prévisionnel (À Réaliser par Section)</div>', unsafe_allow_html=True)
    formatted_ca = df_ca_raw.copy()
    for col in formatted_ca.columns:
        if col != "CA PAR SECTION":
            formatted_ca[col] = formatted_ca[col].apply(lambda x: f"{x:,.0f} DA".replace(",", " "))

    show_table(formatted_ca, "table_ca_objectif")

    st.markdown('<div class="sub-title">📊 Répartition Graphique des Objectifs de CA par Section</div>', unsafe_allow_html=True)
    fig_ca_bar = px.bar(df_ca_raw, x="CA PAR SECTION", y="GLOBAL", title="Objectif CA Total Annuel par Section (DA)", color="CA PAR SECTION")
    st.plotly_chart(fig_ca_bar, use_container_width=True)

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        © 2026 TMF Logistics — Solution Intégrée Analytics Transport & RH (Akbou / Béjaïa)
    </div>
    """,
    unsafe_allow_html=True,
)
