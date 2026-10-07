import streamlit as st
import pandas as pd
import numpy as np
import os
import io
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# CONFIGURATION DE LA PAGE
# ============================================================

st.set_page_config(
    page_title="Gestion de la Flotte & RH — TMF Logistics",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
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
""", unsafe_allow_html=True)

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

def kpi_card(title, value, subtext="", color="#087443"):
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color: {color};">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{subtext}</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# CHARGEMENT DES BASE DE DONNÉES
# ============================================================

camions = load_data(FILES["camions"])
chauffeurs = load_data(FILES["chauffeurs"], "Chauffeurs")
clients = load_data(FILES["clients"])
commandes = load_data(FILES["commandes"])
om = load_data(FILES["om"], "Input OM fini")

# Statistiques globales
nb_camions = len(camions) if not camions.empty else 0
nb_chauffeurs = len(chauffeurs) if not chauffeurs.empty else 0
nb_clients = len(clients) if not clients.empty else 0
nb_commandes = len(commandes) if not commandes.empty else 0
nb_om = len(om) if not om.empty else 0
total_ca_annuel = df_ca["GLOBAL"].sum()

# ============================================================
# NAVIGATION SIDEBAR
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
            "🏠 Tableau de bord Global",
            "📊 Analytics Transport & Transfert",
            "👨‍✈️ Analytics RH & Chauffeurs",
            "💰 Chiffre d'Affaires & Sections",
            "📋 Ordres de Mission (OM)",
            "🚛 Flotte de Camions",
            "📦 Commandes & Clients",
            "📊 Rapports & Exports"
        ],
        index=0
    )

    st.markdown("---")
    st.markdown("**📁 Fichiers Source :**")
    for name, path in FILES.items():
        status = "✓" if os.path.isfile(path) else "✗"
        color = "#16834b" if os.path.isfile(path) else "#c0392b"
        st.markdown(f"<span style='color:{color}; font-size:12px;'>{status} {os.path.basename(path)}</span>", unsafe_allow_html=True)

# ============================================================
# HEADER EN TÊTE
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
        <div style="font-size:28px; font-weight:700; color:black;">
            Système de Gestion Intégré & Analytics Flotte
        </div>
        <div style="font-size:18px; color:#000000;">
            Suivi des opérations de transport, des KPI RH, de la rentabilité et du transfert de marchandises
        </div>
        """,
        unsafe_allow_html=True
    )
st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# 1. TABLEAU DE BORD GLOBAL
# ============================================================

if menu == "🏠 Tableau de bord Global":

    st.markdown('<div class="section-title">🏠 Vue d\'ensemble des Indicateurs Clés (KPI)</div>', unsafe_allow_html=True)

    # Ligne KPI Principaux
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        kpi_card("CA Annuel Total", format_currency(total_ca_annuel), "Global toutes sections")
    with c2:
        kpi_card("Total Missions (OM)", f"{nb_om:,}", "Ordres de mission exécutés")
    with c3:
        kpi_card("Taille Flotte", f"{nb_camions} Véhicules", "Camions enregistrés")
    with c4:
        kpi_card("Effectif Chauffeurs", f"{nb_chauffeurs} Chauffeurs", "Conducteurs actifs")
    with c5:
        kpi_card("Commandes Client", f"{nb_commandes}", "Commandes enregistrées")

    st.markdown("---")

    col_g1, col_g2 = st.columns([7, 5])

    with col_g1:
        st.markdown('<div class="sub-title">📈 Évolution Mensuelle du Chiffre d\'Affaires</div>', unsafe_allow_html=True)
        months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
        ca_mensuel = df_ca.drop(columns=["CA PAR SECTION", "GLOBAL"]).sum().values

        df_trend = pd.DataFrame({"Mois": months, "CA": ca_mensuel})
        fig_trend = px.line(df_trend, x="Mois", y="CA", markers=True, title="Tendance du CA Mensuel (DA)")
        fig_trend.update_traces(line_color="#087443", line_width=3)
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_g2:
        st.markdown('<div class="sub-title">📊 Répartition du CA par Section</div>', unsafe_allow_html=True)
        fig_pie = px.pie(df_ca, names="CA PAR SECTION", values="GLOBAL", hole=0.4, title="Part de Chiffre d'Affaires")
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

