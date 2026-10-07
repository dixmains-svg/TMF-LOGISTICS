import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# ==========================================
# 1. CONFIGURATION DE LA PAGE STREAMLIT
# ==========================================
st.set_page_config(
    page_title="TMF Logistics - Dashboard Management",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        color: #1E3A8A;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 25px;
    }
    .metric-card {
        background-color: #F8FAFC;
        border-left: 5px solid #1E3A8A;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">🚛 TMF Logistics - Tableau de Bord Général</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Gestion Flotte, Transport, RH et Suivi d\'Activité</p>', unsafe_allow_html=True)


# ==========================================
# 2. CHARGEMENT ET CACHING DES DONNÉES
# ==========================================
@st.cache_data(show_spinner=False)
def load_data(file_path, sheet_name=0):
    """Charge un fichier Excel de manière sécurisée et optimisée."""
    if not os.path.exists(file_path):
        return pd.DataFrame()
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        # Nettoyage de base des noms de colonnes
        df.columns = [str(c).strip().lower() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Erreur de chargement du fichier {file_path} : {e}")
        return pd.DataFrame()

def find_column_by_keywords(df, keywords):
    """Trouve la première colonne d'un DataFrame correspondant à l'un des mots-clés."""
    if df.empty:
        return None
    for kw in keywords:
        for col in df.columns:
            if kw.lower() in str(col).lower():
                return col
    return None


# Charger vos jeux de données principaux (adapter les noms de fichiers si besoin)
df_om = load_data("ordres_de_mission.xlsx")
df_flotte = load_data("flotte_camions.xlsx")
df_rh = load_data("ressources_humaines.xlsx")
df_commandes = load_data("commandes_clients.xlsx")


# ==========================================
# 3. DÉFINITION DES FILTRES SIDEBAR
# ==========================================
st.sidebar.header("🔍 Filtres Globaux")

# --- A. FILTRE PAR MOIS ---
MOIS_LISTE = [
    "Tous les mois",
    "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
]
mois_selectionne = st.sidebar.selectbox("📅 Mois", MOIS_LISTE)

MOIS_MAP = {
    "Janvier": 1, "Février": 2, "Mars": 3, "Avril": 4, "Mai": 5, "Juin": 6,
    "Juillet": 7, "Août": 8, "Septembre": 9, "Octobre": 10, "Novembre": 11, "Décembre": 12
}

# --- B. FILTRE PAR AFFECTATION / AGENCE ---
AFFECTATIONS_LISTE = ["Toutes les affectations", "Akbou", "Setif", "Alger", "Oran"]
affectation_selectionnee = st.sidebar.selectbox("📍 Affectation / Agence", AFFECTATIONS_LISTE)

# --- C. FILTRE PAR NUMÉRO DE CAMION ---
def extract_camions_list(*dfs):
    camions = set()
    keywords = ["immatriculation", "camion", "code camion", "code_vehicule", "vehicule"]
    for df in dfs:
        if not df.empty:
            col = find_column_by_keywords(df, keywords)
            if col:
                vals = df[col].dropna().astype(str).str.strip().unique()
                camions.update(vals)
    sorted_camions = sorted(list(camions))
    return ["Tous les camions"] + sorted_camions

liste_camions = extract_camions_list(df_flotte, df_om)
camion_selectionne = st.sidebar.selectbox("🚛 Numéro de Camion", liste_camions)


# ==========================================
# 4. FONCTIONS DE FILTRAGE
# ==========================================
def filter_by_month(df, keywords, month_name):
    if df.empty or month_name == "Tous les mois":
        return df
    col = find_column_by_keywords(df, keywords)
    if col:
        try:
            dates = pd.to_datetime(df[col], errors='coerce')
            target_month = MOIS_MAP[month_name]
            return df[dates.dt.month == target_month]
        except Exception:
            return df
    return df

def filter_by_affectation(df, keywords, affectation):
    if df.empty or affectation == "Toutes les affectations":
        return df
    col = find_column_by_keywords(df, keywords)
    if col:
        return df[df[col].astype(str).str.contains(affectation, case=False, na=False)]
    return df

def filter_by_camion(df, keywords, camion):
    if df.empty or camion == "Tous les camions":
        return df
    col = find_column_by_keywords(df, keywords)
    if col:
        return df[df[col].astype(str).str.strip().str.upper() == str(camion).strip().upper()]
    return df

def apply_all_filters(df, date_kw, affect_kw, camion_kw):
    df_filtered = df.copy()
    if not df_filtered.empty:
        df_filtered = filter_by_month(df_filtered, date_kw, mois_selectionne)
        df_filtered = filter_by_affectation(df_filtered, affect_kw, affectation_selectionnee)
        df_filtered = filter_by_camion(df_filtered, camion_kw, camion_selectionne)
    return df_filtered


# Mots-clés pour chaque DataFrame
df_om_f = apply_all_filters(
    df_om, 
    date_kw=["date", "date_om", "date_depart"], 
    affect_kw=["agence", "affectation", "site", "depot"], 
    camion_kw=["camion", "immatriculation", "code_camion", "vehicule"]
)

df_flotte_f = filter_by_camion(
    filter_by_affectation(
        df_flotte, 
        keywords=["agence", "affectation", "site", "depot"], 
        affectation=affectation_selectionnee
    ),
    keywords=["camion", "immatriculation", "code_camion", "code"], 
    camion=camion_selectionne
)

df_rh_f = filter_by_affectation(
    df_rh, 
    keywords=["agence", "affectation", "site", "depot"], 
    affectation=affectation_selectionnee
)

df_commandes_f = apply_all_filters(
    df_commandes, 
    date_kw=["date", "date_commande", "date_livraison"], 
    affect_kw=["agence", "affectation", "site", "region"], 
    camion_kw=["camion", "immatriculation", "code_camion"]
)


# ==========================================
# 5. NAVIGATION / PAGES
# ==========================================
menu = st.sidebar.radio(
    "📊 Navigation",
    [
        "📈 Chiffre d'Affaires & Synthèse",
        "👥 Ressources Humaines",
        "🚛 Transport & Trajets",
        "🔧 Flotte & Camions",
        "📦 Clients & Commandes"
    ]
)

# ------------------------------------------
# PAGE 1 : CHIFFRE D'AFFAIRES & SYNTHÈSE
# ------------------------------------------
if menu == "📈 Chiffre d'Affaires & Synthèse":
    st.title("📈 Synthèse Financière & Chiffre d'Affaires")
    
    col1, col2, col3, col4 = st.columns(4)
    
    ca_col = find_column_by_keywords(df_om_f, ["ca", "montant", "prix", "chiffre_affaires", "recette"])
    total_ca = df_om_f[ca_col].sum() if ca_col and not df_om_f.empty else 0
    
    trajet_col = find_column_by_keywords(df_om_f, ["om", "id", "code_om", "trajet"])
    total_trajets = len(df_om_f) if not df_om_f.empty else 0
    
    km_col = find_column_by_keywords(df_om_f, ["km", "kilometrage", "distance"])
    total_km = df_om_f[km_col].sum() if km_col and not df_om_f.empty else 0
    
    col1.metric("Chiffre d'Affaires Total", f"{total_ca:,.2f} DZD")
    col2.metric("Nombre de Trajets (OM)", f"{total_trajets:,}")
    col3.metric("Distance Totale", f"{total_km:,.0f} Km")
    col4.metric("Nbr Camions Actifs", f"{len(df_flotte_f):,}")
    
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📊 Répartition du CA par Agence / Affectation")
        aff_col = find_column_by_keywords(df_om_f, ["agence", "affectation", "site"])
        if aff_col and ca_col and not df_om_f.empty:
            df_ca_aff = df_om_f.groupby(aff_col)[ca_col].sum().reset_index()
            fig = px.pie(df_ca_aff, values=ca_col, names=aff_col, hole=0.4, title="CA par Agence")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Données insuffisantes pour afficher la répartition du CA par agence.")
            
    with col_right:
        st.subheader("🚛 Top Camions par CA Généré")
        cam_col = find_column_by_keywords(df_om_f, ["camion", "immatriculation", "code_camion"])
        if cam_col and ca_col and not df_om_f.empty:
            df_top_camion = df_om_f.groupby(cam_col)[ca_col].sum().reset_index().sort_values(by=ca_col, ascending=False).head(10)
            fig_bar = px.bar(df_top_camion, x=cam_col, y=ca_col, labels={cam_col: "Camion", ca_col: "CA (DZD)"}, title="Top 10 Camions")
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Données insuffisantes pour le classement des camions.")

# ------------------------------------------
# PAGE 2 : RESSOURCES HUMAINES
# ------------------------------------------
elif menu == "👥 Ressources Humaines":
    st.title("👥 Gestion des Ressources Humaines (Chauffeurs & Personnel)")
    
    col1, col2, col3 = st.columns(3)
    
    total_agents = len(df_rh_f) if not df_rh_f.empty else 0
    post_col = find_column_by_keywords(df_rh_f, ["poste", "fonction", "role", "metier"])
    
    chauffeurs_count = 0
    if post_col and not df_rh_f.empty:
        chauffeurs_count = df_rh_f[df_rh_f[post_col].astype(str).str.contains("chauffeur|conducteur", case=False, na=False)].shape[0]
        
    col1.metric("Effectif Total", f"{total_agents:,}")
    col2.metric("Chauffeurs", f"{chauffeurs_count:,}")
    col3.metric("Hors Chauffeurs", f"{total_agents - chauffeurs_count:,}")
    
    st.markdown("---")
    st.subheader("📋 Liste des collaborateurs")
    if not df_rh_f.empty:
        st.dataframe(df_rh_f, use_container_width=True)
    else:
        st.warning("Aucune donnée RH disponible pour les filtres sélectionnés.")

# ------------------------------------------
# PAGE 3 : TRANSPORT & TRAJETS
# ------------------------------------------
elif menu == "🚛 Transport & Trajets":
    st.title("🚛 Suivi du Transport et des Ordres de Mission (OM)")
    
    if not df_om_f.empty:
        col1, col2, col3 = st.columns(3)
        
        km_col = find_column_by_keywords(df_om_f, ["km", "kilometrage", "distance"])
        carbu_col = find_column_by_keywords(df_om_f, ["gazole", "carburant", "gasoil", "litre"])
        
        tot_km = df_om_f[km_col].sum() if km_col else 0
        tot_carbu = df_om_f[carbu_col].sum() if carbu_col else 0
        conso_moyenne = (tot_carbu / tot_km * 100) if tot_km > 0 else 0
        
        col1.metric("Kilométrage Parcouru", f"{tot_km:,.0f} Km")
        col2.metric("Consommation Carburant", f"{tot_carbu:,.0f} L")
        col3.metric("Moyenne Consommation", f"{conso_moyenne:.2f} L/100Km")
        
        st.markdown("---")
        st.subheader("📄 DÉTAIL DES ORDRES DE MISSION")
        st.dataframe(df_om_f, use_container_width=True)
    else:
        st.warning("Aucune donnée de transport disponible.")

# ------------------------------------------
# PAGE 4 : FLOTTE & CAMIONS
# ------------------------------------------
elif menu == "🔧 Flotte & Camions":
    st.title("🔧 Suivi du Parc Automobile & Flotte")
    
    if not df_flotte_f.empty:
        st.metric("Nombre total de véhicules répertoriés", f"{len(df_flotte_f):,}")
        st.markdown("---")
        
        statut_col = find_column_by_keywords(df_flotte_f, ["statut", "etat", "disponibilite"])
        if statut_col:
            st.subheader("📊 État de la Flotte")
            fig_statut = px.pie(df_flotte_f, names=statut_col, title="Répartition par Statut")
            st.plotly_chart(fig_statut, use_container_width=True)
            
        st.subheader("🚚 Inventaire de la Flotte")
        st.dataframe(df_flotte_f, use_container_width=True)
    else:
        st.warning("Aucune donnée de flotte disponible.")

# ------------------------------------------
# PAGE 5 : CLIENTS & COMMANDES
# ------------------------------------------
elif menu == "📦 Clients & Commandes":
    st.title("📦 Suivi des Clients et Commandes")
    
    if not df_commandes_f.empty:
        col1, col2 = st.columns(2)
        
        client_col = find_column_by_keywords(df_commandes_f, ["client", "nom_client", "societe"])
        vol_col = find_column_by_keywords(df_commandes_f, ["quantite", "tonnage", "poids", "volume"])
        
        tot_commandes = len(df_commandes_f)
        tot_vol = df_commandes_f[vol_col].sum() if vol_col else 0
        
        col1.metric("Commandes Enregistrées", f"{tot_commandes:,}")
        col2.metric("Volume / Tonnage Total", f"{tot_vol:,.2f}")
        
        st.markdown("---")
        if client_col and vol_col:
            st.subheader("🏢 Top 10 Clients")
            df_client_top = df_commandes_f.groupby(client_col)[vol_col].sum().reset_index().sort_values(by=vol_col, ascending=False).head(10)
            fig_client = px.bar(df_client_top, x=client_col, y=vol_col, title="Volume transporté par Client")
            st.plotly_chart(fig_client, use_container_width=True)
            
        st.dataframe(df_commandes_f, use_container_width=True)
    else:
        st.warning("Aucune donnée de commande disponible.")
