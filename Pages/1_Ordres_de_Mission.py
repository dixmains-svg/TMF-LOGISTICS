import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO
import time


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TMF LOGISTICS - Ordres de Mission",
    page_icon="📋",
    layout="wide"
)


# ============================================================
# CHEMIN DU FICHIER
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

FICHIER_OM = BASE_DIR / "Data" / "OM.xlsx"

FEUILLE_OM = "Input OM fini"


# ============================================================
# FONCTION DE LECTURE EXCEL
# IMPORTANT : PAS DE CACHE
# ============================================================

def charger_om():

    if not FICHIER_OM.exists():

        st.error(
            f"""
            ❌ Le fichier OM.xlsx est introuvable.

            Chemin recherché :

            `{FICHIER_OM}`
            """
        )

        return pd.DataFrame()

    try:

        # Lire directement le fichier Excel
        df = pd.read_excel(
            FICHIER_OM,
            sheet_name=FEUILLE_OM,
            engine="openpyxl"
        )

        # Nettoyage des noms de colonnes
        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        # Nettoyage des données
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
            f"""
            ❌ Erreur lors de la lecture de OM.xlsx :

            `{e}`
            """
        )

        return pd.DataFrame()


# ============================================================
# DATE DE MODIFICATION DU FICHIER
# ============================================================

if FICHIER_OM.exists():

    date_modification = FICHIER_OM.stat().st_mtime

    date_modification_lisible = time.strftime(
        "%d/%m/%Y %H:%M:%S",
        time.localtime(date_modification)
    )

else:

    date_modification_lisible = "Fichier introuvable"


# ============================================================
# CHARGEMENT
# ============================================================

df_om = charger_om()


# ============================================================
# VÉRIFICATION
# ============================================================

if df_om.empty:

    st.error(
        f"""
        ❌ Aucun Ordre de Mission trouvé.

        Fichier :

        `{FICHIER_OM}`

        Feuille :

        `{FEUILLE_OM}`
        """
    )

    st.stop()


# ============================================================
# TITRE
# ============================================================

st.title("📋 Ordres de Mission")

st.subheader(
    "Gestion des Ordres de Mission - TMF LOGISTICS"
)


# ============================================================
# INFORMATION FICHIER
# ============================================================

st.caption(
    f"📂 Fichier utilisé : {FICHIER_OM}"
)

st.caption(
    f"🕐 Dernière modification du fichier : "
    f"{date_modification_lisible}"
)


# ============================================================
# BOUTON ACTUALISER
# ============================================================

if st.button(
    "🔄 Actualiser les données",
    type="primary"
):

    # Effacer tous les caches éventuels
    st.cache_data.clear()
    st.cache_resource.clear()

    # Recharger la page
    st.rerun()


st.divider()


# ============================================================
# STATISTIQUES
# ============================================================

nombre_om = len(df_om)


if "Status" in df_om.columns:

    nombre_statuts = (
        df_om["Status"]
        .replace("", pd.NA)
        .nunique()
    )

else:

    nombre_statuts = 0


if "Numero Camion" in df_om.columns:

    nombre_camions = (
        df_om["Numero Camion"]
        .replace("", pd.NA)
        .nunique()
    )

else:

    nombre_camions = 0


if "Chauffeur" in df_om.columns:

    nombre_chauffeurs = (
        df_om["Chauffeur"]
        .replace("", pd.NA)
        .nunique()
    )

else:

    nombre_chauffeurs = 0


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "📋 Total OM",
        nombre_om
    )


with col2:

    st.metric(
        "📊 Statuts",
        nombre_statuts
    )


with col3:

    st.metric(
        "🚚 Camions",
        nombre_camions
    )


with col4:

    st.metric(
        "👷 Chauffeurs",
        nombre_chauffeurs
    )


st.divider()


# ============================================================
# RECHERCHE
# ============================================================

st.subheader("🔎 Recherche")

recherche = st.text_input(
    "Rechercher un Ordre de Mission",
    placeholder=(
        "N° OM, commande, camion, chauffeur, client..."
    )
)


# ============================================================
# FILTRES
# ============================================================

col1, col2, col3 = st.columns(3)


# ------------------------------------------------------------
# STATUT
# ------------------------------------------------------------

with col1:

    if "Status" in df_om.columns:

        statuts = sorted(
            [
                str(x)
                for x in df_om["Status"]
                .dropna()
                .unique()
                if str(x).strip()
            ]
        )

        filtre_statut = st.multiselect(
            "📊 Statut",
            statuts
        )

    else:

        filtre_statut = []


# ------------------------------------------------------------
# CAMION
# ------------------------------------------------------------

with col2:

    if "Numero Camion" in df_om.columns:

        camions = sorted(
            [
                str(x)
                for x in df_om["Numero Camion"]
                .dropna()
                .unique()
                if str(x).strip()
            ]
        )

        filtre_camion = st.multiselect(
            "🚚 Camion",
            camions
        )

    else:

        filtre_camion = []


# ------------------------------------------------------------
# CLIENT
# ------------------------------------------------------------

