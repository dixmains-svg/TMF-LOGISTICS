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
nb_commandes = len(commandes)
nb_om = len(om)
total_ca_annuel = df_ca["GLOBAL"].sum()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    if os.path.isfile(LOGO_FILE):
        st.image(LOGO_FILE, width=120)
    else:
        st.markdown('<div style="font-size:55px; text-align:center; padding:10px;">🚚</div>', unsafe_allow_html=True)

    st.markdown("---")

    menu = st.radio(
        "MENU",
        [
            "🏠 Accueil",
            "💰 Chiffre d'Affaires",
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
    st.markdown('<div style="font-size:13px; font-weight:600; color:#0b5d3b; margin-bottom:8px;">📁 Fichiers de données</div>', unsafe_allow_html=True)

    for name, path in FILES.items():
        if os.path.isfile(path):
            st.markdown(f'<div style="font-size:11px; color:#16834b; margin-bottom:3px;">✓ {os.path.basename(path)}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="font-size:11px; color:#c0392b; margin-bottom:3px;">✗ {os.path.basename(path)}</div>', unsafe_allow_html=True)

# ============================================================
# HEADER CENTRAL
# ============================================================

st.markdown('<div class="tmf-header">', unsafe_allow_html=True)
col_logo, col_title = st.columns([1, 6], vertical_alignment="center")

with col_logo:
    if os.path.isfile(LOGO_FILE):
        st.image(LOGO_FILE, width=110)
    else:
        st.markdown('<div style="font-size:60px; text-align:center;">🚚</div>', unsafe_allow_html=True)

with col_title:
    st.markdown(
        """
        <div style="font-size:32px; font-weight:700; color:white; text-align:left; line-height:1.2;">
            Gestion de la flotte TMF Logistics
        </div>
        <div style="margin-top:8px; font-size:15px; color:#e8f5ef; text-align:left;">
            Transport & Logistique
        </div>
        """,
        unsafe_allow_html=True
    )
st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# ACCUEIL
# ============================================================

if menu == "🏠 Accueil":

    st.markdown('<div class="section-title">🏠 Tableau de bord</div>', unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f'<div class="info-card"><div class="info-card-title">💰 CA Annuel</div><div class="info-card-value">{format_currency(total_ca_annuel)}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="info-card"><div class="info-card-title">🚛 Camions</div><div class="info-card-value">{nb_camions}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="info-card"><div class="info-card-title">👨‍✈️ Chauffeurs</div><div class="info-card-value">{nb_chauffeurs}</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="info-card"><div class="info-card-title">👥 Clients</div><div class="info-card-value">{nb_clients}</div></div>', unsafe_allow_html=True)
    with col5:
        st.markdown(f'<div class="info-card"><div class="info-card-title">📋 Ordres de Mission</div><div class="info-card-value">{nb_om}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="sub-title">📌 Présentation</div>', unsafe_allow_html=True)
    st.info(
        """
        Bienvenue dans l'application **Gestion de la flotte TMF Logistics**.
        Suivez les performances financières (CA par section), la flotte de camions, la gestion des chauffeurs, les clients, commandes et ordres de mission.
        """
    )

    st.markdown('<div class="sub-title">📁 État des fichiers</div>', unsafe_allow_html=True)
    file_status = [
        {"Fichier": os.path.basename(path), "Statut": "Disponible" if os.path.isfile(path) else "Introuvable"}
        for name, path in FILES.items()
    ]
    st.dataframe(pd.DataFrame(file_status), use_container_width=True, hide_index=True)

# ============================================================
# CHIFFRE D'AFFAIRES
# ============================================================

elif menu == "💰 Chiffre d'Affaires":

    st.markdown('<div class="section-title">💰 Analyse du Chiffre d\'Affaires par Section</div>', unsafe_allow_html=True)

    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.metric("CA Annuel Total", format_currency(total_ca_annuel))
    with m_col2:
        st.metric("CA Mensuel Moyen", format_currency(total_ca_annuel / 12))
    with m_col3:
        best_section = df_ca.loc[df_ca["GLOBAL"].idxmax(), "CA PAR SECTION"]
        st.metric("Meilleure Section", best_section)
    with m_col4:
        best_month_col = df_ca.drop(columns=["CA PAR SECTION", "GLOBAL"]).sum().idxmax()
        best_month_val = df_ca.drop(columns=["CA PAR SECTION", "GLOBAL"]).sum().max()
        st.metric("Meilleur Mois", f"{best_month_col} ({format_currency(best_month_val)})")

    st.markdown("---")
    st.markdown('<div class="sub-title">📊 Tableau du CA Mensuel et Annuel (en DA)</div>', unsafe_allow_html=True)

    formatted_ca = df_ca.copy()
    for col in formatted_ca.columns:
        if col != "CA PAR SECTION":
            formatted_ca[col] = formatted_ca[col].apply(lambda x: f"{x:,.0f}".replace(",", " "))

    show_table(formatted_ca, "ca_table")

    st.markdown('<div class="sub-title">📈 Contribution des Sections au CA Annuel</div>', unsafe_allow_html=True)
    chart_data = df_ca.set_index("CA PAR SECTION")["GLOBAL"]
    st.bar_chart(chart_data)

    st.markdown('<div class="sub-title">🔗 Croisement avec la Flotte, Ordres de Mission & Commandes</div>', unsafe_allow_html=True)

    cross_analysis = []
    for section in df_ca["CA PAR SECTION"]:
        ca_sec = df_ca[df_ca["CA PAR SECTION"] == section]["GLOBAL"].values[0]
        
        om_count = 0
        if not om.empty:
            match_om = om.astype(str).apply(lambda col: col.str.lower().str.contains(section.lower(), na=False)).any(axis=1)
            om_count = om[match_om].shape[0]

        cmd_count = 0
        if not commandes.empty:
            match_cmd = commandes.astype(str).apply(lambda col: col.str.lower().str.contains(section.lower(), na=False)).any(axis=1)
            cmd_count = commandes[match_cmd].shape[0]

        ratio_om = (ca_sec / om_count) if om_count > 0 else 0

        cross_analysis.append({
            "Section": section,
            "CA Annuel (DA)": format_currency(ca_sec),
            "Part du CA (%)": f"{(ca_sec / total_ca_annuel)*100:.2f} %",
            "Missions identifiées (OM)": om_count,
            "Commandes identifiées": cmd_count,
            "CA Moyen / Mission": format_currency(ratio_om) if ratio_om > 0 else "N/A"
        })

    st.dataframe(pd.DataFrame(cross_analysis), use_container_width=True, hide_index=True)

# ============================================================
# GESTION DU TRANSPORT
# ============================================================

elif menu == "🚚 Gestion du transport":

    st.markdown('<div class="section-title">🚚 Gestion du transport</div>', unsafe_allow_html=True)
    st.write("Suivi et analyse des données liées à l'activité de transport.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Camions", nb_camions)
    with col2:
        st.metric("Chauffeurs", nb_chauffeurs)
    with col3:
        st.metric("Ordres de mission", nb_om)
    with col4:
        st.metric("Chiffre d'Affaires Total", format_currency(total_ca_annuel))

    st.markdown('<div class="sub-title">🔎 Recherche globale dans toutes les bases</div>', unsafe_allow_html=True)

    search_text = st.text_input("Rechercher", placeholder="Saisissez une référence, un camion, un client...")

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
                result = search_data(df, search_text)
                if not result.empty:
                    st.markdown(f"### {name}")
                    show_table(result, f"transport_{name}")

# ============================================================
# ORDRES DE MISSION
# ============================================================

elif menu == "📋 Ordres de Mission":

    st.markdown('<div class="section-title">📋 Ordres de Mission</div>', unsafe_allow_html=True)

    if om.empty:
        st.warning("Aucune donnée OM disponible.")
    else:
        st.write(f"Nombre de lignes : **{nb_om}**")

        search_om = st.text_input("🔎 Rechercher dans les Ordres de Mission", key="search_om")
        filtered_om = search_data(om, search_om)

        filter_col1, filter_col2 = st.columns(2)

        with filter_col1:
            selected_column = st.selectbox("Filtrer par colonne", ["Aucun"] + list(om.columns), key="om_filter_column")

        with filter_col2:
            if selected_column != "Aucun" and selected_column in filtered_om.columns:
                values = filtered_om[selected_column].dropna().astype(str).unique().tolist()
                selected_value = st.selectbox("Valeur", ["Tous"] + sorted(values), key="om_filter_value")
                filtered_om = filter_data(filtered_om, selected_column, selected_value)

        show_table(filtered_om, "om_table")

# ============================================================
# CAMIONS
# ============================================================

elif menu == "🚛 Camions":

    st.markdown('<div class="section-title">🚛 Gestion des camions</div>', unsafe_allow_html=True)

    if camions.empty:
        st.warning("Le fichier Camions.xlsx est vide ou introuvable.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Nombre de camions", nb_camions)
        with col2:
            st.metric("Nombre de colonnes", len(camions.columns))

        search_camions = st.text_input("🔎 Rechercher un camion", key="search_camions")
        filtered_camions = search_data(camions, search_camions)

        show_table(filtered_camions, "camions_table")

# ============================================================
# CHAUFFEURS
# ============================================================

elif menu == "👨‍✈️ Chauffeurs":

    st.markdown('<div class="section-title">👨‍✈️ Gestion des chauffeurs</div>', unsafe_allow_html=True)

    if chauffeurs.empty:
        st.warning("Le fichier Chauffeurs.xlsx est vide ou introuvable.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Nombre de chauffeurs", nb_chauffeurs)
        with col2:
            st.metric("Nombre de colonnes", len(chauffeurs.columns))

        search_chauffeurs = st.text_input("🔎 Rechercher un chauffeur", key="search_chauffeurs")
        filtered_chauffeurs = search_data(chauffeurs, search_chauffeurs)

        show_table(filtered_chauffeurs, "chauffeurs_table")

# ============================================================
# CLIENTS
# ============================================================

elif menu == "👥 Clients":

    st.markdown('<div class="section-title">👥 Gestion des clients</div>', unsafe_allow_html=True)

    if clients.empty:
        st.warning("Le fichier Clients.xlsx est vide ou introuvable.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Nombre de clients", nb_clients)
        with col2:
            st.metric("Nombre de colonnes", len(clients.columns))

        search_clients = st.text_input("🔎 Rechercher un client", key="search_clients")
        filtered_clients = search_data(clients, search_clients)

        show_table(filtered_clients, "clients_table")

# ============================================================
# COMMANDES DE VENTE
# ============================================================

elif menu == "📦 Commandes de vente":

    st.markdown('<div class="section-title">📦 Commandes de vente</div>', unsafe_allow_html=True)

    if commandes.empty:
        st.warning("Le fichier Commande de vente.xlsx est vide ou introuvable.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Commandes", nb_commandes)
        with col2:
            st.metric("Nombre de colonnes", len(commandes.columns))

        search_commandes = st.text_input("🔎 Rechercher une commande", key="search_commandes")
        filtered_commandes = search_data(commandes, search_commandes)

        show_table(filtered_commandes, "commandes_table")

# ============================================================
# RAPPORTS
# ============================================================

elif menu == "📊 Rapports":

    st.markdown('<div class="section-title">📊 Rapports & Synthèse</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">📈 Récapitulatif Général</div>', unsafe_allow_html=True)

    report_data = pd.DataFrame(
        {
            "Indicateur": [
                "Chiffre d'Affaires Total (DA)",
                "Camions",
                "Chauffeurs",
                "Clients",
                "Commandes de vente",
                "Ordres de Mission"
            ],
            "Valeur": [
                format_currency(total_ca_annuel),
                nb_camions,
                nb_chauffeurs,
                nb_clients,
                nb_commandes,
                nb_om
            ]
        }
    )

    st.dataframe(report_data, use_container_width=True, hide_index=True)

    st.markdown('<div class="sub-title">📋 Aperçu explicatif des données</div>', unsafe_allow_html=True)

    report_choice = st.selectbox(
        "Sélectionner les données à afficher",
        [
            "Chiffre d'Affaires",
            "Camions",
            "Chauffeurs",
            "Clients",
            "Commandes de vente",
            "Ordres de Mission"
        ]
    )

    report_datasets = {
        "Chiffre d'Affaires": df_ca,
        "Camions": camions,
        "Chauffeurs": chauffeurs,
        "Clients": clients,
        "Commandes de vente": commandes,
        "Ordres de Mission": om
    }

    selected_report = report_datasets[report_choice]

    if selected_report.empty:
        st.info("Aucune donnée disponible.")
    else:
        report_search = st.text_input("🔎 Rechercher", key="report_search")
        selected_report = search_data(selected_report, report_search)
        show_table(selected_report, "report_table")

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
