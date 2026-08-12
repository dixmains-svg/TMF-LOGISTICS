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
# CHEMIN DU FICHIER
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

FICHIER_CAMIONS = BASE_DIR / "Data" / "Camions.xlsx"


# ============================================================
# TITRE
# ============================================================

st.title("🚚 Gestion des Camions")

st.subheader(
    "Parc automobile - TMF LOGISTICS"
)


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
            engine="openpyxl"
        )

        # Nettoyage des colonnes
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

    except ImportError:

        st.error(
            """
            ❌ Le module **openpyxl** n'est pas installé.

            Vérifiez votre `requirements.txt` :

            `openpyxl==3.1.5`

            Ensuite faites un nouveau déploiement
            de l'application Streamlit.
            """
        )

        return pd.DataFrame()

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
# VÉRIFICATION
# ============================================================

if df_camions.empty:

    st.error(
        f"""
        ❌ Le fichier Camions.xlsx est introuvable ou vide.

        **Fichier recherché :**

        `{FICHIER_CAMIONS}`
        """
    )

    st.stop()


# ============================================================
# STATISTIQUES
# ============================================================

total_camions = len(df_camions)


# ============================================================
# RECHERCHE
# ============================================================

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

df_filtre = df_camions.copy()


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
# STATISTIQUES
# ============================================================

st.divider()

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🚚 Total Camions",
        total_camions
    )


# ------------------------------------------------------------
# STATUT
# ------------------------------------------------------------

if "Statut" in df_camions.columns:

    nombre_operationnels = (
        df_camions["Statut"]
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


with col2:

    st.metric(
        "✅ Opérationnels",
        nombre_operationnels
    )


# ------------------------------------------------------------
# NON OPÉRATIONNELS
# ------------------------------------------------------------

if "Statut" in df_camions.columns:

    nombre_non_operationnels = (
        total_camions - nombre_operationnels
    )

else:

    nombre_non_operationnels = 0


with col3:

    st.metric(
        "⚠️ Non opérationnels",
        nombre_non_operationnels
    )


with col4:

    st.metric(
        "📋 Résultats",
        len(df_filtre)
    )


# ============================================================
# TABLEAU
# ============================================================

st.divider()

st.subheader(
    f"🚚 Liste des camions ({len(df_filtre)})"
)

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
            sheet_name="Camions"
        )

    return buffer.getvalue()


try:

    fichier_excel = convertir_excel(df_filtre)

    st.download_button(
        label="📥 Télécharger la liste des camions",
        data=fichier_excel,
        file_name="Camions_filtres.xlsx",
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
