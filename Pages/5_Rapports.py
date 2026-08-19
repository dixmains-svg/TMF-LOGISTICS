import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ============================================================
# CONFIGURATION DE LA PAGE
# ============================================================

st.set_page_config(
    page_title="TMF LOGISTICS - Analyse Approfondie",
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
    "Camion": "Numero Camion"
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

# Conversions de types
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

st.title("📊 Rapports & Analyse Approfondie")
st.caption("Tableau de bord décisionnel : Ordres de Mission, Commandes, Flotte et Clients.")

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

filtre_statut = st.sidebar.multiselect("📊 Statut OM", extraire_options(df_om, "Status"), key="f_statut")
filtre_client = st.sidebar.multiselect("👥 Nom Client", extraire_options(df_om, col_client_filter), key="f_client")
filtre_chauffeur = st.sidebar.multiselect("👷 Chauffeur", extraire_options(df_om, "Chauffeur"), key="f_chauffeur")
filtre_section = st.sidebar.multiselect("🏢 Section", extraire_options(df_om, "Section"), key="f_section")

# ============================================================
# FILTRAGE DES DONNÉES
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
# RAPPROCHEMENT DES DONNÉES
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
        "Camion_Cmd": "Numero Camion"
    })
    cols = ["Ordre de Mission"] + [c for c in df_croise.columns if c != "Ordre de Mission"]
    df_croise = df_croise[cols]
else:
    df_croise = pd.DataFrame()

# ============================================================
# SYNTHÈSE & KPIS AVANCÉS
# ============================================================

st.divider()
st.header("📈 Synthèse globale & Performance")

total_ca = df_commandes_analyse["Montant ligne HT"].sum() if "Montant ligne HT" in df_commandes_analyse.columns else 0
total_tonnage = df_commandes_analyse["Tonnage"].sum() if "Tonnage" in df_commandes_analyse.columns else 0
nb_om = len(df_analyse)
nb_camions = df_analyse["Numero Camion"].replace("", pd.NA).nunique() if "Numero Camion" in df_analyse.columns else 0
nb_chauffeurs = df_analyse["Chauffeur"].replace("", pd.NA).nunique() if "Chauffeur" in df_analyse.columns else 0
nb_clients = df_analyse[col_client_filter].replace("", pd.NA).nunique() if col_client_filter in df_analyse.columns else 0

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("💰 CA Total (HT)", f"{total_ca:,.2f} DA")
c2.metric("⚖️ Tonnage Total", f"{total_tonnage:,.2f} T")
c3.metric("📋 Ordres de Mission", f"{nb_om:,}")
c4.metric("🚚 Camions Actifs", f"{nb_camions}")
c5.metric("👷 Chauffeurs", f"{nb_chauffeurs}")
c6.metric("👥 Clients Servis", f"{nb_clients}")

# ============================================================
# ONGLETS D'ANALYSE APPROFONDIE
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "💼 Analyse Commerciale & Clients", 
    "🚚 Flotte & Chauffeurs", 
    "📅 Évolution Temporelle", 
    "📄 Tableau Croisé Complet"
])

# ------------------------------------------------------------
# TAB 1 : COMMERCIAL & CLIENTS
# ------------------------------------------------------------
with tab1:
    st.subheader("Performance par Client")
    col_left, col_right = st.columns(2)
    
    if not df_commandes_analyse.empty and "Nom client" in df_commandes_analyse.columns and "Montant ligne HT" in df_commandes_analyse.columns:
        ca_client = df_commandes_analyse.groupby("Nom client")["Montant ligne HT"].sum().reset_index().sort_values(by="Montant ligne HT", ascending=False).head(10)
        
        fig_ca = px.bar(
            ca_client, x="Montant ligne HT", y="Nom client", orientation="h",
            title="Top 10 Clients par Chiffre d'Affaires (HT)",
            labels={"Montant ligne HT": "CA (HT)", "Nom client": "Client"},
            color="Montant ligne HT", color_continuous_scale="Viridis"
        )
        fig_ca.update_layout(yaxis={"categoryorder": "total ascending"})
        col_left.plotly_chart(fig_ca, use_container_width=True)
    else:
        col_left.info("Données insuffisantes pour le CA par client.")

    if not df_commandes_analyse.empty and "Nom client" in df_commandes_analyse.columns and "Tonnage" in df_commandes_analyse.columns:
        ton_client = df_commandes_analyse.groupby("Nom client")["Tonnage"].sum().reset_index().sort_values(by="Tonnage", ascending=False).head(10)
        
        fig_ton = px.bar(
            ton_client, x="Tonnage", y="Nom client", orientation="h",
            title="Top 10 Clients par Tonnage Livré",
            labels={"Tonnage": "Tonnage (T)", "Nom client": "Client"},
            color="Tonnage", color_continuous_scale="Plasma"
        )
        fig_ton.update_layout(yaxis={"categoryorder": "total ascending"})
        col_right.plotly_chart(fig_ton, use_container_width=True)
    else:
        col_right.info("Données insuffisantes pour le tonnage par client.")

