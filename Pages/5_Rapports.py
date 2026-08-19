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
FICHIER_COMMANDES = BASE_DIR / "Data" / "Commande de vente.xlsx"

FEUILLE_OM = "Input OM fini"
FEUILLE_COMMANDES = "Feuil1"

# Standardisation des noms de colonnes clés
MAPPING_COLONNES = {
    "code convention": "Client",
    "Code convention": "Client",
    "Code Convention": "Client",
    "Nom client": "Client",
    "code vehicule": "Camion",
    "Code vehicule": "Camion",
    "code véhicule": "Camion",
    "Code véhicule": "Camion",
    "Code Vehicule": "Camion",
    "Numero Camion": "Camion",
    "Numéro Camion": "Camion",
    "Driver": "Chauffeur",
    "Conducteur": "Chauffeur",
}

# ============================================================
# NETTOYAGE & CHARGEMENT DES DONNÉES
# ============================================================

def nettoyer_colonnes_vides(df: pd.DataFrame) -> pd.DataFrame:
    """Supprime les colonnes ne contenant aucune valeur utile (NaN, vide, None)."""
    if df.empty:
        return df
    cols_a_garder = []
    for col in df.columns:
        valeurs_reelles = df[col].replace(["", "nan", "NaN", "None", "null"], pd.NA).dropna()
        if not valeurs_reelles.empty:
            cols_a_garder.append(col)
    return df[cols_a_garder]

def nettoyer_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    df = df.copy()
    # Nettoyage des noms de colonnes
    df.columns = df.columns.astype(str).str.strip()
    df = df.rename(columns=MAPPING_COLONNES)
    
    # Nettoyage des valeurs de type texte
    cols_texte = df.select_dtypes(include=["object"]).columns
    for col in cols_texte:
        df[col] = df[col].fillna("").astype(str).str.strip()
        
    return nettoyer_colonnes_vides(df)

@st.cache_data(ttl=30)
def charger_donnees(chemin: Path, feuille: str = None) -> pd.DataFrame:
    if not chemin.exists():
        return pd.DataFrame()
    try:
        kwargs = {"sheet_name": feuille} if feuille else {}
        df = pd.read_excel(chemin, engine="openpyxl", **kwargs)
        return nettoyer_dataframe(df)
    except Exception as e:
        st.error(f"❌ Erreur de chargement (`{chemin.name}`) : {e}")
        return pd.DataFrame()

# Chargement
df_om = charger_donnees(FICHIER_OM, FEUILLE_OM)
df_commandes = charger_donnees(FICHIER_COMMANDES, FEUILLE_COMMANDES)

if df_om.empty:
    st.error(f"❌ Impossible d'accéder aux Ordres de Mission dans `{FICHIER_OM}`.")
    st.stop()

# Conversions numériques pour les commandes
if not df_commandes.empty:
    for col_num in ["Montant ligne HT", "Prix unitaire", "Tonnage", "Quantité"]:
        if col_num in df_commandes.columns:
            df_commandes[col_num] = pd.to_numeric(df_commandes[col_num], errors="coerce").fillna(0)

# ============================================================
# TITRE ET PARC TOTAL
# ============================================================

st.title("📊 Analyse Logistique & Taux d'Exploitation")
st.caption("Suivi rigoureux de l'activité transport, rentabilité et utilisation du parc roulant.")

# ============================================================
# FILTRES DE LA BARRE LATÉRALE
# ============================================================

st.sidebar.header("⚙️ Configuration Flotte")
flotte_totale = st.sidebar.number_input(
    "🚛 Taille globale du parc (Camions disponibles)",
    min_value=1,
    value=25,
    help="Indiquez le nombre total de camions possédés/disponibles dans l'entreprise pour calculer le taux d'exploitation exact."
)

st.sidebar.header("🔎 Filtres de Sélection")

# Filtre par Date
if "Date Depart" in df_om.columns:
    df_om["Date Depart"] = pd.to_datetime(df_om["Date Depart"], errors="coerce")
    dates_valides = df_om["Date Depart"].dropna()
