import streamlit as st
import pandas as pd
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TMF LOGISTICS - Rapports",
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
    "code vehicule": "Camion",
    "Code vehicule": "Camion",
    "code véhicule": "Camion",
    "Code véhicule": "Camion",
    "Code Vehicule": "Camion"
}

# ============================================================
# FONCTIONS UTILITAIRES & CHARGEMENT
# ============================================================

def nettoyer_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.astype(str).str.strip()
    
    df = df.rename(columns=CORRESPONDANCE_COLONNES)
    
    obj_cols = df.select_dtypes(include=["object"]).columns
    for col in obj_cols:
        df[col] = df[col].fillna("").astype(str).str.strip()
        
    return df

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
            st.error(f"❌ Erreur lors de la lecture de {chemin.name} : {e}")
            return pd.DataFrame()

# Chargement
df_om = charger_excel(FICHIER_OM, FEUILLE_OM)
df_chauffeurs = charger_excel(FICHIER_CHAUFFEURS, FEUILLE_CHAUFFEURS)
df_clients = charger_excel(FICHIER_CLIENTS)
df_commandes = charger_excel(FICHIER_COMMANDES, FEUILLE_COMMANDES)

# Convertir les colonnes spécifiques de df_commandes
if not df_commandes.empty:
    for col in ["Date de Mission", "Date Heure Charg Planif"]:
        if col in df_commandes.columns:
            df_commandes[col] = pd.to_datetime(df_commandes[col], errors="coerce")
            
    num_cols = ["Prix unitaire", "Quantité restante", "Tonnage", "Montant ligne HT", "Quantité", "Quantité réservée (base)"]
    for col in num_cols:
        if col in df_commandes.columns:
            df_commandes[col] = pd.to_numeric(df_commandes[col], errors="coerce")

# ============================================================
# TITRE
# ============================================================

st.title("📊 Rapports & Analyse")
st.subheader("Analyse des données de TMF LOGISTICS")
st.caption("Analyse croisée des Ordres de Mission, Commandes de vente, Chauffeurs et Clients.")

if df_om.empty:
    st.error(f"❌ Impossible de charger les Ordres de Mission.\nFichier : `{FICHIER_OM}`")
    st.stop()

# ============================================================
# SIDEBAR / FILTRES
# ============================================================

st.sidebar.header("🔎 Filtres du rapport")

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
        return sorted([str(x) for x in df[col].dropna().unique() if str(x).strip()])
    return []

col_client_filter = "Nom client" if "Nom client" in df_om.columns else "Client"

filtre_statut = st.sidebar.multiselect("📊 Statut", extraire_options(df_om, "Status"), key="f_statut")
filtre_client = st.sidebar.multiselect("👥 Client", extraire_options(df_om, col_client_filter), key="f_client")
filtre_chauffeur = st.sidebar.multiselect("👷 Chauffeur", extraire_options(df_om, "Chauffeur"), key="f_chauffeur")
filtre_section = st.sidebar.multiselect("🏢 Section", extraire_options(df_om, "Section"), key="f_section")

# ============================================================
# FILTRAGE
# ============================================================

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
if filtre_section and "Section" in df_analyse.columns:
    df_analyse = df_analyse[df_analyse["Section"].isin(filtre_section)]

df_commandes_analyse = df_commandes.copy()
if isinstance(periode, tuple) and len(periode) == 2 and "Date de Mission" in df_commandes_analyse.columns:
    df_commandes_analyse = df_commandes_analyse[
        (df_commandes_analyse["Date de Mission"] >= date_debut) & 
        (df_commandes_analyse["Date de Mission"] < date_fin)
    ]

# ============================================================
# SYNTHÈSE ET KPI
# ============================================================

st.divider()
st.header("📊 Synthèse générale")

col_camion = "Numero Camion" if "Numero Camion" in df_analyse.columns else "Camion"

nombre_om = len(df_analyse)
nombre_camions = df_analyse[col_camion].replace("", pd.NA).nunique() if col_camion in df_analyse.columns else 0
nombre_chauffeurs = df_analyse["Chauffeur"].replace("", pd.NA).nunique() if "Chauffeur" in df_analyse.columns else 0
nombre_clients = df_analyse[col_client_filter].replace("", pd.NA).nunique() if col_client_filter in df_analyse.columns else 0

nombre_commandes = df_commandes_analyse["N° document"].replace("", pd.NA).nunique() if "N° document" in df_commandes_analyse.columns else len(df_commandes_analyse)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("📋 Ordres de Mission", nombre_om)
col2.metric("🚚 Camions", nombre_camions)
col3.metric("👷 Chauffeurs", nombre_chauffeurs)
col4.metric("👥 Clients", nombre_clients)
col5.metric("📦 Commandes de vente", nombre_commandes)

# ============================================================
# ANALYSE CROISÉE
# ============================================================

st.divider()
st.header("🔗 Analyse croisée : Commandes de vente → OM → Camions → Chauffeurs")
st.caption("Cette analyse rapproche les commandes de vente des Ordres de Mission.")

if df_commandes_analyse.empty or df_analyse.empty:
    st.warning("⚠️ Impossible de réaliser l'analyse croisée : données de commandes ou d'OM insuffisantes.")
else:
    col_om_cmd = None
    for nom_col in ["Ordre de Mission", "Numéro", "N° OM", "Code"]:
        if nom_col in df_commandes_analyse.columns:
            col_om_cmd = nom_col
            break

    col_om_main = None
    for nom_col in ["Code", "Numéro", "Ordre de Mission", "N° OM"]:
        if nom_col in df_analyse.columns:
            col_om_main = nom_col
            break

    if col_om_cmd and col_om_main:
        df_croise = pd.merge(
            df_commandes_analyse,
            df_analyse,
            left_on=col_om_cmd,
            right_on=col_om_main,
            how="inner",
            suffixes=("_CMD", "_OM")
        )

        col_clef_nommee = col_om_cmd if col_om_cmd in df_croise.columns else col_om_main
        
        # Renommage explicite de Ordre de Mission et de Camion_CMD -> Numero Camion
        df_croise = df_croise.rename(columns={
            col_clef_nommee: "Ordre de Mission",
            "Camion_CMD": "Numero Camion",
            "Camion_Cmd": "Numero Camion"
        })
        
        cols = ["Ordre de Mission"] + [c for c in df_croise.columns if c != "Ordre de Mission"]
        df_croise = df_croise[cols]

        st.subheader(f"📌 {len(df_croise)} lignes associées trouvées")
        st.dataframe(df_croise, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Clef de liaison 'Ordre de Mission' introuvable dans les jeux de données.")
