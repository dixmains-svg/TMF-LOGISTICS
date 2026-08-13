import streamlit as st
import pandas as pd
import numpy as np
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
# CHEMIN DES FICHIERS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "Data"

FICHIER_OM = DATA_DIR / "OM.xlsx"
FICHIER_CAMIONS = DATA_DIR / "Camions.xlsx"
FICHIER_CHAUFFEURS = DATA_DIR / "Chauffeurs.xlsx"
FICHIER_CLIENTS = DATA_DIR / "Clients.xlsx"


# ============================================================
# LECTURE EXCEL
# ============================================================

@st.cache_data
def charger_excel(fichier):

    if not fichier.exists():
        return pd.DataFrame()

    try:

        df = pd.read_excel(
            fichier,
            engine="openpyxl"
        )

        # Nettoyage des colonnes
        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        # Supprimer les lignes complètement vides
        df = df.dropna(how="all")

        # Nettoyage texte
        for colonne in df.columns:

            if df[colonne].dtype == "object":

                df[colonne] = (
                    df[colonne]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )

        return df

    except Exception as e:

        st.error(
            f"❌ Erreur lors de la lecture de "
            f"{fichier.name} : {e}"
        )

        return pd.DataFrame()


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

df_om = charger_excel(FICHIER_OM)

df_camions = charger_excel(FICHIER_CAMIONS)

df_chauffeurs = charger_excel(FICHIER_CHAUFFEURS)

df_clients = charger_excel(FICHIER_CLIENTS)


# ============================================================
# FONCTIONS UTILITAIRES
# ============================================================

def trouver_colonne(df, mots):

    """
    Recherche automatiquement une colonne
    à partir de plusieurs mots-clés.
    """

    if df.empty:
        return None

    colonnes = list(df.columns)

    for mot in mots:

        mot = mot.lower()

        for colonne in colonnes:

            nom = str(colonne).lower()

            if mot in nom:
                return colonne

    return None


def valeurs_uniques(df, colonne):

    if df.empty or colonne is None:
        return []

    valeurs = (
        df[colonne]
        .dropna()
        .astype(str)
        .str.strip()
    )

    valeurs = [
        x for x in valeurs.unique()
        if x and x.lower() not in [
            "nan",
            "none",
            "nat"
        ]
    ]

    return sorted(valeurs)


def taux(partie, total):

    if total == 0:
        return 0

    return round(
        (partie / total) * 100,
        2
    )


# ============================================================
# DÉTECTION DES COLONNES OM
# ============================================================

COL_OM = trouver_colonne(
    df_om,
    [
        "n° om",
        "n om",
        "numéro om",
        "numero om",
        "om"
    ]
)

COL_CAMION = trouver_colonne(
    df_om,
    [
        "camion",
        "immatriculation",
        "matricule"
    ]
)

COL_CHAUFFEUR = trouver_colonne(
    df_om,
    [
        "chauffeur",
        "conducteur"
    ]
)

COL_CLIENT = trouver_colonne(
    df_om,
    [
        "client",
        "customer"
    ]
)

COL_DATE_DEPART = trouver_colonne(
    df_om,
    [
        "date départ",
        "date depart",
        "départ",
        "depart"
    ]
)

COL_DATE_RETOUR = trouver_colonne(
    df_om,
    [
        "date retour",
        "retour"
    ]
)

COL_KM_DEPART = trouver_colonne(
    df_om,
    [
        "km départ",
        "km depart",
        "kilometrage depart",
        "kilométrage départ"
    ]
)

COL_KM_RETOUR = trouver_colonne(
    df_om,
    [
        "km retour",
        "kilometrage retour",
        "kilométrage retour"
    ]
)

COL_KM_PARCOURU = trouver_colonne(
    df_om,
    [
        "km parcourus",
        "kilometrage parcouru",
        "kilométrage parcouru"
    ]
)

COL_STATUT = trouver_colonne(
    df_om,
    [
        "statut",
        "status",
        "état",
        "etat"
    ]
)

COL_MISSION = trouver_colonne(
    df_om,
    [
        "mission",
        "type mission"
    ]
)


# ============================================================
# TITRE
# ============================================================

st.title("📊 Rapports & Analyse")

st.subheader(
    "Analyse de la flotte, des chauffeurs et des clients"
)


st.info(
    "📌 Les analyses sont calculées à partir des "
    "Ordres de Mission et croisées avec les fichiers "
    "Camions, Chauffeurs et Clients."
)


# ============================================================
# VÉRIFICATION
# ============================================================

if df_om.empty:

    st.error(
        f"""
        ❌ Le fichier OM.xlsx est introuvable,
        vide ou impossible à lire.

        Fichier :

        `{FICHIER_OM}`
        """
    )

    st.stop()


