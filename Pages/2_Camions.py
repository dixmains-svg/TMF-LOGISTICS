import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TMF LOGISTICS - Camions",
    page_icon="🚚",
    layout="wide"
)


# ============================================================
# DÉTERMINATION DU DOSSIER RACINE
# ============================================================

CURRENT_DIR = Path(__file__).resolve().parent


def trouver_racine_projet():

    # Cas normal :
    # /tmf-logistics/Pages/2_Camions.py
    if (CURRENT_DIR.parent / "Data").exists():
        return CURRENT_DIR.parent

    # Recherche dans les parents
    for parent in CURRENT_DIR.parents:

        if (parent / "Data").exists():
            return parent

    # Dernier recours
    return CURRENT_DIR.parent


BASE_DIR = trouver_racine_projet()

DATA_DIR = BASE_DIR / "Data"


# ============================================================
# FICHIERS
# ============================================================

FICHIER_CAMIONS = DATA_DIR / "Camions.xlsx"
FICHIER_OM = DATA_DIR / "OM.xlsx"


# ============================================================
# TITRE
# ============================================================

st.title("🚚 Gestion des Camions")

st.subheader(
    "Parc automobile - TMF LOGISTICS"
)


# ============================================================
# INFORMATIONS FICHIERS
# ============================================================

with st.expander("📁 Informations sur les fichiers"):

    st.write(
        f"**Dossier du projet :** `{BASE_DIR}`"
    )

    st.write(
        f"**Dossier Data :** `{DATA_DIR}`"
    )

    st.write(
        f"**Fichier Camions :** `{FICHIER_CAMIONS}`"
    )

    if FICHIER_CAMIONS.exists():

        st.success(
            "✅ Camions.xlsx trouvé"
        )

    else:

        st.error(
            "❌ Camions.xlsx introuvable"
        )

        st.stop()


# ============================================================
# LECTURE CAMIONS
# ============================================================

@st.cache_data
def charger_camions():

    try:

        df = pd.read_excel(
            FICHIER_CAMIONS,
            engine="openpyxl"
        )

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        df = df.dropna(
            how="all"
        )

        # Nettoyage des données texte
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
            f"❌ Erreur lors de la lecture de Camions.xlsx : {e}"
        )

        return pd.DataFrame()


# ============================================================
# CHARGEMENT
# ============================================================

df_camions = charger_camions()


if df_camions.empty:

    st.error(
        "❌ Le fichier Camions.xlsx est vide."
    )

    st.stop()


# ============================================================
# LECTURE ORDRES DE MISSION
# ============================================================

@st.cache_data
def charger_om():

    if not FICHIER_OM.exists():

        return pd.DataFrame()

    try:

        df = pd.read_excel(
            FICHIER_OM,
            sheet_name="Input OM fini",
            engine="openpyxl"
        )

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        df = df.dropna(
            how="all"
        )

        return df

    except Exception:

        return pd.DataFrame()


df_om = charger_om()


# ============================================================
# NETTOYAGE DES NUMÉROS DE CAMION
# ============================================================

def nettoyer_camion(valeur):

    if pd.isna(valeur):

        return ""

    return str(valeur).strip().upper()


# ============================================================
# STATISTIQUES PAR CAMION
# ============================================================

