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
        "CELLULE",
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


def find_column_by_keywords(df, keywords):
    if df.empty:
        return None
    for col in df.columns:
        col_str = str(col).lower()
        if any(kw in col_str for kw in keywords):
            return col
    return None


def extract_unique_options(df, keywords):
    col = find_column_by_keywords(df, keywords)
    if col and not df.empty:
        vals = df[col].dropna().astype(str).str.strip().unique().tolist()
        vals = [v for v in vals if v and v.lower() != "nan"]
        return sorted(vals)
    return []


def apply_text_filter(df, keywords, selected_value):
    if df.empty or not selected_value or selected_value == "Tous":
        return df
    col = find_column_by_keywords(df, keywords)
    if col:
        return df[df[col].astype(str).str.strip() == str(selected_value).strip()]
    return df


def format_currency(amount):
    return f"{amount:,.0f} DA".replace(",", " ")


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
    if df.empty:
        st.info("Aucune donnée disponible pour cette sélection.")
        return
    st.dataframe(df, use_container_width=True, hide_index=True, key=key)


# ============================================================
# CHARGEMENT DES BASES DE DONNÉES
# ============================================================

camions = load_data(FILES["camions"])
chauffeurs = load_data(FILES["chauffeurs"], "Chauffeurs")
clients = load_data(FILES["clients"])
commandes = load_data(FILES["commandes"])
om = load_data(FILES["om"], "Input OM fini")

# Options dynamiques pour filtres
opts_affectations = ["Akbou", "Setif", "Alger", "Oran"]
opts_camions = extract_unique_options(
    camions, ["immatriculation", "matricule", "camion", "code", "véhicule"]
)
if not opts_camions:
    opts_camions = extract_unique_options(
        om, ["camion", "immatriculation", "matricule", "tracteur", "code"]
    )

opts_clients = extract_unique_options(
    clients, ["nom", "client", "raison", "societé"]
)
if not opts_clients:
    opts_clients = extract_unique_options(om, ["client", "société", "nom"])

opts_chauffeurs = extract_unique_options(
    chauffeurs, ["nom", "chauffeur", "conducteur", "agent"]
)
if not opts_chauffeurs:
    opts_chauffeurs = extract_unique_options(om, ["chauffeur", "conducteur", "nom"])

# ============================================================
# BARRE LATÉRALE (SIDEBAR) & FILTRES
# ============================================================