# ============================================================
# FILTRES
# ============================================================

st.sidebar.header("🔎 Filtres")


# ------------------------------------------------------------
# FILTRE DATE
# ------------------------------------------------------------

df_analyse = df_om.copy()

if COL_DATE_DEPART:

    df_analyse["_DATE"] = pd.to_datetime(
        df_analyse[COL_DATE_DEPART],
        errors="coerce",
        dayfirst=True
    )

    dates_valides = (
        df_analyse["_DATE"]
        .dropna()
    )

    if not dates_valides.empty:

        date_min = dates_valides.min().date()
        date_max = dates_valides.max().date()

        periode = st.sidebar.date_input(
            "📅 Période",
            value=(date_min, date_max),
            min_value=date_min,
            max_value=date_max
        )

        if isinstance(periode, tuple) and len(periode) == 2:

            debut = pd.Timestamp(periode[0])
            fin = pd.Timestamp(periode[1])

            df_analyse = df_analyse[
                (df_analyse["_DATE"] >= debut)
                &
                (df_analyse["_DATE"] <= fin)
            ]


# ------------------------------------------------------------
# FILTRE CHAUFFEUR
# ------------------------------------------------------------

if COL_CHAUFFEUR:

    chauffeurs = valeurs_uniques(
        df_om,
        COL_CHAUFFEUR
    )

    filtre_chauffeur = st.sidebar.multiselect(
        "👷 Chauffeur",
        chauffeurs
    )

    if filtre_chauffeur:

        df_analyse = df_analyse[
            df_analyse[COL_CHAUFFEUR]
            .astype(str)
            .isin(filtre_chauffeur)
        ]


# ------------------------------------------------------------
# FILTRE CAMION
# ------------------------------------------------------------

if COL_CAMION:

    camions = valeurs_uniques(
        df_om,
        COL_CAMION
    )

    filtre_camion = st.sidebar.multiselect(
        "🚚 Camion",
        camions
    )

    if filtre_camion:

        df_analyse = df_analyse[
            df_analyse[COL_CAMION]
            .astype(str)
            .isin(filtre_camion)
        ]


# ------------------------------------------------------------
# FILTRE CLIENT
# ------------------------------------------------------------

if COL_CLIENT:

    clients = valeurs_uniques(
        df_om,
        COL_CLIENT
    )

    filtre_client = st.sidebar.multiselect(
        "👥 Client",
        clients
    )

    if filtre_client:

        df_analyse = df_analyse[
            df_analyse[COL_CLIENT]
            .astype(str)
            .isin(filtre_client)
        ]


# ============================================================
# KPI GÉNÉRAUX
# ============================================================

st.divider()

st.header("📌 Indicateurs généraux")


total_om = len(df_analyse)

total_camions = (
    df_camions.shape[0]
    if not df_camions.empty
    else 0
)

total_chauffeurs = (
    df_chauffeurs.shape[0]
    if not df_chauffeurs.empty
    else 0
)

total_clients = (
    df_clients.shape[0]
    if not df_clients.empty
    else 0
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "📋 Ordres de Mission",
        total_om
    )


with col2:

    st.metric(
        "🚚 Total Camions",
        total_camions
    )


with col3:

    st.metric(
        "👷 Total Chauffeurs",
        total_chauffeurs
    )


with col4:

    st.metric(
        "👥 Total Clients",
        total_clients
    )


# ============================================================
# ACTIVITÉ FLOTTES
# ============================================================

st.divider()

st.header("🚚 Analyse de la flotte")


if COL_CAMION:

    camions_utilises = (
        df_analyse[COL_CAMION]
        .replace("", np.nan)
        .dropna()
        .astype(str)
        .nunique()
    )

else:

    camions_utilises = 0


camions_non_utilises = max(
    total_camions - camions_utilises,
    0
)


taux_utilisation = taux(
    camions_utilises,
    total_camions
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🚚 Camions utilisés",
        camions_utilises
    )


with col2:

    st.metric(
        "⛔ Camions non utilisés",
        camions_non_utilises
    )


with col3:

    st.metric(
        "📈 Taux d'utilisation flotte",
        f"{taux_utilisation}%"
    )


with col4:

    st.metric(
        "📋 Missions",
        total_om
    )


# ------------------------------------------------------------
# MISSIONS PAR CAMION
# ------------------------------------------------------------

