import streamlit as st
import pandas as pd
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TMF LOGISTICS - Camions",
    page_icon="🚚",
    layout="wide"
)


# ============================================================
# CHEMIN DU FICHIER
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

FICHIER_CAMIONS = BASE_DIR / "Data" / "Camions.xlsx"


# ============================================================
# LECTURE EXCEL
# ============================================================

@st.cache_data
def charger_camions():

    if not FICHIER_CAMIONS.exists():
        return pd.DataFrame()

    try:

        df = pd.read_excel(
            FICHIER_CAMIONS,
            sheet_name="Camions",
            engine="openpyxl"
        )

        # Nettoyage des noms de colonnes
        df.columns = df.columns.astype(str).str.strip()

        # Nettoyage des cellules texte
        for colonne in df.columns:
            if df[colonne].dtype == "object":
                df[colonne] = df[colonne].fillna("").astype(str).str.strip()

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


# ============================================================
# TITRE
# ============================================================

st.title("🚚 Gestion des Camions")

st.subheader(
    "Parc automobile - TMF LOGISTICS"
)


# ============================================================
# VÉRIFICATION
# ============================================================

if df_camions.empty:

    st.error(
        f"""
        ❌ Le fichier Camions.xlsx est introuvable ou vide.

        Fichier recherché :

        `{FICHIER_CAMIONS}`
        """
    )

    st.stop()


# ============================================================
# STATISTIQUES
# ============================================================

total_camions = len(df_camions)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🚚 Total Camions",
        total_camions
    )


with col2:

    if "Affectation" in df_camions.columns:
        nombre_affectations = df_camions["Affectation"].nunique()
    else:
        nombre_affectations = 0

    st.metric(
        "📍 Affectations",
        nombre_affectations
    )


with col3:

    if "Marque" in df_camions.columns:
        nombre_marques = df_camions["Marque"].nunique()
    else:
        nombre_marques = 0

    st.metric(
        "🏭 Marques",
        nombre_marques
    )


with col4:

    if "Superviseur" in df_camions.columns:
        nombre_superviseurs = df_camions["Superviseur"].nunique()
    else:
        nombre_superviseurs = 0

    st.metric(
        "👤 Superviseurs",
        nombre_superviseurs
    )


st.divider()


# ============================================================
# RECHERCHE
# ============================================================

st.subheader("🔎 Recherche")

recherche = st.text_input(
    "Rechercher un camion",
    placeholder=(
        "N°, immatriculation, section, affectation, "
        "genre, marque ou superviseur..."
    )
)


# ============================================================
# FILTRES
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    if "Section" in df_camions.columns:

        sections = sorted(
            [
                x for x in
                df_camions["Section"].dropna().unique()
                if str(x).strip()
            ]
        )

        section_selection = st.multiselect(
            "📂 Section",
            sections
        )

    else:

        section_selection = []


with col2:

    if "Affectation" in df_camions.columns:

        affectations = sorted(
            [
                x for x in
                df_camions["Affectation"].dropna().unique()
                if str(x).strip()
            ]
        )

        affectation_selection = st.multiselect(
            "📍 Affectation",
            affectations
        )

    else:

        affectation_selection = []


with col3:

    if "Marque" in df_camions.columns:

        marques = sorted(
            [
                x for x in
                df_camions["Marque"].dropna().unique()
                if str(x).strip()
            ]
        )

        marque_selection = st.multiselect(
            "🏭 Marque",
            marques
        )

    else:

        marque_selection = []


# ============================================================
# FILTRAGE
# ============================================================

df_filtre = df_camions.copy()


# Recherche générale

if recherche:

    masque = (
        df_filtre.astype(str)
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


# Section

if section_selection:

    df_filtre = df_filtre[
        df_filtre["Section"].isin(section_selection)
    ]


# Affectation

if affectation_selection:

    df_filtre = df_filtre[
        df_filtre["Affectation"].isin(affectation_selection)
    ]


# Marque

if marque_selection:

    df_filtre = df_filtre[
        df_filtre["Marque"].isin(marque_selection)
    ]


# ============================================================
# RÉSULTAT
# ============================================================

st.divider()

st.subheader(
    f"🚛 Liste des camions ({len(df_filtre)})"
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

st.subheader("📥 Export")


@st.cache_data
def convertir_excel(df):

    from io import BytesIO

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


fichier_excel = convertir_excel(df_filtre)


st.download_button(
    label="📥 Télécharger la liste des camions",
    data=fichier_excel,
    file_name="Camions_filtrés.xlsx",
    mime=(
        "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet"
    )
)