# ------------------------------------------------------------
# TAB 2 : FLOTTE & CHAUFFEURS
# ------------------------------------------------------------
with tab2:
    st.subheader("Activité de la Flotte et des Chauffeurs")
    col_flotte, col_statut = st.columns(2)
    
    if "Numero Camion" in df_analyse.columns:
        top_camions = df_analyse["Numero Camion"].value_counts().reset_index()
        top_camions.columns = ["Numero Camion", "Nombre de Missions"]
        top_camions = top_camions[top_camions["Numero Camion"] != ""].head(10)
        
        fig_cam = px.bar(
            top_camions, x="Numero Camion", y="Nombre de Missions",
            title="Top 10 Camions les plus Sollicités",
            color="Nombre de Missions", color_continuous_scale="Blues"
        )
        col_flotte.plotly_chart(fig_cam, use_container_width=True)
        
    if "Status" in df_analyse.columns:
        statut_counts = df_analyse["Status"].value_counts().reset_index()
        statut_counts.columns = ["Status", "Total"]
        
        fig_pie = px.pie(
            statut_counts, names="Status", values="Total",
            title="Répartition des Ordres de Mission par Statut",
            hole=0.4
        )
        col_statut.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("Charge de travail par Chauffeur")
    if "Chauffeur" in df_analyse.columns:
        top_chauffeurs = df_analyse["Chauffeur"].value_counts().reset_index()
        top_chauffeurs.columns = ["Chauffeur", "Nombre de Missions"]
        top_chauffeurs = top_chauffeurs[top_chauffeurs["Chauffeur"] != ""].head(15)
        
        fig_ch = px.bar(
            top_chauffeurs, x="Chauffeur", y="Nombre de Missions",
            title="Top 15 Chauffeurs par Nombre de Missions",
            color="Nombre de Missions", color_continuous_scale="Greens"
        )
        st.plotly_chart(fig_ch, use_container_width=True)

# ------------------------------------------------------------
# TAB 3 : ÉVOLUTION TEMPORELLE
# ------------------------------------------------------------
with tab3:
    st.subheader("Évolution Journalière des Missions")
    if "Date Depart" in df_analyse.columns and not df_analyse["Date Depart"].dropna().empty:
        df_temp = df_analyse.groupby(df_analyse["Date Depart"].dt.date).size().reset_index(name="Nombre d'OM")
        
        fig_line = px.line(
            df_temp, x="Date Depart", y="Nombre d'OM",
            title="Nombre d'Ordres de Mission par Jour",
            markers=True
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("Aucune donnée temporelle disponible pour tracer le graphique.")

# ------------------------------------------------------------
# TAB 4 : TABLEAU CROISÉ DÉTAILLÉ
# ------------------------------------------------------------
with tab4:
    st.subheader("Données Croisées Rapprochées")
    if not df_croise.empty:
        st.caption(f"📌 {len(df_croise)} lignes trouvées après croisement.")
        st.dataframe(df_croise, use_container_width=True, hide_index=True)
        
        # Export CSV
        csv = df_croise.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Télécharger le tableau croisé (CSV)",
            data=csv,
            file_name="Analyse_Croisee_TMF.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ Aucun croisement possible avec les filtres sélectionnés.")