# ============================================================
# 2. ANALYTICS TRANSPORT & TRANSFERT DE MARCHANDISES
# ============================================================

elif menu == "📊 Analytics Transport & Transfert":

    st.markdown('<div class="section-title">🚚 KPI Transport & Transfert de Marchandises</div>', unsafe_allow_html=True)

    # Calculs KPI avancés Transport
    ca_par_om = total_ca_annuel / nb_om if nb_om > 0 else 0
    ca_par_camion = total_ca_annuel / nb_camions if nb_camions > 0 else 0
    om_par_camion = nb_om / nb_camions if nb_camions > 0 else 0

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        kpi_card("CA Moyen / Mission", format_currency(ca_par_om), "Rentabilité par Ordre de Mission")
    with k2:
        kpi_card("CA Moyen / Camion", format_currency(ca_par_camion), "Productivité annuelle par camion")
    with k3:
        kpi_card("Missions / Camion", f"{om_par_camion:.1f}", "Moyenne annuelle de rotations")
    with k4:
        ratio_rotation = (nb_commandes / nb_om) if nb_om > 0 else 0
        kpi_card("Taux Commandes/OM", f"{ratio_rotation:.2f}", "Nombre de commandes par mission")

    st.markdown("---")
    st.markdown('<div class="sub-title">📊 Analyse d\'Activité par Type de Remorque / Section</div>', unsafe_allow_html=True)

    transport_kpi = []
    for section in df_ca["CA PAR SECTION"]:
        ca_sec = df_ca[df_ca["CA PAR SECTION"] == section]["GLOBAL"].values[0]
        
        # Recherche correspondance OM
        om_count = 0
        if not om.empty:
            match_om = om.astype(str).apply(lambda col: col.str.lower().str.contains(section.lower(), na=False)).any(axis=1)
            om_count = om[match_om].shape[0]

        ca_moyen_mission = (ca_sec / om_count) if om_count > 0 else 0

        transport_kpi.append({
            "Section Transport": section,
            "CA Annuel Total": ca_sec,
            "Part du CA (%)": (ca_sec / total_ca_annuel) * 100,
            "Nombre d'OM": om_count,
            "CA Moyen / Mission (DA)": ca_moyen_mission
        })

    df_trans_kpi = pd.DataFrame(transport_kpi)

    c_bar1, c_bar2 = st.columns(2)
    with c_bar1:
        fig_bar_om = px.bar(df_trans_kpi, x="Section Transport", y="Nombre d'OM", title="Nombre de Missions (OM) par Section", color="Section Transport")
        st.plotly_chart(fig_bar_om, use_container_width=True)

    with c_bar2:
        fig_bar_ca = px.bar(df_trans_kpi, x="Section Transport", y="CA Moyen / Mission (DA)", title="Rentabilité Moyenne par Mission (DA)", color="Section Transport")
        st.plotly_chart(fig_bar_ca, use_container_width=True)

    st.markdown('<div class="sub-title">📋 Tableau Synthétique des Performance Transport</div>', unsafe_allow_html=True)
    
    df_trans_display = df_trans_kpi.copy()
    df_trans_display["CA Annuel Total"] = df_trans_display["CA Annuel Total"].apply(format_currency)
    df_trans_display["Part du CA (%)"] = df_trans_display["Part du CA (%)"].apply(lambda x: f"{x:.2f} %")
    df_trans_display["CA Moyen / Mission (DA)"] = df_trans_display["CA Moyen / Mission (DA)"].apply(format_currency)

    show_table(df_trans_display, "transport_kpi_table")

# ============================================================
# 3. ANALYTICS RH & CHAUFFEURS
# ============================================================

