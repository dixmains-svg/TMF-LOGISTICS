import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

FICHIER_CLIENTS = BASE_DIR / "Data" / "Clients.xlsx"
# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TMF LOGISTICS - Clients",
    page_icon="👥",
    layout="wide"
)


# ============================================================
# CHEMIN DU FICHIER EXCEL
# ============================================================

# Le fichier 4_Clients.py se trouve dans Pages/
# parent.parent = dossier principal TMF-LOGISTICS

BASE_DIR = Path(__file__).resolve().parent.parent

FICHIER_CLIENTS = BASE_DIR / "Data" / "Clients.xlsx"


# ============================================================
# TITRE
# ============================================================

st.title("👥 Gestion des Clients")

st.subheader(
    "Gestion des clients - TMF LOGISTICS"
)


# ============================================================
# INFORMATIONS SUR LE FICHIER
# ============================================================

with st.expander("📁 Informations sur le fichier Excel"):

    st.write(
        f"**Dossier de l'application :**  \n"
        f"`{BASE_DIR}`"
    )

    st.write(
        f"**Fichier Clients :**  \n"
        f"`{FICHIER_CLIENTS}`"
    )

    if FICHIER_CLIENTS.exists():
        st.success("✅ Le fichier Clients.xlsx existe.")
    else:
        st.error("❌ Le fichier Clients.xlsx est introuvable.")


# ============================================================
# LECTURE DU FICHIER EXCEL
# ============================================================

@st.cache_data
def charger_clients():

    if not FICHIER_CLIENTS.exists():
        return pd.DataFrame()

    try:

        # Lecture Excel
        df = pd.read_excel(
            FICHIER_CLIENTS,
            engine="openpyxl"
        )

        # ----------------------------------------------------
        # NETTOYAGE DES NOMS DE COLONNES
        # ----------------------------------------------------

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        # ----------------------------------------------------
        # NETTOYAGE DES DONNÉES
        # ----------------------------------------------------

        for colonne in df.columns:

            if df[colonne].dtype == "object":

                df[colonne] = (
                    df[colonne]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )

        return df

    except ImportError:

        st.error(
            """
            ❌ Le module **openpyxl** n'est pas installé.

            Ajoutez cette ligne dans `requirements.txt` :

            `openpyxl==3.1.5`

            Puis faites un nouveau déploiement de l'application.
            """
        )

        return pd.DataFrame()

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
# VÉRIFICATION
# ============================================================

if df_clients.empty:

    st.error(
        f"""
        ❌ Le fichier Clients.xlsx est introuvable ou vide.

        **Fichier recherché :**

        `{FICHIER_CLIENTS}`
        """
    )

    st.stop()


# ============================================================
# STATISTIQUES
# ============================================================

total_clients = len(df_clients)


# ------------------------------------------------------------
# NOMBRE DE VILLES
# ------------------------------------------------------------

if "Ville" in df_clients.columns:

    nombre_villes = (
        df_clients["Ville"]
        .replace("", pd.NA)
        .dropna()
        .nunique()
    )

else:

    nombre_villes = 0


# ------------------------------------------------------------
# CLIENTS AVEC REGISTRE DE COMMERCE
# ------------------------------------------------------------

if "Registre de Commerce" in df_clients.columns:

    nombre_rc = (
        df_clients["Registre de Commerce"]
        .replace("", pd.NA)
        .notna()
        .sum()
    )

else:

    nombre_rc = 0


# ------------------------------------------------------------
# CLIENTS AVEC TÉLÉPHONE
# ------------------------------------------------------------

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


# ============================================================
# FILTRE VILLE
# ============================================================

with col1:

    if "Ville" in df_clients.columns:

        villes = sorted(
            [
                str(x).strip()
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


# ============================================================
# FILTRE REGISTRE DE COMMERCE
# ============================================================

with col2:

    if "Registre de Commerce" in df_clients.columns:

        filtre_rc = st.selectbox(
            "📄 Registre de Commerce",
            [
                "Tous",
                "Avec Registre de Commerce",
                "Sans Registre de Commerce"
            ]
        )

    else:

        filtre_rc = "Tous"


# ============================================================
# APPLICATION DES FILTRES
# ============================================================

df_filtre = df_clients.copy()


# ============================================================
# RECHERCHE
# ============================================================

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
# FILTRE VILLE
# ============================================================

if filtre_ville and "Ville" in df_filtre.columns:

    df_filtre = df_filtre[
        df_filtre["Ville"].isin(filtre_ville)
    ]


# ============================================================
# FILTRE REGISTRE DE COMMERCE
# ============================================================

if (
    filtre_rc == "Avec Registre de Commerce"
    and "Registre de Commerce" in df_filtre.columns
):

    df_filtre = df_filtre[
        df_filtre["Registre de Commerce"]
        .fillna("")
        .astype(str)
        .str.strip()
        != ""
    ]


elif (
    filtre_rc == "Sans Registre de Commerce"
    and "Registre de Commerce" in df_filtre.columns
):

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


try:

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

except Exception as e:

    st.error(
        f"❌ Impossible de créer le fichier Excel : {e}"
    )


# ============================================================
# ACTUALISER
# ============================================================

st.divider()

if st.button("🔄 Actualiser les données"):

    st.cache_data.clear()

    st.rerun()
