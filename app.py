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
# CHEMINS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

FICHIER_OM = BASE_DIR / "Data" / "OM.xlsx"
FICHIER_CHAUFFEURS = BASE_DIR / "Data" / "Chauffeurs.xlsx"
FICHIER_CLIENTS = BASE_DIR / "Data" / "Clients.xlsx"

FEUILLE_OM = "Input OM fini"
FEUILLE_CHAUFFEURS = "Chauffeurs"


# ============================================================
# FONCTION DE NETTOYAGE
# ============================================================

def nettoyer_dataframe(df):

    df = df.copy()

    # Nettoyage des noms de colonnes
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    # Nettoyage des valeurs texte
    for colonne in df.columns:

        if df[colonne].dtype == "object":

            df[colonne] = (
                df[colonne]
                .fillna("")
                .astype(str)
                .str.strip()
            )

    return df


# ============================================================
# LECTURE OM
# ============================================================

@st.cache_data(ttl=30)
def charger_om():

    if not FICHIER_OM.exists():
        return pd.DataFrame()

    try:

        df = pd.read_excel(
            FICHIER_OM,
            sheet_name=FEUILLE_OM,
            engine="openpyxl"
        )

        return nettoyer_dataframe(df)

    except Exception:

        # Essai sans imposer le nom de feuille
        try:

            df = pd.read_excel(
                FICHIER_OM,
                engine="openpyxl"
            )

            return nettoyer_dataframe(df)

        except Exception as e:

            st.error(
                f"❌ Erreur lors de la lecture de OM.xlsx : {e}"
            )

            return pd.DataFrame()


# ============================================================
# LECTURE CHAUFFEURS
# ============================================================

@st.cache_data(ttl=30)
def charger_chauffeurs():

    if not FICHIER_CHAUFFEURS.exists():
        return pd.DataFrame()

    try:

        df = pd.read_excel(
            FICHIER_CHAUFFEURS,
            sheet_name=FEUILLE_CHAUFFEURS,
            engine="openpyxl"
        )

        return nettoyer_dataframe(df)

    except Exception:

        try:

            df = pd.read_excel(
                FICHIER_CHAUFFEURS,
                engine="openpyxl"
            )

            return nettoyer_dataframe(df)

        except Exception as e:

            st.error(
                f"❌ Erreur lors de la lecture de Chauffeurs.xlsx : {e}"
            )

            return pd.DataFrame()


# ============================================================
# LECTURE CLIENTS
# ============================================================

@st.cache_data(ttl=30)
def charger_clients():

    if not FICHIER_CLIENTS.exists():
        return pd.DataFrame()

    try:

        df = pd.read_excel(
            FICHIER_CLIENTS,
            engine="openpyxl"
        )

        return nettoyer_dataframe(df)

    except Exception as e:

        st.error(
            f"❌ Erreur lors de la lecture de Clients.xlsx : {e}"
        )

        return pd.DataFrame()


# ============================================================
# CHARGEMENT
# ============================================================

df_om = charger_om()
df_chauffeurs = charger_chauffeurs()
df_clients = charger_clients()


# ============================================================
# TITRE
# ============================================================

st.title("📊 Rapports & Analyse")

st.subheader(
    "Analyse des données de TMF LOGISTICS"
)

st.caption(
    "Analyse croisée des Ordres de Mission, Chauffeurs et Clients."
)


# ============================================================
# VÉRIFICATION
# ============================================================

if df_om.empty:

    st.error(
        f"""
        ❌ Impossible de charger les Ordres de Mission.

        Fichier :
        `{FICHIER_OM}`
        """
    )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("🔎 Filtres du rapport")


# ============================================================
# PRÉPARATION DES DATES
# ============================================================

if "Date Depart" in df_om.columns:

    df_om["Date Depart"] = pd.to_datetime(
        df_om["Date Depart"],
        errors="coerce"
    )

    dates_valides = (
        df_om["Date Depart"]
        .dropna()
    )

else:

    dates_valides = pd.Series(dtype="datetime64[ns]")


# ============================================================
# FILTRE PÉRIODE
# ============================================================

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

    periode = None


# ============================================================
# FILTRE STATUT
# ============================================================