elif menu == "👨‍✈️ Analytics RH & Chauffeurs":

    st.markdown('<div class="section-title">👨‍✈️ KPI Ressources Humaines & Performance Chauffeurs</div>', unsafe_allow_html=True)

    # Calculs KPI RH
    om_par_chauffeur = nb_om / nb_chauffeurs if nb_chauffeurs > 0 else 0
    ca_par_chauffeur = total_ca_annuel / nb_chauffeurs if nb_chauffeurs > 0 else 0
    ratio_camion_chauffeur = nb_camions / nb_chauffeurs if nb_chauffeurs > 0 else 0

    rh1, rh2, rh3, rh4 = st.columns(4)
    with rh1:
        kpi_card("Effectif Chauffeurs", f"{nb_chauffeurs}", "Chauffeurs enregistrés")
    with rh2:
        kpi_card("Missions / Chauffeur", f"{om_par_chauffeur:.1f}", "Rotations moyennes / an")
    with rh3:
        kpi_card("CA Généré / Chauffeur", format_currency(ca_par_chauffeur), "Productivité RH moyenne")
    with rh4:
        kpi_card("Ratio Camions/Chauffeur", f"{ratio_camion_chauffeur:.2f}", "Couverture de la flotte")

    st.markdown("---")

    if not chauffeurs.empty and not om.empty:
        st.markdown('<div class="sub-title">🏆 Top Chauffeurs par Nombre de Missions (Ordres de Mission)</div>', unsafe_allow_html=True)
        
        # Détection de la colonne chauffeur dans OM
        possible_cols = [c for c in om.columns if "chauffeur" in c.lower() or "conducteur" in c.lower() or "nom" in c.lower()]
        
        if possible_cols:
            col_driver = possible_cols[0]
            driver_counts = om[col_driver].value_counts().reset_index()
            driver_counts.columns = ["Chauffeur", "Nombre de Missions"]
            
            f_driver = px.bar(driver_counts.head(10), x="Chauffeur", y="Nombre de Missions", title="Top 10 Chauffeurs les plus sollicités", color="Nombre de Missions")
            st.plotly_chart(f_driver, use_container_width=True)
            
            show_table(driver_counts, "driver_missions_table")
        else:
            st.info("Colonne identifiant le chauffeur non détectée automatiquement dans la base OM.")
    else:
        st.warning("Données insuffisantes pour générer la répartition détaillée par chauffeur.")

# ============================================================
# 4. CHIFFRE D'AFFAIRES & SECTIONS
# ============================================================

elif menu == "💰 Chiffre d'Affaires & Sections":

    st.markdown('<div class="section-title">💰 Analyse du Chiffre d\'Affaires par Section</div>', unsafe_allow_html=True)

    formatted_ca = df_ca.copy()
    for col in formatted_ca.columns:
        if col != "CA PAR SECTION":
            formatted_ca[col] = formatted_ca[col].apply(lambda x: f"{x:,.0f}".replace(",", " "))

    show_table(formatted_ca, "ca_full_table")

    st.markdown('<div class="sub-title">📊 CA Mensuel par Section (Détail)</div>', unsafe_allow_html=True)
    df_melted = df_ca.melt(id_vars=["CA PAR SECTION"], var_name="Mois", value_name="CA")
    df_melted = df_melted[df_melted["Mois"] != "GLOBAL"]

    fig_stack = px.bar(df_melted, x="Mois", y="CA", color="CA PAR SECTION", title="Répartition du CA mensuel par section")
    st.plotly_chart(fig_stack, use_container_width=True)

# ============================================================
# 5. ORDRES DE MISSION (OM)
# ============================================================

