import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TMF LOGISTICS - Chauffeurs",
    page_icon="👷",
    layout="wide"
)


# ============================================================
# CHEMIN DU FICHIER
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

FICHIER_CHAUFFEURS = BASE_DIR / "Data" / "Chauffeurs.xlsx"


# ============================================================
# LECTURE DU FICHIER EXCEL
# ============================================================

@st.cache_data
def charger_chauffeurs():

    if not FICHIER_CHAUFFEURS.exists():
        return pd.DataFrame()

    try:

        df = pd.read_excel(
            FICHIER_CHAUFFEURS,
            sheet_name="Chauffeurs",
            engine="openpyxl"
        )

        # Nettoyage des noms de colonnes
        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
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
            f"❌ Erreur lors de la lecture de Chauffeurs.xlsx : {e}"
        )

        return pd.DataFrame()


# ============================================================
# CHARGEMENT
# ============================================================

df_chauffeurs = charger_chauffeurs()


# ============================================================
# TITRE
# ============================================================

st.title("👷 Gestion des Chauffeurs")

st.subheader(
    "Gestion du personnel roulant - TMF LOGISTICS"
)


# ============================================================
# VÉRIFICATION DU FICHIER
# ============================================================

if df_chauffeurs.empty:

    st.error(
        f"""
        ❌ Le fichier Chauffeurs.xlsx est introuvable ou vide.

        Fichier recherché :

        `{FICHIER_CHAUFFEURS}`
        """
    )

    st.stop()


# ============================================================
# STATISTIQUES
# ============================================================

total_chauffeurs = len(df_chauffeurs)


if "Fonction" in df_chauffeurs.columns:

    nombre_fonctions = (
        df_chauffeurs["Fonction"]
        .replace("", pd.NA)
        .nunique()
    )

else:

    nombre_fonctions = 0


if "Section/Affectation" in df_chauffeurs.columns:

    nombre_affectations = (
        df_chauffeurs["Section/Affectation"]
        .replace("", pd.NA)
        .nunique()
    )

else:

    nombre_affectations = 0


if "Superviseur" in df_chauffeurs.columns:

    nombre_superviseurs = (
        df_chauffeurs["Superviseur"]
        .replace("", pd.NA)
        .nunique()
    )

else:

    nombre_superviseurs = 0


# ============================================================
# CARTES STATISTIQUES
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "👷 Total Chauffeurs",
        total_chauffeurs
    )


with col2:

    st.metric(
        "🪪 Fonctions",
        nombre_fonctions
    )


with col3:

    st.metric(
        "📍 Affectations",
        nombre_affectations
    )


with col4:

    st.metric(
        "👤 Superviseurs",
        nombre_superviseurs
    )


st.divider()


# ============================================================
# RECHERCHE
# ============================================================

st.subheader("🔎 Recherche d'un chauffeur")

recherche = st.text_input(
    "Rechercher",
    placeholder=(
        "Nom, matricule, fonction, affectation ou superviseur..."
    )
)


# ============================================================
# FILTRES
# ============================================================

col1, col2, col3 = st.columns(3)


# ------------------------------------------------------------
# FILTRE FONCTION
# ------------------------------------------------------------

with col1:

    if "Fonction" in df_chauffeurs.columns:

        fonctions = sorted(
            [
                str(x)
                for x in df_chauffeurs["Fonction"]
                .dropna()
                .unique()
                if str(x).strip()
            ]
        )

        filtre_fonction = st.multiselect(
            "🪪 Fonction",
            fonctions
        )

    else:

        filtre_fonction = []


# ------------------------------------------------------------
# FILTRE AFFECTATION
# ------------------------------------------------------------

with col2:

    if "Section/Affectation" in df_chauffeurs.columns:

        affectations = sorted(
            [
                str(x)
                for x in df_chauffeurs["Section/Affectation"]
                .dropna()
                .unique()
                if str(x).strip()
            ]
        )

        filtre_affectation = st.multiselect(
            "📍 Section / Affectation",
            affectations
        )

    else:

        filtre_affectation = []


# ------------------------------------------------------------
# FILTRE SUPERVISEUR
# ------------------------------------------------------------

with col3:

    if "Superviseur" in df_chauffeurs.columns:

        superviseurs = sorted(
            [
                str(x)
                for x in df_chauffeurs["Superviseur"]
                .dropna()
                .unique()
                if str(x).strip()
            ]
        )

        filtre_superviseur = st.multiselect(
            "👤 Superviseur",
            superviseurs
        )

    else:

        filtre_superviseur = []


# ============================================================
# APPLICATION DES FILTRES
# ============================================================

df_filtre = df_chauffeurs.copy()


# ------------------------------------------------------------
# RECHERCHE GÉNÉRALE
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
# FONCTION
# ------------------------------------------------------------

if filtre_fonction:

    df_filtre = df_filtre[
        df_filtre["Fonction"].isin(
            filtre_fonction
        )
    ]


# ------------------------------------------------------------
# AFFECTATION
# ------------------------------------------------------------

if filtre_affectation:

    df_filtre = df_filtre[
        df_filtre["Section/Affectation"].isin(
            filtre_affectation
        )
    ]


# ------------------------------------------------------------
# SUPERVISEUR
# ------------------------------------------------------------

if filtre_superviseur:

    df_filtre = df_filtre[
        df_filtre["Superviseur"].isin(
            filtre_superviseur
        )
    ]


# ============================================================
# RÉSULTAT
# ============================================================

st.divider()

st.subheader(
    f"👷 Liste des chauffeurs ({len(df_filtre)})"
)


# ============================================================
# TABLEAU
# ============================================================

st.dataframe(
    df_filtre,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# EXPORT EXCEL
# ============================================================

st.divider()

st.subheader("📥 Export des données")


def convertir_excel(df):

    buffer = BytesIO()

    with pd.ExcelWriter(
        buffer,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Chauffeurs"
        )

    return buffer.getvalue()


fichier_excel = convertir_excel(df_filtre)


st.download_button(
    label="📥 Télécharger la liste des chauffeurs",
    data=fichier_excel,
    file_name="Chauffeurs_filtrés.xlsx",
    mime=(
        "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet"
    )
)


# ============================================================
# ACTUALISER LES DONNÉES
# ============================================================

st.divider()

if st.button("🔄 Actualiser les données"):

    st.cache_data.clear()

    st.rerun()