with col3:

    if "Client" in df_om.columns:

        clients = sorted(
            [
                str(x)
                for x in df_om["Client"]
                .dropna()
                .unique()
                if str(x).strip()
            ]
        )

        filtre_client = st.multiselect(
            "👥 Client",
            clients
        )

    else:

        filtre_client = []


# ============================================================
# DEUXIÈME LIGNE
# ============================================================

col1, col2, col3 = st.columns(3)


# ------------------------------------------------------------
# CHAUFFEUR
# ------------------------------------------------------------

with col1:

    if "Chauffeur" in df_om.columns:

        chauffeurs = sorted(
            [
                str(x)
                for x in df_om["Chauffeur"]
                .dropna()
                .unique()
                if str(x).strip()
            ]
        )

        filtre_chauffeur = st.multiselect(
            "👷 Chauffeur",
            chauffeurs
        )

    else:

        filtre_chauffeur = []


# ------------------------------------------------------------
# AFFECTATION
# ------------------------------------------------------------

with col2:

    if "Affectation" in df_om.columns:

        affectations = sorted(
            [
                str(x)
                for x in df_om["Affectation"]
                .dropna()
                .unique()
                if str(x).strip()
            ]
        )

        filtre_affectation = st.multiselect(
            "📍 Affectation",
            affectations
        )

    else:

        filtre_affectation = []


# ------------------------------------------------------------
# SECTION
# ------------------------------------------------------------

with col3:

    if "Section" in df_om.columns:

        sections = sorted(
            [
                str(x)
                for x in df_om["Section"]
                .dropna()
                .unique()
                if str(x).strip()
            ]
        )

        filtre_section = st.multiselect(
            "🏢 Section",
            sections
        )

    else:

        filtre_section = []


# ============================================================
# APPLICATION DES FILTRES
# ============================================================

df_filtre = df_om.copy()


# ------------------------------------------------------------
# RECHERCHE
# ------------------------------------------------------------

if recherche:

    masque = (
        df_filtre
        .astype(str)
        .apply(
            lambda colonne:
            colonne.str.contains(
                recherche,
                case=False,
                na=False
            )
        )
        .any(axis=1)
    )

    df_filtre = df_filtre[masque]


# ------------------------------------------------------------
# STATUT
# ------------------------------------------------------------

if filtre_statut:

    df_filtre = df_filtre[
        df_filtre["Status"].isin(filtre_statut)
    ]


# ------------------------------------------------------------
# CAMION
# ------------------------------------------------------------

if filtre_camion:

    df_filtre = df_filtre[
        df_filtre["Numero Camion"].isin(filtre_camion)
    ]


# ------------------------------------------------------------
# CLIENT
# ------------------------------------------------------------

if filtre_client:

    df_filtre = df_filtre[
        df_filtre["Client"].isin(filtre_client)
    ]


# ------------------------------------------------------------
# CHAUFFEUR
# ------------------------------------------------------------

if filtre_chauffeur:

    df_filtre = df_filtre[
        df_filtre["Chauffeur"].isin(filtre_chauffeur)
    ]


# ------------------------------------------------------------
# AFFECTATION
# ------------------------------------------------------------

if filtre_affectation:

    df_filtre = df_filtre[
        df_filtre["Affectation"].isin(filtre_affectation)
    ]


# ------------------------------------------------------------
# SECTION
# ------------------------------------------------------------

if filtre_section:

    df_filtre = df_filtre[
        df_filtre["Section"].isin(filtre_section)
    ]


# ============================================================
# COLONNES À AFFICHER
# ============================================================

COLONNES_OM = [

    "Status",
    "Numéro",
    "N° Commande",
    "Numero Camion",
    "Remorque",
    "Chauffeur",
    "Matricule du Chauffeur",
    "Trajet Réel",
    "Date Depart",
    "Time Depart",
    "Date de Retour",
    "Time Retour",
    "Kilometrage au Depart",
    "Kilometrage au Retour",
    "Kilometrage Parcouru",
    "Date & Heure Dechargement",
    "Date Arrivée Destination",
    "Section",
    "Lieu de Chargement",
    "Lieu de DéChargement",
    "Client",
    "Objet de la Mission",
    "Nom du destinataire",
    "Tonnage",
    "Nature du Chargement",
    "Affectation",
    "Produit_Transporté"
]


colonnes_disponibles = [
    colonne
    for colonne in COLONNES_OM
    if colonne in df_filtre.columns
]


df_affichage = df_filtre[
    colonnes_disponibles
].copy()


# ============================================================
# TABLEAU
# ============================================================

st.divider()

st.subheader(
    f"📋 Liste des Ordres de Mission ({len(df_filtre)})"
)


st.dataframe(
    df_affichage,
    use_container_width=True,
    hide_index=True,
    height=550
)


# ============================================================
# EXPORT
# ============================================================

st.divider()

st.subheader("📥 Export")


def convertir_excel(df):

    buffer = BytesIO()

    with pd.ExcelWriter(
        buffer,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Ordres de Mission"
        )

    return buffer.getvalue()


fichier_excel = convertir_excel(df_filtre)


st.download_button(
    label="📥 Télécharger les OM filtrés",
    data=fichier_excel,
    file_name="Ordres_de_Mission_filtres.xlsx",
    mime=(
        "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet"
    )
)
