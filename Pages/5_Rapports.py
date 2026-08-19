import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ============================================================
# CONFIGURATION DE LA PAGE
# ============================================================

st.set_page_config(
    page_title="TMF LOGISTICS - Analyse & Taux d'Exploitation",
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
    """Supprime les colonnes totalement vides ou remplies de valeurs manquantes."""
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

def calculer_taux_transport(df_om: pd.DataFrame, df_commandes: pd.DataFrame, flotte_totale: int):
    """Calcule le taux d'exploitation et les ratios métier du transport."""
    camions_utilises = df_om["Numero Camion"].replace(["", "nan"], pd.NA).dropna().nunique() if "Numero Camion" in df_om.columns else 0
    taux_exploitation = (camions_utilises / flotte_totale * 100) if flotte_totale > 0 else 0
    
    ca_total = df_commandes["Montant ligne HT"].sum() if not df_commandes.empty and "Montant ligne HT" in df_commandes.columns else 0
    ca_par_camion = (ca_total / camions_utilises) if camions_utilises > 0 else 0

    return {
        "Flotte Totale": flotte_totale,
        "Camions Exploités": camions_utilises,
        "Taux d'Exploitation (%)": round(taux_exploitation, 2),
        "CA Total HT (DA)": round(ca_total, 2),
        "CA Moyen / Camion (DA)": round(ca_par_camion, 2)
    }

# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

df_om = charger_excel(FICHIER_OM, FEUILLE_OM)
df_chauffeurs = charger_excel(FICHIER_CHAUFFEURS, FEUILLE_CHAUFFEURS)
df_clients = charger_excel(FICHIER_CLIENTS)
df_commandes = charger_excel(FICHIER_COMMANDES, FEUILLE_COMMANDES)

if not df_commandes.empty:
    for col in ["Date de Mission", "Date Heure Charg Planif"]:
        if col in df_commandes.columns:
            df_commandes[col] = pd.to_datetime(df_commandes[col], errors="coerce")
            
    num_cols = ["Prix unitaire", "Quantité restante", "Tonnage", "Montant ligne HT", "Quantité", "Quantité réservée (base)"]
    for col in num_cols:
        if col in df_commandes.columns:
            df_commandes[col] = pd.to_numeric(df_commandes[col], errors="coerce").fillna(0)

# ============================================================
# TITRE ET PARC TOTAL
# ============================================================

st.title("📊 Rapport & Analyse d'Exploitation - TMF LOGISTICS")
st.caption("Tableau de bord décisionnel : Performance, Taux d'exploitation, Camions et Clients.")

if df_om.empty:
    st.error(f"❌ Les données des Ordres de Mission sont introuvables : `{FICHIER_OM}`")
    st.stop()

# ============================================================
# SIDEBAR / FILTRES ET PARAMÈTRES FLOTTE
# ============================================================

st.sidebar.header("⚙️ Paramètres du Parc")
flotte_saisie = st.sidebar.number_input("🚛 Taille totale de la Flotte (Camions)", min_value=1, value=25)

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

# ============================================================
# FILTRAGE ET CRÉATION DE DF_ANALYSE
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
if filtre_camion and "Numero Camion" in df_analyse.columns:
    df_analyse = df_analyse[df_analyse["Numero Camion"].isin(filtre_camion)]

df_commandes_analyse = df_commandes.copy()
if isinstance(periode, tuple) and len(periode) == 2 and "Date de Mission" in df_commandes_analyse.columns:
    df_commandes_analyse = df_commandes_analyse[
        (df_commandes_analyse["Date de Mission"] >= date_debut) & 
        (df_commandes_analyse["Date de Mission"] < date_fin)
    ]

# ============================================================
# RAPPROCHEMENT ET CRÉATION DE DF_CROISE
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
    
    df_croise = df_croise.loc[:, ~df_croise.columns.duplicated()]
    cols = ["Ordre de Mission"] + [c for c in df_croise.columns if c != "Ordre de Mission"]
    df_croise = df_croise[cols]
    df_croise = supprimer_colonnes_vides(df_croise)
else:
    df_croise = pd.DataFrame()

# ============================================================
# INDICATEURS CLÉS & TAUX D'EXPLOITATION
# ============================================================

st.divider()

# Appel sécurisé : df_analyse et df_croise existent désormais !
kpis = calculer_taux_transport(df_analyse, df_croise, flotte_totale=flotte_saisie)

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("📈 Taux d'Exploitation", f"{kpis['Taux d\'Exploitation (%)']} %")
k2.metric("🚛 Flotte Exploité / Total", f"{kpis['Camions Exploités']} / {kpis['Flotte Totale']}")
k3.metric("💰 CA Total (HT)", f"{kpis['CA Total HT (DA)']:,.2f} DA")
k4.metric("📊 CA Moyen / Camion", f"{kpis['CA Moyen / Camion (DA)']:,.2f} DA")
k5.metric("📋 Missions Totales", f"{len(df_analyse):,}")

# ============================================================
# ONGLETS D'ANALYSE DÉTAILLÉE
# ============================================================

tab_camion, tab_chauffeur, tab_client, tab_table = st.tabs([
    "🚚 Performance par Camion",
    "👷 Performance par Chauffeur",
    "👥 Performance par Client",
    "📄 Table Croisée Nettoyée"
])

# ------------------------------------------------------------
# ONGLET 1 : ANALYSE PAR CAMION
# ------------------------------------------------------------
with tab_camion:
    st.subheader("Analyse de la Flotte et du Taux d'Exploitation")
    c1, c2 = st.columns(2)
    
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
            c1.info("Aucun camion actif à afficher.")

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
            c2.info("Aucun chiffre d'affaires enregistré par camion.")

# ------------------------------------------------------------
# ONGLET 2 : ANALYSE PAR CHAUFFEUR
# ------------------------------------------------------------
with tab_chauffeur:
    st.subheader("Performance et Activité des Chauffeurs")
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
            col_ch1.info("Aucun chiffre d'affaires généré par les chauffeurs.")

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
            col_ch2.info("Aucune mission enregistrée pour les chauffeurs.")

# ------------------------------------------------------------
# ONGLET 3 : ANALYSE PAR CLIENT
# ------------------------------------------------------------
with tab_client:
    st.subheader("Chiffre d'Affaires par Client")
    
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
            st.info("Aucun chiffre d'affaires disponible par client.")

# ------------------------------------------------------------
# ONGLET 4 : TABLEAU DÉTAILLÉ SANS COLONNES VIDES
# ------------------------------------------------------------
with tab_table:
    st.subheader("Tableau de Données Croisées")
    
    if not df_croise.empty:
        df_affichage = supprimer_colonnes_vides(df_croise)
        st.caption(f"📌 **{len(df_affichage)}** lignes d'analyse (Colonnes totalement vides retirées).")
        st.dataframe(df_affichage, use_container_width=True, hide_index=True)
        
        csv = df_affichage.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Télécharger les données (CSV)",
            data=csv,
            file_name="Rapport_TMF_Logistics.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ Aucun enregistrement associé avec les filtres sélectionnés.")
