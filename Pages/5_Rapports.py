import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ============================================================
# CONFIGURATION DE LA PAGE
# ============================================================

st.set_page_config(
    page_title="TMF LOGISTICS - Analyse Professionnelle",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# CHEMINS & CONSTANTES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

FICHIER_OM = BASE_DIR / "Data" / "OM.xlsx"
FICHIER_CHAUFFEURS = BASE_DIR / "Data" / "Chauffeurs.xlsx"
FICHIER_CLIENTS = BASE_DIR / "Data" / "Clients.xlsx"
FICHIER_COMMANDES = BASE_DIR / "Data" / "Commande de vente.xlsx"

FEUILLE_OM = "Input OM fini"
FEUILLE_CHAUFFEURS = "Chauffeurs"
FEUILLE_COMMANDES = "Feuil1"

CORRESPONDANCE_COLONNES = {
    "code convention": "Nom client",
    "Code convention": "Nom client",
    "Code Convention": "Nom client",
    "Client": "Nom client",
    "code vehicule": "Numero Camion",
    "Code vehicule": "Numero Camion",
    "code véhicule": "Numero Camion",
    "Code véhicule": "Numero Camion",
    "Code Vehicule": "Numero Camion",
    "Camion": "Numero Camion",
    "Camion_CMD": "Numero Camion",
    "Camion_Cmd": "Numero Camion",
}

# ============================================================
# FONCTIONS UTILITAIRES & NETTOYAGE STRICT
# ============================================================

def supprimer_colonnes_vides(df: pd.DataFrame) -> pd.DataFrame:
    """Supprime les colonnes totalement vides ou ne contenant que des chaînes vides/NaN."""
    if df.empty:
        return df
    cols_a_garder = []
    for col in df.columns:
        valeurs_propres = df[col].replace(["", "nan", "NaN", "None"], pd.NA).dropna()
        if not valeurs_propres.empty:
            cols_a_garder.append(col)
    return df[cols_a_garder]

def nettoyer_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    df = df.copy()
    df.columns = df.columns.astype(str).str.strip()
    df = df.rename(columns=CORRESPONDANCE_COLONNES)
    
    # Nettoyage des espaces pour les colonnes texte
    obj_cols = df.select_dtypes(include=["object"]).columns
    for col in obj_cols:
        df[col] = df[col].fillna("").astype(str).str.strip()
        
    return supprimer_colonnes_vides(df)

@st.cache_data(ttl=30)
def charger_excel(chemin: Path, feuille: str = None) -> pd.DataFrame:
    if not chemin.exists():
        return pd.DataFrame()
    try:
        kwargs = {"sheet_name": feuille} if feuille else {}
        df = pd.read_excel(chemin, engine="openpyxl", **kwargs)
        return nettoyer_dataframe(df)
    except Exception:
        try:
            df = pd.read_excel(chemin, engine="openpyxl")
            return nettoyer_dataframe(df)
        except Exception as e:
            st.error(f"❌ Erreur de lecture ({chemin.name}) : {e}")
            return pd.DataFrame()

# Chargement des données
df_om = charger_excel(FICHIER_OM, FEUILLE_OM)
df_chauffeurs = charger_excel(FICHIER_CHAUFFEURS, FEUILLE_CHAUFFEURS)
df_clients = charger_excel(FICHIER_CLIENTS)
df_commandes = charger_excel(FICHIER_COMMANDES, FEUILLE_COMMANDES)

# Conversions de types
if not df_commandes.empty:
    for col in ["Date de Mission", "Date Heure Charg Planif"]:
        if col in df_commandes.columns:
            df_commandes[col] = pd.to_datetime(df_commandes[col], errors="coerce")
            
    num_cols = ["Prix unitaire", "Quantité restante", "Tonnage", "Montant ligne HT", "Quantité", "Quantité réservée (base)"]
    for col in num_cols:
        if col in df_commandes.columns:
            df_commandes[col] = pd.to_numeric(df_commandes[col], errors="coerce").fillna(0)

# ============================================================
# TITRE ET EN-TÊTE
# ============================================================

st.title("📊 Analyse Décisionnelle - TMF LOGISTICS")
st.caption("Rapport de performance analytique : Flotte, Chauffeurs et Portefeuille Clients.")

if df_om.empty:
    st.error(f"❌ Les données des Ordres de Mission sont introuvables : `{FICHIER_OM}`")
    st.stop()

# ============================================================
# FILTRES DYNAMIQUES
# ============================================================

st.sidebar.header("🔎 Filtres d'Analyse")

if "Date Depart" in df_om.columns:
    df_om["Date Depart"] = pd.to_datetime(df_om["Date Depart"], errors="coerce")
    dates_valides = df_om["Date Depart"].dropna()
else:
    dates_valides = pd.Series(dtype="datetime64[ns]")

if not dates_valides.empty:
    date_min = dates_valides.min().date()
    date_max = dates_valides.max().date()
    periode = st.sidebar.date_input(
        "📅 Période",
        value=(date_min, date_max),
        min_value=date_min,
        max_value=date_max,
        key="rapport_periode"
    )
else:
    periode = ()

def extraire_options(df: pd.DataFrame, col: str) -> list:
    if col in df.columns:
        return sorted([str(x) for x in df[col].replace(["", "nan", "None"], pd.NA).dropna().unique()])
    return []

col_client_filter = "Nom client" if "Nom client" in df_om.columns else "Client"

filtre_statut = st.sidebar.multiselect("📊 Statut OM", extraire_options(df_om, "Status"))
filtre_client = st.sidebar.multiselect("👥 Client", extraire_options(df_om, col_client_filter))
filtre_chauffeur = st.sidebar.multiselect("👷 Chauffeur", extraire_options(df_om, "Chauffeur"))
filtre_camion = st.sidebar.multiselect("🚚 Camion", extraire_options(df_om, "Numero Camion"))

# Application des filtres
df_analyse = df_om.copy()

if isinstance(periode, tuple) and len(periode) == 2:
    date_debut = pd.Timestamp(periode[0])
    date_fin = pd.Timestamp(periode[1]) + pd.Timedelta(days=1)
    if "Date Depart" in df_analyse.columns:
        df_analyse = df_analyse[(df_analyse["Date Depart"] >= date_debut) & (df_analyse["Date Depart"] < date_fin)]

if filtre_statut and "Status" in df_analyse.columns:
    df_analyse = df_analyse[df_analyse["Status"].isin(filtre_statut)]
if filtre_client and col_client_filter in df_analyse.columns:
    df_analyse = df_analyse[df_analyse[col_client_filter].isin(filtre_client)]
if filtre_chauffeur and "Chauffeur" in df_analyse.columns:
    df_analyse = df_analyse[df_analyse["Chauffeur"].isin(filtre_chauffeur)]
if filtre_camion and "Numero Camion" in df_analyse.columns:
    df_analyse = df_analyse[df_analyse["Numero Camion"].isin(filtre_camion)]

df_commandes_analyse = df_commandes.copy()
if isinstance(periode, tuple) and len(periode) == 2 and "Date de Mission" in df_commandes_analyse.columns:
    df_commandes_analyse = df_commandes_analyse[
        (df_commandes_analyse["Date de Mission"] >= date_debut) & 
        (df_commandes_analyse["Date de Mission"] < date_fin)
    ]

# ============================================================
# RAPPROCHEMENT DES DONNÉES (INNER JOIN)
# ============================================================

col_om_cmd = next((c for c in ["Ordre de Mission", "Numéro", "N° OM", "Code"] if c in df_commandes_analyse.columns), None)
col_om_main = next((c for c in ["Code", "Numéro", "Ordre de Mission", "N° OM"] if c in df_analyse.columns), None)

if col_om_cmd and col_om_main and not df_commandes_analyse.empty and not df_analyse.empty:
    df_croise = pd.merge(
        df_commandes_analyse,
        df_analyse,
        left_on=col_om_cmd,
        right_on=col_om_main,
        how="inner",
        suffixes=("_CMD", "_OM")
    )
    
    col_clef = col_om_cmd if col_om_cmd in df_croise.columns else col_om_main
    df_croise = df_croise.rename(columns={
        col_clef: "Ordre de Mission",
        "Camion_CMD": "Numero Camion",
        "Camion_Cmd": "Numero Camion",
        "Nom client_CMD": "Nom client",
        "Nom client_OM": "Nom client"
    })
    
    # Élimination des colonnes en double générées par la fusion si nécessaire
    df_croise = df_croise.loc[:, ~df_croise.columns.duplicated()]
    
    # Réorganisation : Ordre de Mission en première position
    cols = ["Ordre de Mission"] + [c for c in df_croise.columns if c != "Ordre de Mission"]
    df_croise = df_croise[cols]
    df_croise = supprimer_colonnes_vides(df_croise)
else:
    df_croise = pd.DataFrame()

# ============================================================
# INDICATEURS CLÉS (KPIs)
# ============================================================

st.divider()
total_ca = df_croise["Montant ligne HT"].sum() if "Montant ligne HT" in df_croise.columns else 0
nb_missions = df_analyse["Ordre de Mission"].replace("", pd.NA).nunique() if "Ordre de Mission" in df_analyse.columns else len(df_analyse)
nb_camions = df_analyse["Numero Camion"].replace(["", "nan"], pd.NA).dropna().nunique() if "Numero Camion" in df_analyse.columns else 0
nb_chauffeurs = df_analyse["Chauffeur"].replace(["", "nan"], pd.NA).dropna().nunique() if "Chauffeur" in df_analyse.columns else 0
nb_clients = df_croise["Nom client"].replace(["", "nan"], pd.NA).dropna().nunique() if "Nom client" in df_croise.columns else 0

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("💰 CA Total (HT)", f"{total_ca:,.2f} DA")
kpi2.metric("📋 Missions Totales", f"{nb_missions:,}")
kpi3.metric("🚚 Camions Actifs", f"{nb_camions}")
kpi4.metric("👷 Chauffeurs Actifs", f"{nb_chauffeurs}")
kpi5.metric("👥 Clients Servis", f"{nb_clients}")

# ============================================================
# SECTION D'ANALYSE PAR ONGLETS
# ============================================================

tab_camion, tab_chauffeur, tab_client, tab_table = st.tabs([
    "🚚 Performance par Camion",
    "👷 Performance par Chauffeur",
    "👥 Performance par Client",
    "📄 Table de Données Croisées"
])

# ------------------------------------------------------------
# ONGLET 1 : ANALYSE PAR CAMION
# ------------------------------------------------------------
with tab_camion:
    st.subheader("Analyse de la Flotte (Camions)")
    c1, c2 = st.columns(2)
    
    # 1. Nombre de missions par camion
    if "Numero Camion" in df_analyse.columns:
        df_cam_missions = (
            df_analyse[df_analyse["Numero Camion"].replace(["", "nan"], pd.NA).notna()]
            .groupby("Numero Camion")
            .size()
            .reset_index(name="Nombre de Missions")
            .sort_values(by="Nombre de Missions", ascending=False)
        )
        
        if not df_cam_missions.empty:
            fig_m_cam = px.bar(
                df_cam_missions, x="Numero Camion", y="Nombre de Missions",
                title="Nombre de Missions par Camion",
                color="Nombre de Missions", color_continuous_scale="Blues",
                text_auto=True
            )
            c1.plotly_chart(fig_m_cam, use_container_width=True)
        else:
            c1.info("Aucune donnée disponible pour le nombre de missions par camion.")
            
    # 2. Chiffre d'affaires par camion
    if not df_croise.empty and "Numero Camion" in df_croise.columns and "Montant ligne HT" in df_croise.columns:
        df_cam_ca = (
            df_croise[df_croise["Numero Camion"].replace(["", "nan"], pd.NA).notna()]
            .groupby("Numero Camion")["Montant ligne HT"]
            .sum()
            .reset_index(name="CA Total (HT)")
            .sort_values(by="CA Total (HT)", ascending=False)
        )
        df_cam_ca = df_cam_ca[df_cam_ca["CA Total (HT)"] > 0]
        
        if not df_cam_ca.empty:
            fig_ca_cam = px.bar(
                df_cam_ca, x="Numero Camion", y="CA Total (HT)",
                title="Chiffre d'Affaires par Camion (HT)",
                color="CA Total (HT)", color_continuous_scale="Viridis",
                text_auto=".2s"
            )
            c2.plotly_chart(fig_ca_cam, use_container_width=True)
        else:
            c2.info("Aucun Chiffre d'Affaires associé aux camions sur cette période.")

# ------------------------------------------------------------
# ONGLET 2 : ANALYSE PAR CHAUFFEUR
# ------------------------------------------------------------
with tab_chauffeur:
    st.subheader("Analyse de la Performance des Chauffeurs")
    col_ch1, col_ch2 = st.columns(2)
    
    if not df_croise.empty and "Chauffeur" in df_croise.columns and "Montant ligne HT" in df_croise.columns:
        df_ch_ca = (
            df_croise[df_croise["Chauffeur"].replace(["", "nan"], pd.NA).notna()]
            .groupby("Chauffeur")["Montant ligne HT"]
            .sum()
            .reset_index(name="CA Généré (HT)")
            .sort_values(by="CA Généré (HT)", ascending=False)
        )
        df_ch_ca = df_ch_ca[df_ch_ca["CA Généré (HT)"] > 0]
        
        if not df_ch_ca.empty:
            fig_ch_ca = px.bar(
                df_ch_ca, y="Chauffeur", x="CA Généré (HT)", orientation="h",
                title="Chiffre d'Affaires par Chauffeur (HT)",
                color="CA Généré (HT)", color_continuous_scale="Cividis",
                text_auto=".2s"
            )
            fig_ch_ca.update_layout(yaxis={"categoryorder": "total ascending"})
            col_ch1.plotly_chart(fig_ch_ca, use_container_width=True)
        else:
            col_ch1.info("Aucune donnée de chiffre d'affaires par chauffeur.")

    if "Chauffeur" in df_analyse.columns:
        df_ch_missions = (
            df_analyse[df_analyse["Chauffeur"].replace(["", "nan"], pd.NA).notna()]
            .groupby("Chauffeur")
            .size()
            .reset_index(name="Nombre de Missions")
            .sort_values(by="Nombre de Missions", ascending=False)
        )
        
        if not df_ch_missions.empty:
            fig_ch_m = px.bar(
                df_ch_missions, y="Chauffeur", x="Nombre de Missions", orientation="h",
                title="Nombre de Missions par Chauffeur",
                color="Nombre de Missions", color_continuous_scale="Teal",
                text_auto=True
            )
            fig_ch_m.update_layout(yaxis={"categoryorder": "total ascending"})
            col_ch2.plotly_chart(fig_ch_m, use_container_width=True)
        else:
            col_ch2.info("Aucune donnée de missions par chauffeur.")

# ------------------------------------------------------------
# ONGLET 3 : ANALYSE PAR CLIENT
# ------------------------------------------------------------
with tab_client:
    st.subheader("Analyse du Portefeuille Client")
    
    if not df_croise.empty and "Nom client" in df_croise.columns and "Montant ligne HT" in df_croise.columns:
        df_cli_ca = (
            df_croise[df_croise["Nom client"].replace(["", "nan"], pd.NA).notna()]
            .groupby("Nom client")["Montant ligne HT"]
            .sum()
            .reset_index(name="CA Client (HT)")
            .sort_values(by="CA Client (HT)", ascending=False)
        )
        df_cli_ca = df_cli_ca[df_cli_ca["CA Client (HT)"] > 0]
        
        if not df_cli_ca.empty:
            fig_cli = px.bar(
                df_cli_ca, x="Nom client", y="CA Client (HT)",
                title="Chiffre d'Affaires par Client (HT)",
                color="CA Client (HT)", color_continuous_scale="Plasma",
                text_auto=".2s"
            )
            st.plotly_chart(fig_cli, use_container_width=True)
        else:
            st.info("Aucun Chiffre d'Affaires client à afficher.")
    else:
        st.info("Données insuffisantes pour établir le classement du CA par client.")

# ------------------------------------------------------------
# ONGLET 4 : TABLEAU DÉTAILLÉ SANS COLONNES VIDES
# ------------------------------------------------------------
with tab_table:
    st.subheader("Visualisation de la Table Croisée Nettoyée")
    
    if not df_croise.empty:
        # Nettoyage supplémentaire pour affichage (suppression des colonnes entièrement vides)
        df_affichage = supprimer_colonnes_vides(df_croise)
        
        st.caption(f"📌 **{len(df_affichage)}** lignes d'analyse croisée répertoriées (Colonnes vides automatiquement masquées).")
        st.dataframe(df_affichage, use_container_width=True, hide_index=True)
        
        # Export CSV
        csv = df_affichage.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Télécharger le tableau nettoyé (CSV)",
            data=csv,
            file_name="Rapport_TMF_Logistics.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ Aucun enregistrement associé trouvé avec les filtres sélectionnés.")