with st.sidebar:
    if os.path.isfile(LOGO_FILE):
        st.image(LOGO_FILE, width=120)
    else:
        st.markdown(
            '<div style="font-size:50px; text-align:center;">🚚</div>',
            unsafe_allow_html=True,
        )

    st.markdown("### **TMF LOGISTICS**")
    st.markdown("---")

    menu = st.radio(
        "MENU PRINCIPAL",
        [
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
        st.markdown(
            f"<span style='color:{color}; font-size:12px;'>{status} {os.path.basename(path)}</span>",
            unsafe_allow_html=True,
        )

# ============================================================
# APPLICATION DES FILTRES
# ============================================================

om_filtered = apply_text_filter(
    om, ["affectation", "type", "prestation", "agence", "site", "parc", "wilaya"], sel_affectation
)
om_filtered = apply_text_filter(
    om_filtered, ["camion", "immatriculation", "matricule", "tracteur", "code"], sel_camion
)
om_filtered = apply_text_filter(om_filtered, ["client", "société", "nom"], sel_client)
om_filtered = apply_text_filter(om_filtered, ["chauffeur", "conducteur", "agent"], sel_chauffeur)

commandes_filtered = apply_text_filter(commandes, ["client", "société", "nom"], sel_client)

camions_filtered = apply_text_filter(camions, ["immatriculation", "matricule", "camion", "code"], sel_camion)
chauffeurs_filtered = apply_text_filter(chauffeurs, ["nom", "chauffeur", "conducteur", "agent"], sel_chauffeur)

nb_om_mois = len(om_filtered) if not om_filtered.empty else 0
nb_commandes_mois = len(commandes_filtered) if not commandes_filtered.empty else 0
total_ca_objectif_annuel = df_ca_raw["GLOBAL"].sum()

# ============================================================
# EN-TÊTE DE L'APPLICATION
# ============================================================

st.markdown('<div class="tmf-header">', unsafe_allow_html=True)
col_l, col_t = st.columns([1, 6], vertical_alignment="center")
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
# 1. PAGE : ANALYSE MENSUELLE (OM & VENTES)
# ============================================================

if menu == "📊 Analyse Mensuelle (OM & Ventes)":
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
        kpi_card("Objectif CA Annuel", format_currency(total_ca_objectif_annuel), "Global sections à réaliser")

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
        col_cli_cmd = find_column_by_keywords(commandes_filtered, ["client", "société", "nom", "raison"])
        if col_cli_cmd and not commandes_filtered.empty:
            cli_counts = commandes_filtered[col_cli_cmd].value_counts().reset_index().head(10)
            cli_counts.columns = ["Client", "Nombre de Commandes"]
            fig_cli = px.pie(cli_counts, names="Client", values="Nombre de Commandes", title="Top Clients par volume de commandes", hole=0.3)
            st.plotly_chart(fig_cli, use_container_width=True)
        else:
            st.info("Données insuffisantes pour la répartition par client.")

# ============================================================
# 2. PAGE : RAPPORT & ANALYSE CROISÉE (NOUVEAU)
# ============================================================

elif menu == "📈 Rapport & Analyse Croisée":
    st.markdown('<div class="section-title">📈 Analyse Croisée : OM, Commandes, Camions & Chauffeurs</div>', unsafe_allow_html=True)
    st.markdown("Ce rapport croise les données opérationnelles des **Ordres de Mission (`OM.xlsx`)** avec les **Commandes de Vente (`Commande de vente.xlsx`)**, en corrélant les performances des **Camions** et des **Chauffeurs**.")

    # 1. Tableau Croisé Chauffeurs & Camions selon les OM
    st.markdown('<div class="sub-title">👥 Tableau Croisé : Chauffeurs vs Camions (Missions Réalisées)</div>', unsafe_allow_html=True)
    col_chauffeur_om = find_column_by_keywords(om_filtered, ["chauffeur", "conducteur", "agent"])
    col_camion_om = find_column_by_keywords(om_filtered, ["camion", "tracteur", "immatriculation", "code"])

    if col_chauffeur_om and col_camion_om and not om_filtered.empty:
        # Création d'une table croisée (Pivot Table)
        pivot_chauffeur_camion = pd.pivot_table(
            om_filtered,
            index=col_chauffeur_om,
            columns=col_camion_om,
            aggfunc='size',
            fill_value=0
        )
        show_table(pivot_chauffeur_camion.reset_index(), "pivot_chauffeur_camion")
    else:
        st.info("Colonnes Chauffeur ou Camion non détectées simultanément dans OM.xlsx.")

    st.markdown("---")

    # 2. Graphiques et Tableaux Croisés Avancés
    col_r1, col_r2 = st.columns(2)

    with col_r1:
        st.markdown('<div class="sub-title">👨‍✈️ Top Chauffeurs par Nombre de Missions</div>', unsafe_allow_html=True)
        if col_chauffeur_om and not om_filtered.empty:
            df_top_chauffeurs = om_filtered[col_chauffeur_om].value_counts().reset_index()
            df_top_chauffeurs.columns = ["Chauffeur", "Nombre d'OM"]
            fig_top_ch = px.bar(df_top_chauffeurs.head(10), x="Chauffeur", y="Nombre d'OM", title="Top 10 Chauffeurs les plus actifs", color="Nombre d'OM")
            st.plotly_chart(fig_top_ch, use_container_width=True)
            show_table(df_top_chauffeurs, "table_top_chauffeurs")
        else:
            st.info("Données de chauffeurs non disponibles dans les OM.")

    with col_r2:
        st.markdown('<div class="sub-title">🚛 Top Camions par Nombre de Missions</div>', unsafe_allow_html=True)
        if col_camion_om and not om_filtered.empty:
            df_top_camions = om_filtered[col_camion_om].value_counts().reset_index()
            df_top_camions.columns = ["Camion", "Nombre d'OM"]
            fig_top_cm = px.bar(df_top_camions.head(10), x="Camion", y="Nombre d'OM", title="Top 10 Camions les plus actifs", color="Nombre d'OM")
            st.plotly_chart(fig_top_cm, use_container_width=True)
            show_table(df_top_camions, "table_top_camions")
        else:
            st.info("Données de camions non disponibles dans les OM.")

    st.markdown("---")

    # 3. Analyse Croisée Commandes & Clients (Ventes vs Logistique)
    st.markdown('<div class="sub-title">📦 Analyse de la Demande : Commandes par Client</div>', unsafe_allow_html=True)
    col_client_cmd = find_column_by_keywords(commandes_filtered, ["client", "société", "nom", "raison"])
    col_vol_cmd = find_column_by_keywords(commandes_filtered, ["quantite", "tonnage", "poids", "volume", "montant"])

    if col_client_cmd and not commandes_filtered.empty:
        if col_vol_cmd:
            df_cmd_summary = commandes_filtered.groupby(col_client_cmd)[col_vol_cmd].agg(['count', 'sum']).reset_index()
            df_cmd_summary.columns = ["Client", "Nombre de Commandes", "Volume / Montant Total"]
        else:
            df_cmd_summary = commandes_filtered[col_client_cmd].value_counts().reset_index()
            df_cmd_summary.columns = ["Client", "Nombre de Commandes"]

        fig_cmd_bar = px.bar(df_cmd_summary.head(15), x="Client", y=df_cmd_summary.columns[1], title="Répartition des Commandes par Client", color=df_cmd_summary.columns[1])
        st.plotly_chart(fig_cmd_bar, use_container_width=True)
        show_table(df_cmd_summary, "table_cmd_summary")
    else:
        st.info("Aucune donnée de commande exploitable pour ce croisement.")

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