if "Status" in df_om.columns:

    statuts = sorted(
        [
            str(x)
            for x in df_om["Status"].dropna().unique()
            if str(x).strip()
        ]
    )

else:

    statuts = []


filtre_statut = st.sidebar.multiselect(
    "📊 Statut",
    statuts,
    key="rapport_filtre_statut"
)


# ============================================================
# FILTRE CLIENT
# ============================================================

if "Client" in df_om.columns:

    clients = sorted(
        [
            str(x)
            for x in df_om["Client"].dropna().unique()
            if str(x).strip()
        ]
    )

else:

    clients = []


filtre_client = st.sidebar.multiselect(
    "👥 Client",
    clients,
    key="rapport_filtre_client"
)


# ============================================================
# FILTRE CHAUFFEUR
# ============================================================

if "Chauffeur" in df_om.columns:

    chauffeurs = sorted(
        [
            str(x)
            for x in df_om["Chauffeur"].dropna().unique()
            if str(x).strip()
        ]
    )

else:

    chauffeurs = []


filtre_chauffeur = st.sidebar.multiselect(
    "👷 Chauffeur",
    chauffeurs,
    key="rapport_filtre_chauffeur"
)


# ============================================================
# FILTRE SECTION
# ============================================================

if "Section" in df_om.columns:

    sections = sorted(
        [
            str(x)
            for x in df_om["Section"].dropna().unique()
            if str(x).strip()
        ]
    )

else:

    sections = []


filtre_section = st.sidebar.multiselect(
    "🏢 Section",
    sections,
    key="rapport_filtre_section"
)


# ============================================================
# APPLICATION DES FILTRES
# ============================================================

df_analyse = df_om.copy()


# ------------------------------------------------------------
# PÉRIODE
# ------------------------------------------------------------

if periode is not None and len(periode) == 2:

    date_debut = pd.Timestamp(periode[0])
    date_fin = pd.Timestamp(periode[1])

    if "Date Depart" in df_analyse.columns:

        df_analyse = df_analyse[
            (
                df_analyse["Date Depart"] >=
                date_debut
            )
            &
            (
                df_analyse["Date Depart"] <=
                date_fin
            )
        ].copy()


# ------------------------------------------------------------
# STATUT
# ------------------------------------------------------------

if filtre_statut:

    df_analyse = df_analyse[
        df_analyse["Status"].isin(
            filtre_statut
        )
    ].copy()


# ------------------------------------------------------------
# CLIENT
# ------------------------------------------------------------

if filtre_client:

    df_analyse = df_analyse[
        df_analyse["Client"].isin(
            filtre_client
        )
    ].copy()


# ------------------------------------------------------------
# CHAUFFEUR
# ------------------------------------------------------------

if filtre_chauffeur:

    df_analyse = df_analyse[
        df_analyse["Chauffeur"].isin(
            filtre_chauffeur
        )
    ].copy()


# ------------------------------------------------------------
# SECTION
# ------------------------------------------------------------

if filtre_section:

    df_analyse = df_analyse[
        df_analyse["Section"].isin(
            filtre_section
        )
    ].copy()


# ============================================================
# RÉSUMÉ
# ============================================================

st.divider()

st.header("📊 Synthèse générale")


nombre_om = len(df_analyse)


if "Numero Camion" in df_analyse.columns:

    nombre_camions = (
        df_analyse["Numero Camion"]
        .replace("", pd.NA)
        .nunique()
    )

else:

    nombre_camions = 0


if "Chauffeur" in df_analyse.columns:

    nombre_chauffeurs = (
        df_analyse["Chauffeur"]
        .replace("", pd.NA)
        .nunique()
    )

else:

    nombre_chauffeurs = 0


if "Client" in df_analyse.columns:

    nombre_clients = (
        df_analyse["Client"]
        .replace("", pd.NA)
        .nunique()
    )

else:

    nombre_clients = 0


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "📋 Ordres de Mission",
        nombre_om
    )


with col2:

    st.metric(
        "🚚 Camions",
        nombre_camions
    )


with col3:

    st.metric(
        "👷 Chauffeurs",
        nombre_chauffeurs
    )


