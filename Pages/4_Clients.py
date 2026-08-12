import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO


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
# LECTURE DU FICHIER EXCEL
# ============================================================

@st.cache_data
def charger_clients():

    if not FICHIER_CLIENTS.exists():
        return pd.DataFrame()

    try:

        df = pd.read_excel(
            FICHIER_CLIENTS,
            sheet_name="Feuil1",
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
            f"❌ Erreur lors de la lecture de Clients.xlsx : {e}"
        )

        return pd.DataFrame()


# ============================================================
# CHARGEMENT
# ============================================================

df_clients = charger_clients()


# ============================================================
# TITRE
# ============================================================

st.title("👥 Gestion des Clients")

st.subheader(
    "Gestion des clients - TMF LOGISTICS"
)


# ============================================================
# VÉRIFICATION
# ============================================================

if df_clients.empty:

    st.error(
        f"""
        ❌ Le fichier Clients.xlsx est introuvable ou vide.

        Fichier recherché :

        `{FICHIER_CLIENTS}`
        """
    )

    st.stop()


# ============================================================
# STATISTIQUES
# ============================================================

total_clients = len(df_clients)


if "Ville" in df_clients.columns:

    nombre_villes = (
        df_clients["Ville"]
        .replace("", pd.NA)
        .nunique()
    )

else:

    nombre_villes = 0


if "Registre de Commerce" in df_clients.columns:

    nombre_rc = (
        df_clients["Registre de Commerce"]
        .replace("", pd.NA)
        .notna()
        .sum()
    )

else:

    nombre_rc = 0


if "N° téléphone" in df_clients.columns:

    nombre_telephone = (
        df_clients["N° téléphone"]
        .replace("", pd.NA)
        .notna()
        .sum()
    )

else:

    nombre_telephone = 0


# ============================================================
# CARTES STATISTIQUES
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "👥 Total Clients",
        total_clients
    )


with col2:

    st.metric(
        "🏙️ Villes",
        nombre_villes
    )


with col3:

    st.metric(
        "📄 Clients avec RC",
        nombre_rc
    )


with col4:

    st.metric(
        "📞 Clients avec téléphone",
        nombre_telephone
    )


st.divider()


# ============================================================
# RECHERCHE
# ============================================================

st.subheader("🔎 Recherche d'un client")

recherche = st.text_input(
    "Rechercher",
    placeholder=(
        "N°, nom, téléphone, registre de commerce, "
        "identifiant fiscal, adresse ou ville..."
    )
)


# ============================================================
# FILTRES
# ============================================================

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# FILTRE VILLE
# ------------------------------------------------------------

with col1:

    if "Ville" in df_clients.columns:

        villes = sorted(
            [
                str(x)
                for x in df_clients["Ville"]
                .dropna()
                .unique()
                if str(x).strip()
            ]
        )

        filtre_ville = st.multiselect(
            "🏙️ Ville",
            villes
        )

    else:

        filtre_ville = []


# ------------------------------------------------------------
# FILTRE RC
# ------------------------------------------------------------

with col2:

    filtre_rc = st.selectbox(
        "📄 Registre de Commerce",
        [
            "Tous",
            "Avec Registre de Commerce",
            "Sans Registre de Commerce"
        ]
    )


# ============================================================
# APPLICATION DES FILTRES
# ============================================================

df_filtre = df_clients.copy()


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
# VILLE
# ------------------------------------------------------------

if filtre_ville:

    df_filtre = df_filtre[
        df_filtre["Ville"].isin(filtre_ville)
    ]


# ------------------------------------------------------------
# REGISTRE DE COMMERCE
# ------------------------------------------------------------

if filtre_rc == "Avec Registre de Commerce":

    df_filtre = df_filtre[
        df_filtre["Registre de Commerce"]
        .fillna("")
        .astype(str)
        .str.strip()
        != ""
    ]


elif filtre_rc == "Sans Registre de Commerce":

    df_filtre = df_filtre[
        df_filtre["Registre de Commerce"]
        .fillna("")
        .astype(str)
        .str.strip()
        == ""
    ]


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
            sheet_name="Clients"
        )

    return buffer.getvalue()


fichier_excel = convertir_excel(df_filtre)


st.download_button(
    label="📥 Télécharger la liste des clients",
    data=fichier_excel,
    file_name="Clients_filtres.xlsx",
    mime=(
        "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet"
    )
)


# ============================================================
# ACTUALISER
# ============================================================

st.divider()

if st.button("🔄 Actualiser les données"):

    st.cache_data.clear()

    st.rerun()