elif menu == "📋 Ordres de Mission (OM)":

    st.markdown('<div class="section-title">📋 Gestion des Ordres de Mission</div>', unsafe_allow_html=True)

    if om.empty:
        st.warning("Aucune donnée disponible dans OM.xlsx")
    else:
        st.write(f"Total des enregistrements : **{nb_om}**")

        s_om = st.text_input("🔎 Recherche rapide", key="om_search")
        filtered_om = search_data(om, s_om)

        col_f1, col_f2 = st.columns(2)
        with col_f1:
            sel_col = st.selectbox("Filtrer par colonne", ["Aucun"] + list(om.columns))
        with col_f2:
            if sel_col != "Aucun":
                vals = filtered_om[sel_col].dropna().astype(str).unique().tolist()
                sel_val = st.selectbox("Valeur", ["Tous"] + sorted(vals))
                filtered_om = filter_data(filtered_om, sel_col, sel_val)

        show_table(filtered_om, "om_main_table")

# ============================================================
# 6. FLOTTE DE CAMIONS
# ============================================================

elif menu == "🚛 Flotte de Camions":

    st.markdown('<div class="section-title">🚛 Gestion de la Flotte de Camions</div>', unsafe_allow_html=True)

    if camions.empty:
        st.warning("Aucune donnée disponible dans Camions.xlsx")
    else:
        st.write(f"Nombre total de camions : **{nb_camions}**")

        s_cam = st.text_input("🔎 Recherche camion", key="camion_search")
        filtered_cam = search_data(camions, s_cam)

        show_table(filtered_cam, "camions_main_table")

# ============================================================
# 7. COMMANDES & CLIENTS
# ============================================================

elif menu == "📦 Commandes & Clients":

    st.markdown('<div class="section-title">📦 Commandes de Vente & Portefeuille Clients</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📦 Commandes", "👥 Clients"])

    with tab1:
        if commandes.empty:
            st.warning("Aucune donnée Commande disponible.")
        else:
            st.write(f"Nombre de commandes : **{nb_commandes}**")
            s_cmd = st.text_input("🔎 Recherche commande", key="cmd_search")
            show_table(search_data(commandes, s_cmd), "cmd_table")

    with tab2:
        if clients.empty:
            st.warning("Aucune donnée Client disponible.")
        else:
            st.write(f"Nombre de clients : **{nb_clients}**")
            s_cli = st.text_input("🔎 Recherche client", key="cli_search")
            show_table(search_data(clients, s_cli), "cli_table")

# ============================================================
# 8. RAPPORTS & EXPORTS
# ============================================================

elif menu == "📊 Rapports & Exports":

    st.markdown('<div class="section-title">📊 Synthèse Globale des KPI</div>', unsafe_allow_html=True)

    kpi_summary = pd.DataFrame([
        {"Catégorie": "Financier", "Indicateur": "CA Annuel Total", "Valeur": format_currency(total_ca_annuel)},
        {"Catégorie": "Financier", "Indicateur": "CA Moyen / Mission", "Valeur": format_currency(total_ca_annuel / nb_om if nb_om > 0 else 0)},
        {"Catégorie": "Financier", "Indicateur": "CA Moyen / Camion", "Valeur": format_currency(total_ca_annuel / nb_camions if nb_camions > 0 else 0)},
        {"Catégorie": "Transport", "Indicateur": "Total Missions Exécutées", "Valeur": f"{nb_om}"},
        {"Catégorie": "Transport", "Indicateur": "Nombre de Camions", "Valeur": f"{nb_camions}"},
        {"Catégorie": "RH", "Indicateur": "Effectif Chauffeurs", "Valeur": f"{nb_chauffeurs}"},
        {"Catégorie": "RH", "Indicateur": "Productivité Chauffeur (CA/Conducteur)", "Valeur": format_currency(total_ca_annuel / nb_chauffeurs if nb_chauffeurs > 0 else 0)},
        {"Catégorie": "Commercial", "Indicateur": "Nombre de Clients", "Valeur": f"{nb_clients}"},
        {"Catégorie": "Commercial", "Indicateur": "Nombre de Commandes", "Valeur": f"{nb_commandes}"}
    ])

    show_table(kpi_summary, "kpi_summary_table")

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        © 2026 TMF Logistics — Solution Intégrée Analytics Transport & RH
    </div>
    """,
    unsafe_allow_html=True
)