if not df_om.empty and "Numero Camion" in df_om.columns:

    df_om["CAMION_ANALYSE"] = (
        df_om["Numero Camion"]
        .apply(nettoyer_camion)
    )


    # --------------------------------------------------------
    # NOMBRE DE MISSIONS
    # --------------------------------------------------------

    missions_par_camion = (
        df_om[
            df_om["CAMION_ANALYSE"] != ""
        ]
        .groupby("CAMION_ANALYSE")
        .size()
        .reset_index(
            name="Nombre de Missions"
        )
    )


    # --------------------------------------------------------
    # KILOMÉTRAGE
    # --------------------------------------------------------

    if "Kilometrage Parcouru" in df_om.columns:

        df_om["KM_ANALYSE"] = pd.to_numeric(
            df_om["Kilometrage Parcouru"],
            errors="coerce"
        ).fillna(0)

        km_par_camion = (
            df_om[
                df_om["CAMION_ANALYSE"] != ""
            ]
            .groupby("CAMION_ANALYSE")["KM_ANALYSE"]
            .sum()
            .reset_index()
        )

        km_par_camion = km_par_camion.rename(
            columns={
                "KM_ANALYSE": "Kilométrage Parcouru"
            }
        )

    else:

        km_par_camion = pd.DataFrame(
            columns=[
                "CAMION_ANALYSE",
                "Kilométrage Parcouru"
            ]
        )


    # --------------------------------------------------------
    # FUSION
    # --------------------------------------------------------

    statistiques_camions = missions_par_camion.merge(
        km_par_camion,
        on="CAMION_ANALYSE",
        how="outer"
    )

else:

    statistiques_camions = pd.DataFrame(
        columns=[
            "CAMION_ANALYSE",
            "Nombre de Missions",
            "Kilométrage Parcouru"
        ]
    )


# ============================================================
# PRÉPARATION DU TABLEAU CAMIONS
# ============================================================

df_affichage = df_camions.copy()


# ------------------------------------------------------------
# IDENTIFICATION DE LA COLONNE CAMION
# ------------------------------------------------------------

colonne_camion = None

possibles_camion = [
    "Numero Camion",
    "Numéro Camion",
    "N° Camion",
    "Camion",
    "Matricule",
    "Matricule Camion"
]


for colonne in possibles_camion:

    if colonne in df_affichage.columns:

        colonne_camion = colonne

        break


# ============================================================
# AJOUT DES STATISTIQUES
# ============================================================

if colonne_camion is not None:

    df_affichage["CAMION_ANALYSE"] = (
        df_affichage[colonne_camion]
        .apply(nettoyer_camion)
    )

    df_affichage = df_affichage.merge(
        statistiques_camions,
        on="CAMION_ANALYSE",
        how="left"
    )

    df_affichage = df_affichage.drop(
        columns=["CAMION_ANALYSE"],
        errors="ignore"
    )

else:

    df_affichage["Nombre de Missions"] = 0

    df_affichage["Kilométrage Parcouru"] = 0


df_affichage["Nombre de Missions"] = (
    pd.to_numeric(
        df_affichage["Nombre de Missions"],
        errors="coerce"
    )
    .fillna(0)
    .astype(int)
)


df_affichage["Kilométrage Parcouru"] = (
    pd.to_numeric(
        df_affichage["Kilométrage Parcouru"],
        errors="coerce"
    )
    .fillna(0)
)


# ============================================================
# STATISTIQUES GÉNÉRALES
# ============================================================

total_camions = len(df_affichage)

total_missions = int(
    df_affichage["Nombre de Missions"].sum()
)

total_km = float(
    df_affichage["Kilométrage Parcouru"].sum()
)


# ============================================================
# STATUTS
# ============================================================

if "Statut" in df_affichage.columns:

    nombre_operationnels = (
        df_affichage["Statut"]
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(
            [
                "opérationnel",
                "operationnel",
                "disponible",
                "en service"
            ]
        )
        .sum()
    )

else:

    nombre_operationnels = 0


nombre_non_operationnels = (
    total_camions - nombre_operationnels
)


# ============================================================
# INDICATEURS
# ============================================================

st.divider()

col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "🚚 Total Camions",
        total_camions
    )


with col2:

    st.metric(
        "✅ Opérationnels",
        nombre_operationnels
    )


with col3:

    st.metric(
        "⚠️ Non opérationnels",
        nombre_non_operationnels
    )


with col4:

    st.metric(
        "📋 Total Missions",
        total_missions
    )


with col5:

    st.metric(
        "🛣️ Total KM",
        f"{total_km:,.0f}"
    )


# ============================================================
# RECHERCHE
# ============================================================

st.divider()

st.subheader("🔎 Recherche")