if COL_CAMION:

    st.subheader(
        "📊 Missions par camion"
    )

    analyse_camions = (
        df_analyse
        .groupby(COL_CAMION)
        .size()
        .reset_index(name="Nombre de missions")
        .sort_values(
            "Nombre de missions",
            ascending=False
        )
    )

    st.dataframe(
        analyse_camions,
        use_container_width=True,
        hide_index=True
    )

    if not analyse_camions.empty:

        st.bar_chart(
            analyse_camions.set_index(
                COL_CAMION
            )
        )


# ============================================================
# ANALYSE CHAUFFEURS
# ============================================================

st.divider()

st.header("👷 Analyse des chauffeurs")


if COL_CHAUFFEUR:

    chauffeurs_actifs = (
        df_analyse[COL_CHAUFFEUR]
        .replace("", np.nan)
        .dropna()
        .astype(str)
        .nunique()
    )

else:

    chauffeurs_actifs = 0


chauffeurs_sans_mission = max(
    total_chauffeurs - chauffeurs_actifs,
    0
)


taux_service_chauffeur = taux(
    chauffeurs_actifs,
    total_chauffeurs
)


taux_chomage_chauffeur = taux(
    chauffeurs_sans_mission,
    total_chauffeurs
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "👷 Chauffeurs actifs",
        chauffeurs_actifs
    )


with col2:

    st.metric(
        "⏸️ Chauffeurs sans mission",
        chauffeurs_sans_mission
    )


with col3:

    st.metric(
        "📈 Taux de service chauffeur",
        f"{taux_service_chauffeur}%"
    )


with col4:

    st.metric(
        "📉 Taux de chômage",
        f"{taux_chomage_chauffeur}%"
    )


# ------------------------------------------------------------
# MISSIONS PAR CHAUFFEUR
# ------------------------------------------------------------

if COL_CHAUFFEUR:

    st.subheader(
        "📊 Activité par chauffeur"
    )

    analyse_chauffeurs = (
        df_analyse
        .groupby(COL_CHAUFFEUR)
        .size()
        .reset_index(name="Nombre de missions")
        .sort_values(
            "Nombre de missions",
            ascending=False
        )
    )

    st.dataframe(
        analyse_chauffeurs,
        use_container_width=True,
        hide_index=True
    )

    if not analyse_chauffeurs.empty:

        st.bar_chart(
            analyse_chauffeurs.set_index(
                COL_CHAUFFEUR
            )
        )


# ============================================================
# ANALYSE CLIENTS
# ============================================================

st.divider()

st.header("👥 Analyse des clients")


if COL_CLIENT:

    clients_actifs = (
        df_analyse[COL_CLIENT]
        .replace("", np.nan)
        .dropna()
        .astype(str)
        .nunique()
    )

else:

    clients_actifs = 0


clients_sans_activite = max(
    total_clients - clients_actifs,
    0
)


taux_clients_actifs = taux(
    clients_actifs,
    total_clients
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "👥 Clients actifs",
        clients_actifs
    )


with col2:

    st.metric(
        "⏸️ Clients sans activité",
        clients_sans_activite
    )


with col3:

    st.metric(
        "📈 Taux clients actifs",
        f"{taux_clients_actifs}%"
    )


# ------------------------------------------------------------
# MISSIONS PAR CLIENT
# ------------------------------------------------------------

if COL_CLIENT:

    st.subheader(
        "📊 Activité par client"
    )

    analyse_clients = (
        df_analyse
        .groupby(COL_CLIENT)
        .size()
        .reset_index(name="Nombre de missions")
        .sort_values(
            "Nombre de missions",
            ascending=False
        )
    )

    st.dataframe(
        analyse_clients,
        use_container_width=True,
        hide_index=True
    )

    if not analyse_clients.empty:

        st.bar_chart(
            analyse_clients.set_index(
                COL_CLIENT
            )
        )


# ============================================================
# KILOMÉTRAGE
# ============================================================

st.divider()

st.header("🛣️ Analyse du kilométrage")


kilometrage_total = 0
kilometrage_moyen = 0


if COL_KM_PARCOURU:

    df_analyse["_KM"] = pd.to_numeric(
        df_analyse[COL_KM_PARCOURU],
        errors="coerce"
    )

    kilometrage_total = (
        df_analyse["_KM"]
        .fillna(0)
        .sum()
    )

    kilometrage_moyen = (
        df_analyse["_KM"]
        .mean()
    )


elif COL_KM_DEPART and COL_KM_RETOUR:

    df_analyse["_KM_DEPART"] = pd.to_numeric(
        df_analyse[COL_KM_DEPART],
        errors="coerce"
    )

    df_analyse["_KM_RETOUR"] = pd.to_numeric(
        df_analyse[COL_KM_RETOUR],
        errors="coerce"
    )

    df_analyse["_KM"] = (
        df_analyse["_KM_RETOUR"]
        -
        df_analyse["_KM_DEPART"]
    )

    kilometrage_total = (
        df_analyse["_KM"]
        .fillna(0)
        .sum()
    )

    kilometrage_moyen = (
        df_analyse["_KM"]
        .mean()
    )


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "🛣️ Kilométrage total",
        f"{kilometrage_total:,.0f} km"
    )