with col4:

    st.metric(
        "👥 Clients",
        nombre_clients
    )


# ============================================================
# KILOMÉTRAGE
# ============================================================

st.divider()

st.header("🛣️ Analyse du kilométrage")


if "Kilometrage Parcouru" in df_analyse.columns:

    df_analyse["Kilometrage Parcouru"] = pd.to_numeric(
        df_analyse["Kilometrage Parcouru"],
        errors="coerce"
    )

    km_total = (
        df_analyse["Kilometrage Parcouru"]
        .fillna(0)
        .sum()
    )

    km_moyen = (
        df_analyse["Kilometrage Parcouru"]
        .dropna()
        .mean()
    )

else:

    km_total = 0
    km_moyen = 0


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "🛣️ KM parcourus",
        f"{km_total:,.0f}"
    )


with col2:

    st.metric(
        "📏 KM moyen / OM",
        f"{km_moyen:,.0f}"
        if pd.notna(km_moyen)
        else "0"
    )


# ============================================================
# ANALYSE PAR STATUT
# ============================================================

st.divider()

st.header("📊 Répartition des Ordres de Mission par statut")


if "Status" in df_analyse.columns:

    analyse_statut = (
        df_analyse["Status"]
        .replace("", "Non renseigné")
        .value_counts()
        .rename_axis("Statut")
        .reset_index(name="Nombre")
    )

    if not analyse_statut.empty:

        st.dataframe(
            analyse_statut,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            analyse_statut.set_index("Statut")
        )


# ============================================================
# ANALYSE CLIENTS
# ============================================================

st.divider()

st.header("👥 Analyse des Clients")


if "Client" in df_analyse.columns:

    analyse_clients = (
        df_analyse["Client"]
        .replace("", "Non renseigné")
        .value_counts()
        .rename_axis("Client")
        .reset_index(name="Nombre OM")
    )

    analyse_clients = analyse_clients.head(20)

    if not analyse_clients.empty:

        st.subheader("🏆 Top 20 des clients par nombre d'OM")

        st.dataframe(
            analyse_clients,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            analyse_clients.set_index("Client")
        )


# ============================================================
# ANALYSE CHAUFFEURS
# ============================================================

st.divider()

st.header("👷 Analyse des Chauffeurs")


if "Chauffeur" in df_analyse.columns:

    analyse_chauffeurs = (
        df_analyse["Chauffeur"]
        .replace("", "Non renseigné")
        .value_counts()
        .rename_axis("Chauffeur")
        .reset_index(name="Nombre OM")
    )

    analyse_chauffeurs = analyse_chauffeurs.head(20)

    if not analyse_chauffeurs.empty:

        st.subheader(
            "🏆 Top 20 des chauffeurs par nombre d'OM"
        )

        st.dataframe(
            analyse_chauffeurs,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            analyse_chauffeurs.set_index("Chauffeur")
        )


# ============================================================
# ANALYSE CAMIONS
# ============================================================

st.divider()

st.header("🚚 Analyse des Camions")


if "Numero Camion" in df_analyse.columns:

    analyse_camions = (
        df_analyse["Numero Camion"]
        .replace("", "Non renseigné")
        .value_counts()
        .rename_axis("Camion")
        .reset_index(name="Nombre OM")
    )

    analyse_camions = analyse_camions.head(20)

    if not analyse_camions.empty:

        st.subheader(
            "🏆 Top 20 des camions par nombre d'OM"
        )

        st.dataframe(
            analyse_camions,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            analyse_camions.set_index("Camion")
        )


# ============================================================
# ANALYSE TONNAGE
# ============================================================

st.divider()

st.header("📦 Analyse du chargement")


if "Tonnage" in df_analyse.columns:

    df_analyse["Tonnage"] = pd.to_numeric(
        df_analyse["Tonnage"],
        errors="coerce"
    )

    tonnage_total = (
        df_analyse["Tonnage"]
        .fillna(0)
        .sum()
    )

    tonnage_moyen = (
        df_analyse["Tonnage"]
        .dropna()
        .mean()
    )

else:

    tonnage_total = 0
    tonnage_moyen = 0


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "⚖️ Tonnage total",
        f"{tonnage_total:,.2f}"
    )