else:
    dates_valides = pd.Series(dtype="datetime64[ns]")

if not dates_valides.empty:
    date_min = dates_valides.min().date()
    date_max = dates_valides.max().date()
    periode = st.sidebar.date_input("📅 Période d'analyse", value=(date_min, date_max))
else:
    periode = ()

# Fonctions d'extraction pour les filtres uniques
def get_options(df: pd.DataFrame, col: str) -> list:
    if col in df.columns:
        return sorted([str(x) for x in df[col].replace(["", "nan", "None"], pd.NA).dropna().unique()])
    return []

filtre_statut = st.sidebar.multiselect("📊 Statut OM", get_options(df_om, "Status"))
filtre_client = st.sidebar.multiselect("👥 Client", get_options(df_om, "Client"))
filtre_chauffeur = st.sidebar.multiselect("👷 Chauffeur", get_options(df_om, "Chauffeur"))
filtre_camion = st.sidebar.multiselect("🚚 Camion", get_options(df_om, "Camion"))

# ============================================================
# APPLICATION DES FILTRES SUR DF_OM
# ============================================================

df_om_filtre = df_om.copy()

if isinstance(periode, tuple) and len(periode) == 2:
    d_start, d_end = pd.Timestamp(periode[0]), pd.Timestamp(periode[1]) + pd.Timedelta(days=1)
    if "Date Depart" in df_om_filtre.columns:
        df_om_filtre = df_om_filtre[(df_om_filtre["Date Depart"] >= d_start) & (df_om_filtre["Date Depart"] < d_end)]

if filtre_statut and "Status" in df_om_filtre.columns:
    df_om_filtre = df_om_filtre[df_om_filtre["Status"].isin(filtre_statut)]
if filtre_client and "Client" in df_om_filtre.columns:
    df_om_filtre = df_om_filtre[df_om_filtre["Client"].isin(filtre_client)]
if filtre_chauffeur and "Chauffeur" in df_om_filtre.columns:
    df_om_filtre = df_om_filtre[df_om_filtre["Chauffeur"].isin(filtre_chauffeur)]
if filtre_camion and "Camion" in df_om_filtre.columns:
    df_om_filtre = df_om_filtre[df_om_filtre["Camion"].isin(filtre_camion)]

# ============================================================
# RAPPROCHEMENT RIGOUREUX (OM / COMMANDES)
# ============================================================

col_om_code = next((c for c in ["Code", "Numéro", "Ordre de Mission", "N° OM"] if c in df_om_filtre.columns), None)
col_cmd_code = next((c for c in ["Ordre de Mission", "Numéro", "N° OM", "Code"] if c in df_commandes.columns), None)

if col_om_code and col_cmd_code and not df_commandes.empty:
    df_fusion = pd.merge(
        df_om_filtre,
        df_commandes,
        left_on=col_om_code,
        right_on=col_cmd_code,
        how="left",
        suffixes=("_OM", "_CMD")
    )
    # Harmonisation des colonnes fusionnées
    if "Camion_OM" in df_fusion.columns:
        df_fusion["Camion"] = df_fusion["Camion_OM"].fillna(df_fusion.get("Camion_CMD", ""))
    if "Client_OM" in df_fusion.columns:
        df_fusion["Client"] = df_fusion["Client_OM"].fillna(df_fusion.get("Client_CMD", ""))
else:
    df_fusion = df_om_filtre.copy()

# Nettoyage de la table fusionnée
df_fusion = nettoyer_colonnes_vides(df_fusion)

# ============================================================
# CALCULS DES LOGIQUES ET INDICATEURS MÉTIERS (KPIs)
# ============================================================

# 1. Camions uniques réellement exploités
camions_actifs = [c for c in df_om_filtre["Camion"].unique() if c not in ["", "nan", "None", "0"]] if "Camion" in df_om_filtre.columns else []
nb_camions_actifs = len(camions_actifs)

# 2. Taux d'exploitation (%)
taux_exploitation = (nb_camions_actifs / flotte_totale * 100) if flotte_totale > 0 else 0.0