with col2:

    st.metric(
        "📏 Kilométrage moyen / mission",
        f"{kilometrage_moyen:,.0f} km"
    )


# ============================================================
# STATUT DES MISSIONS
# ============================================================

if COL_STATUT:

    st.divider()

    st.header("📋 Analyse des statuts")


    analyse_statut = (
        df_analyse[COL_STATUT]
        .replace("", "Non renseigné")
        .value_counts()
        .reset_index()
    )

    analyse_statut.columns = [
        "Statut",
        "Nombre"
    ]

    st.dataframe(
        analyse_statut,
        use_container_width=True,
        hide_index=True
    )

    st.bar_chart(
        analyse_statut.set_index(
            "Statut"
        )
    )


# ============================================================
# RETOUR À VIDE
# ============================================================

st.divider()

st.header("🔄 Taux de retour à vide")


# Recherche d'une colonne pouvant indiquer
# une mission retour / retour à vide.

COL_RETOUR_VIDE = trouver_colonne(
    df_analyse,
    [
        "retour à vide",
        "retour a vide",
        "retour vide",
        "à vide",
        "a vide"
    ]
)


if COL_RETOUR_VIDE:

    valeurs = (
        df_analyse[COL_RETOUR_VIDE]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    retour_vide = valeurs.isin(
        [
            "oui",
            "yes",
            "1",
            "true",
            "vrai",
            "retour à vide",
            "retour a vide"
        ]
    ).sum()

    total_retours = len(df_analyse)

    taux_retour_vide = taux(
        retour_vide,
        total_retours
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "🔄 Retours à vide",
            retour_vide
        )

    with col2:

        st.metric(
            "📈 Taux de retour à vide",
            f"{taux_retour_vide}%"
        )

else:

    st.info(
        """
        ℹ️ Le fichier OM.xlsx ne contient pas de colonne
        permettant d'identifier directement les retours à vide.

        Le taux de retour à vide n'est donc pas calculé
        automatiquement afin de ne pas produire un indicateur
        incorrect.
        """
    )


# ============================================================
# TAUX D'OPTIMISATION CAMION
# ============================================================

st.divider()

st.header("⚙️ Taux d'optimisation camion")


if total_camions > 0 and total_om > 0:

    moyenne_missions_camion = (
        total_om / total_camions
    )

    taux_optimisation = taux(
        camions_utilises,
        total_camions
    )

else:

    moyenne_missions_camion = 0
    taux_optimisation = 0


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "📈 Taux d'optimisation",
        f"{taux_optimisation}%"
    )


with col2:

    st.metric(
        "📊 Moyenne missions / camion",
        f"{moyenne_missions_camion:.2f}"
    )


# ============================================================
# SYNTHÈSE GLOBALE
# ============================================================

st.divider()

st.header("📊 Synthèse globale")


synthese = pd.DataFrame(
    {
        "Indicateur": [
            "Total Ordres de Mission",
            "Total Camions",
            "Camions utilisés",
            "Camions non utilisés",
            "Taux utilisation flotte",
            "Total Chauffeurs",
            "Chauffeurs actifs",
            "Chauffeurs sans mission",
            "Taux service chauffeur",
            "Taux chômage chauffeur",
            "Total Clients",
            "Clients actifs",
            "Clients sans activité",
            "Taux clients actifs",
            "Kilométrage total",
            "Kilométrage moyen / mission",
            "Taux optimisation camion"
        ],

        "Valeur": [
            total_om,
            total_camions,
            camions_utilises,
            camions_non_utilises,
            f"{taux_utilisation}%",

            total_chauffeurs,
            chauffeurs_actifs,
            chauffeurs_sans_mission,
            f"{taux_service_chauffeur}%",
            f"{taux_chomage_chauffeur}%",

            total_clients,
            clients_actifs,
            clients_sans_activite,
            f"{taux_clients_actifs}%",

            f"{kilometrage_total:,.0f} km",
            f"{kilometrage_moyen:,.0f} km",
            f"{taux_optimisation}%"
        ]
    }
)


st.dataframe(
    synthese,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# ACTUALISER
# ============================================================

st.divider()

if st.button(
    "🔄 Actualiser les données",
    use_container_width=True
):

    st.cache_data.clear()

    st.rerun()