recherche = st.text_input(
    "Rechercher un camion",
    placeholder=(
        "Matricule, camion, remorque, chauffeur, "
        "client ou statut..."
    )
)


# ============================================================
# FILTRAGE
# ============================================================

df_filtre = df_affichage.copy()


if recherche:

    masque = (
        df_filtre
        .astype(str)
        .apply(
            lambda colonne:
            colonne.str.contains(
                recherche,
                case=False,
                na=False,
                regex=False
            )
        )
        .any(axis=1)
    )

    df_filtre = df_filtre[
        masque
    ]


# ============================================================
# TABLEAU
# ============================================================

st.divider()

st.subheader(
    f"🚚 Liste des camions ({len(df_filtre)})"
)


# ------------------------------------------------------------
# ORDRE DES COLONNES
# ------------------------------------------------------------

colonnes_prioritaires = []

for colonne in [
    "N°",
    "Numéro",
    "Numero Camion",
    "Numéro Camion",
    "Camion",
    "Remorque",
    "Chauffeur",
    "Statut",
    "Client",
    "Mission",
    "Nombre de Missions",
    "Kilométrage Parcouru"
]:

    if colonne in df_filtre.columns:

        if colonne not in colonnes_prioritaires:

            colonnes_prioritaires.append(
                colonne
            )


autres_colonnes = [
    colonne
    for colonne in df_filtre.columns
    if colonne not in colonnes_prioritaires
]


df_tableau = df_filtre[
    colonnes_prioritaires + autres_colonnes
].copy()


# ============================================================
# AFFICHAGE
# ============================================================

st.dataframe(
    df_tableau,
    use_container_width=True,
    hide_index=True,
    height=600
)


# ============================================================
# DÉTAIL PAR CAMION
# ============================================================

st.divider()

st.subheader(
    "🔍 Analyse détaillée d'un camion"
)


if colonne_camion is not None:

    liste_camions = sorted(
        [
            nettoyer_camion(x)
            for x in df_affichage[
                colonne_camion
            ]
            .dropna()
            .unique()
            if nettoyer_camion(x)
        ]
    )

    if liste_camions:

        camion_selectionne = st.selectbox(
            "🚚 Sélectionner un camion",
            liste_camions,
            key="camion_detail_selection"
        )


        ligne_camion = df_affichage[
            df_affichage[
                colonne_camion
            ]
            .apply(nettoyer_camion)
            == camion_selectionne
        ]


        if not ligne_camion.empty:

            ligne = ligne_camion.iloc[0]


            col1, col2, col3, col4 = st.columns(4)


            with col1:

                st.metric(
                    "🚚 Camion",
                    camion_selectionne
                )


            with col2:

                st.metric(
                    "📋 Missions",
                    int(
                        ligne.get(
                            "Nombre de Missions",
                            0
                        )
                    )
                )


            with col3:

                st.metric(
                    "🛣️ KM Parcourus",
                    f"{float(ligne.get('Kilométrage Parcouru', 0)):,.0f}"
                )


            with col4:

                if "Statut" in ligne.index:

                    st.metric(
                        "📌 Statut",
                        ligne["Statut"]
                    )

                else:

                    st.metric(
                        "📌 Statut",
                        "-"
                    )


# ============================================================
# EXPORT EXCEL
# ============================================================

st.divider()

st.subheader(
    "📥 Export des données"
)


def convertir_excel(df):

    buffer = BytesIO()

    with pd.ExcelWriter(
        buffer,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Camions"
        )

    return buffer.getvalue()


try:

    fichier_excel = convertir_excel(
        df_filtre
    )


    st.download_button(
        label="📥 Télécharger la liste des camions",
        data=fichier_excel,
        file_name="Camions_Analyse.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        key="download_camions_analyse"
    )


except Exception as e:

    st.error(
        f"❌ Impossible de créer le fichier Excel : {e}"
    )


# ============================================================
# ACTUALISATION
# ============================================================

st.divider()

if st.button(
    "🔄 Actualiser les données",
    use_container_width=True,
    key="refresh_camions"
):

    st.cache_data.clear()

    st.rerun()