# 3. Chiffre d'affaires
ca_total = df_fusion["Montant ligne HT"].sum() if "Montant ligne HT" in df_fusion.columns else 0.0

# 4. Nombre de missions
nb_missions = df_om_filtre[col_om_code].nunique() if col_om_code else len(df_om_filtre)

# 5. Moyenne CA par camion actif
ca_moyen_camion = (ca_total / nb_camions_actifs) if nb_camions_actifs > 0 else 0.0

# ============================================================
# AFFICHAGE DES INDICATEURS CLÉS (KPIS)
# ============================================================

st.divider()

col_kpi1, col_kpi2, col_kpi3, col_kpi4, col_kpi5 = st.columns(5)

col_kpi1.metric(
    "📈 Taux d'Exploitation",
    f"{taux_exploitation:.1f} %",
    delta=f"{nb_camions_actifs}/{flotte_totale} camions",
    help="Proportion des camions de la flotte ayant réalisé au moins une mission sur la période."
)
col_kpi2.metric("📋 Total Missions", f"{nb_missions:,}")
col_kpi3.metric("💰 CA Total (HT)", f"{ca_total:,.2f} DA")
col_kpi4.metric("🚛 CA Moyen / Camion", f"{ca_moyen_camion:,.2f} DA")
col_kpi5.metric("👷 Chauffeurs Actifs", f"{df_om_filtre['Chauffeur'].replace('', pd.NA).dropna().nunique() if 'Chauffeur' in df_om_filtre.columns else 0}")

st.divider()

# ============================================================
# VISUALISATION PAR ONGLETS
# ============================================================

tab_flotte, tab_chauffeur, tab_client, tab_donnees = st.tabs([
    "🚛 Exploitation Flotte (Camions)",
    "👷 Performance Chauffeurs",
    "👥 Performance Clients",
    "📄 Vue Détaillée des Données"
])

# ------------------------------------------------------------
# TAB 1 : CAMIONS & TAUX D'EXPLOITATION
# ------------------------------------------------------------
with tab_flotte:
    st.subheader("Analyse de l'Utilisation de la Flotte")
    c1, c2 = st.columns(2)
    
    # Graphique 1 : Nombre de missions par camion
    if "Camion" in df_om_filtre.columns:
        df_cam_m = (
            df_om_filtre[df_om_filtre["Camion"].replace(["", "nan"], pd.NA).notna()]
            .groupby("Camion")
            .size()
            .reset_index(name="Missions")
            .sort_values(by="Missions", ascending=False)
        )
        if not df_cam_m.empty:
            fig_m = px.bar(
                df_cam_m, x="Camion", y="Missions",
                title="Missions réalisées par Camion",
                color="Missions", color_continuous_scale="Blues", text_auto=True
            )
            c1.plotly_chart(fig_m, use_container_width=True)
        else:
            c1.info("Aucune mission enregistrée pour les camions.")

    # Graphique 2 : CA par Camion
    if "Camion" in df_fusion.columns and "Montant ligne HT" in df_fusion.columns:
        df_cam_ca = (
            df_fusion[df_fusion["Camion"].replace(["", "nan"], pd.NA).notna()]
            .groupby("Camion")["Montant ligne HT"]
            .sum()
            .reset_index(name="CA (HT)")
            .sort_values(by="CA (HT)", ascending=False)
        )
        df_cam_ca = df_cam_ca[df_cam_ca["CA (HT)"] > 0]
        
        if not df_cam_ca.empty:
            fig_ca = px.bar(
                df_cam_ca, x="Camion", y="CA (HT)",
                title="Chiffre d'Affaires généré par Camion (HT)",
                color="CA (HT)", color_continuous_scale="Viridis", text_auto=".2s"
            )
            c2.plotly_chart(fig_ca, use_container_width=True)
        else:
            c2.info("Aucun Chiffre d'Affaires associé aux camions.")

