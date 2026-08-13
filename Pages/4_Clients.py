import streamlit as st
import pandas as pd
from pathlib import Path

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

    st.stop()

st.success("✅ Clients.xlsx trouvé.")

# ============================================================
# LECTURE EXCEL
# ============================================================

try:

    import openpyxl

except ImportError:

    st.error(
        """
        ❌ OpenPyXL n'est pas installé.

        Ajoutez dans requirements.txt :

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
# NETTOYAGE
# ============================================================

df_clients.columns = (
    df_clients.columns
    .astype(str)
    .str.strip()
)

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

# ============================================================
# STATISTIQUES
# ============================================================

total_clients = len(df_clients)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "👥 Total Clients",
        total_clients
    )

with col2:

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

    st.metric(
        "📍 Lieux de chargement",
        nombre_lieux_chargement
    )

st.divider()

# ============================================================
# RECHERCHE
# ============================================================

recherche = st.text_input(
    "🔎 Rechercher un client",
    placeholder="Nom, téléphone, ville, RC..."
)

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
# AFFICHAGE
# ============================================================

st.subheader(
    f"👥 Liste des clients ({len(df_filtre)})"
)

st.dataframe(
    df_filtre,
    use_container_width=True,
    hide_index=True
)
