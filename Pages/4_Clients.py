import streamlit as st
import pandas as pd
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TMF LOGISTICS - Clients",
    page_icon="👥",
    layout="wide"
)


# ============================================================
# CHEMIN DU FICHIER
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

FICHIER_CLIENTS = BASE_DIR / "Data" / "Clients.xlsx"


# ============================================================
# VÉRIFICATION DU FICHIER
# ============================================================

if not FICHIER_CLIENTS.exists():

    st.error(
        f"""
        ❌ Le fichier Clients.xlsx est introuvable.

        Vérifiez que le fichier se trouve ici :

        `{FICHIER_CLIENTS}`
        """
    )

    st.stop()


# ============================================================
# LECTURE EXCEL
# ============================================================

try:

    import openpyxl

except ImportError:

    st.error(
        """
        ❌ OpenPyXL n'est pas installé.

        Ajoutez cette ligne dans requirements.txt :

        openpyxl>=3.1.5
        """
    )

    st.stop()


try:

    df_clients = pd.read_excel(
        FICHIER_CLIENTS,
        engine="openpyxl"
    )

except Exception as e:

    st.error(
        f"❌ Erreur lors de la lecture de Clients.xlsx : {e}"
    )

    st.stop()


# ============================================================
# VÉRIFICATION DES DONNÉES
# ============================================================

if df_clients.empty:

    st.warning(
        "⚠️ Le fichier Clients.xlsx est vide."
    )

    st.stop()


# ============================================================
# NETTOYAGE DES COLONNES
# ============================================================

df_clients.columns = (
    df_clients.columns
    .astype(str)
    .str.strip()
)


# ============================================================
# NETTOYAGE DES DONNÉES
# ============================================================

for colonne in df_clients.columns:

    if df_clients[colonne].dtype == "object":

        df_clients[colonne] = (
            df_clients[colonne]
            .fillna("")
            .astype(str)
            .str.strip()
        )


# ============================================================
# TITRE
# ============================================================

st.title("👥 Gestion des Clients")

st.subheader(
    "Gestion des clients - TMF LOGISTICS"
)

st.divider()


# ============================================================
# STATISTIQUES
# ============================================================

total_clients = len(df_clients)


# ============================================================
# LIEUX DE CHARGEMENT
# ============================================================

if "Lieu de chargement" in df_clients.columns:

    nombre_lieux_chargement = (
        df_clients["Lieu de chargement"]
        .fillna("")
        .astype(str)
        .str.strip()
        .replace("", pd.NA)
        .notna()
        .sum()
    )

else:

    nombre_lieux_chargement = 0


# ============================================================
# NOMBRE DE LIEUX UNIQUES
# ============================================================

if "Lieu de chargement" in df_clients.columns:

    lieux_uniques = (
        df_clients["Lieu de chargement"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    lieux_uniques = lieux_uniques[
        lieux_uniques != ""
    ]

    nombre_lieux_uniques = lieux_uniques.nunique()

else:

    nombre_lieux_uniques = 0


# ============================================================
# CARTES STATISTIQUES
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "👥 Total Clients",
        total_clients
    )


with col2:

    st.metric(
        "📍 Clients avec lieu",
        nombre_lieux_chargement
    )


with col3:

    st.metric(
        "📍 Lieux de chargement",
        nombre_lieux_uniques
    )


st.divider()


# ============================================================
# RECHERCHE
# ============================================================

st.subheader("🔎 Recherche")

recherche = st.text_input(
    "Rechercher un client",
    placeholder=(
        "Nom, téléphone, ville, RC, "
        "lieu de chargement..."
    )
)


# ============================================================
# FILTRAGE
# ============================================================

df_filtre = df_clients.copy()


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


# ============================================================
# RÉSULTAT
# ============================================================

st.divider()

st.subheader(
    f"👥 Liste des clients ({len(df_filtre)})"
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
# LISTE DES LIEUX DE CHARGEMENT
# ============================================================

if "Lieu de chargement" in df_clients.columns:

    st.divider()

    st.subheader(
        "📍 Lieux de chargement"
    )

    liste_lieux = (
        df_clients["Lieu de chargement"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    liste_lieux = sorted(
        [
            lieu
            for lieu in liste_lieux.unique()
            if lieu != ""
        ]
    )

    if liste_lieux:

        for lieu in liste_lieux:

            st.write(
                f"📍 **{lieu}**"
            )

    else:

        st.info(
            "ℹ️ Aucun lieu de chargement renseigné "
            "dans le fichier Clients.xlsx."
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