# ------------------------------------------------------------
# TAB 2 : CHAUFFEURS
# ------------------------------------------------------------
with tab_chauffeur:
    st.subheader("Analyse de l'Activité des Chauffeurs")
    ch_c1, ch_c2 = st.columns(2)
    
    if "Chauffeur" in df_om_filtre.columns:
        df_ch_m = (
            df_om_filtre[df_om_filtre["Chauffeur"].replace(["", "nan"], pd.NA).notna()]
            .groupby("Chauffeur")
            .size()
            .reset_index(name="Missions")
            .sort_values(by="Missions", ascending=False)
        )
        if not df_ch_m.empty:
            fig_ch_m = px.bar(
                df_ch_m, y="Chauffeur", x="Missions", orientation="h",
                title="Missions par Chauffeur", color="Missions",
                color_continuous_scale="Teal", text_auto=True
            )
            fig_ch_m.update_layout(yaxis={"categoryorder": "total ascending"})
            ch_c1.plotly_chart(fig_ch_m, use_container_width=True)
        else:
            ch_c1.info("Aucune donnée disponible pour les chauffeurs.")

    if "Chauffeur" in df_fusion.columns and "Montant ligne HT" in df_fusion.columns:
        df_ch_ca = (
            df_fusion[df_fusion["Chauffeur"].replace(["", "nan"], pd.NA).notna()]
            .groupby("Chauffeur")["Montant ligne HT"]
            .sum()
            .reset_index(name="CA (HT)")
            .sort_values(by="CA (HT)", ascending=False)
        )
        df_ch_ca = df_ch_ca[df_ch_ca["CA (HT)"] > 0]
        
        if not df_ch_ca.empty:
            fig_ch_ca = px.bar(
                df_ch_ca, y="Chauffeur", x="CA (HT)", orientation="h",
                title="Chiffre d'Affaires par Chauffeur (HT)", color="CA (HT)",
                color_continuous_scale="Cividis", text_auto=".2s"
            )
            fig_ch_ca.update_layout(yaxis={"categoryorder": "total ascending"})
            ch_c2.plotly_chart(fig_ch_ca, use_container_width=True)
        else:
            ch_c2.info("Aucun chiffre d'affaires généré par chauffeur.")

# ------------------------------------------------------------
# TAB 3 : CLIENTS
# ------------------------------------------------------------
with tab_client:
    st.subheader("Analyse du Portefeuille Clients")
    
    if "Client" in df_fusion.columns and "Montant ligne HT" in df_fusion.columns:
        df_cli_ca = (
            df_fusion[df_fusion["Client"].replace(["", "nan"], pd.NA).notna()]
            .groupby("Client")["Montant ligne HT"]
            .sum()
            .reset_index(name="CA Client (HT)")
            .sort_values(by="CA Client (HT)", ascending=False)
        )
        df_cli_ca = df_cli_ca[df_cli_ca["CA Client (HT)"] > 0]
        
        if not df_cli_ca.empty:
            fig_cli = px.bar(
                df_cli_ca, x="Client", y="CA Client (HT)",
                title="Chiffre d'Affaires par Client (HT)",
                color="CA Client (HT)", color_continuous_scale="Plasma", text_auto=".2s"
            )
            st.plotly_chart(fig_cli, use_container_width=True)
        else:
            st.info("Aucun Chiffre d'Affaires client à afficher.")

# ------------------------------------------------------------
# TAB 4 : TABLEAU DE DONNÉES SANS COLONNES VIDES
# ------------------------------------------------------------
with tab_donnees:
    st.subheader("Données Rapprochées et Filtrées")
    
    if not df_fusion.empty:
        df_affichage = nettoyer_colonnes_vides(df_fusion)
        st.caption(f"📌 **{len(df_affichage)}** lignes d'enregistrement trouvées. Les colonnes vides sont automatiquement masquées.")
        st.dataframe(df_affichage, use_container_width=True, hide_index=True)
        
        csv = df_affichage.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Télécharger le rapport (CSV)",
            data=csv,
            file_name="Rapport_Exploitation_TMF.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ Aucun résultat disponible selon les filtres appliqués.")