with col2:

    st.metric(
        "⚖️ Tonnage moyen / OM",
        f"{tonnage_moyen:,.2f}"
        if pd.notna(tonnage_moyen)
        else "0"
    )


# ============================================================
# ANALYSE DES LIEUX DE CHARGEMENT
# ============================================================

if "Lieu de Chargement" in df_analyse.columns:

    st.divider()

    st.header("📍 Lieux de chargement")

    analyse_chargement = (
        df_analyse["Lieu de Chargement"]
        .replace("", "Non renseigné")
        .value_counts()
        .rename_axis("Lieu de Chargement")
        .reset_index(name="Nombre OM")
    )

    analyse_chargement = analyse_chargement.head(20)

    if not analyse_chargement.empty:

        st.dataframe(
            analyse_chargement,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            analyse_chargement.set_index(
                "Lieu de Chargement"
            )
        )


# ============================================================
# ANALYSE DES LIEUX DE DÉCHARGEMENT
# ============================================================

if "Lieu de DéChargement" in df_analyse.columns:

    st.divider()

    st.header("📍 Lieux de déchargement")

    analyse_dechargement = (
        df_analyse["Lieu de DéChargement"]
        .replace("", "Non renseigné")
        .value_counts()
        .rename_axis("Lieu de Déchargement")
        .reset_index(name="Nombre OM")
    )

    analyse_dechargement = analyse_dechargement.head(20)

    if not analyse_dechargement.empty:

        st.dataframe(
            analyse_dechargement,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            analyse_dechargement.set_index(
                "Lieu de Déchargement"
            )
        )


# ============================================================
# INFORMATIONS SUR LE FICHIER CHAUFFEURS
# ============================================================

st.divider()

st.header("👷 Données du fichier Chauffeurs")


if not df_chauffeurs.empty:

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "👷 Total chauffeurs",
            len(df_chauffeurs)
        )

    with col2:

        if "Fonction" in df_chauffeurs.columns:

            nombre_fonctions = (
                df_chauffeurs["Fonction"]
                .replace("", pd.NA)
                .nunique()
            )

        else:

            nombre_fonctions = 0

        st.metric(
            "🪪 Fonctions",
            nombre_fonctions
        )

    with col3:

        if "Section/Affectation" in df_chauffeurs.columns:

            nombre_affectations = (
                df_chauffeurs["Section/Affectation"]
                .replace("", pd.NA)
                .nunique()
            )

        else:

            nombre_affectations = 0

        st.metric(
            "📍 Affectations",
            nombre_affectations
        )


else:

    st.warning(
        "⚠️ Le fichier Chauffeurs.xlsx n'est pas disponible."
    )


# ============================================================
# INFORMATIONS SUR LE FICHIER CLIENTS
# ============================================================

st.divider()

st.header("👥 Données du fichier Clients")


if not df_clients.empty:

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "👥 Total clients",
            len(df_clients)
        )

    with col2:

        if "Lieu de chargement" in df_clients.columns:

            nombre_lieux = (
                df_clients["Lieu de chargement"]
                .replace("", pd.NA)
                .nunique()
            )

        else:

            nombre_lieux = 0

        st.metric(
            "📍 Lieux de chargement",
            nombre_lieux
        )

else:

    st.warning(
        "⚠️ Le fichier Clients.xlsx n'est pas disponible."
    )


# ============================================================
# CONCLUSION
# ============================================================

st.divider()

st.header("📌 Résumé de l'activité")


st.info(
    f"""
    **Période analysée :**
    {periode[0] if periode and len(periode) == 2 else "Toutes les dates"}
    → {periode[1] if periode and len(periode) == 2 else "Toutes les dates"}

    **Ordres de Mission analysés :** {nombre_om}

    **Camions utilisés :** {nombre_camions}

    **Chauffeurs concernés :** {nombre_chauffeurs}

    **Clients concernés :** {nombre_clients}

    **Kilométrage total :** {km_total:,.0f} km
    """
)


# ============================================================
# ACTUALISATION
# ============================================================

st.divider()

if st.button(
    "🔄 Actualiser les données",
    key="rapport_actualiser"
):

    st.cache_data.clear()
    st.rerun()
