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
# LOCALISATION DU PROJET
# ============================================================

CURRENT_DIR = Path(__file__).resolve()


def trouver_fichier(nom_fichier):
    """
    Recherche automatiquement un fichier dans le projet.
    """

    # --------------------------------------------------------
    # 1. Recherche dans les emplacements principaux
    # --------------------------------------------------------

    emplacements = [
        CURRENT_DIR.parent / "Data" / nom_fichier,
        CURRENT_DIR.parent.parent / "Data" / nom_fichier,
        CURRENT_DIR / "Data" / nom_fichier,
    ]

    for fichier in emplacements:

        if fichier.exists():

            return fichier


    # --------------------------------------------------------
    # 2. Recherche récursive dans le projet
    # --------------------------------------------------------

    projet = CURRENT_DIR.parent.parent

    if projet.exists():

        # Recherche exacte
        fichiers = list(
            projet.rglob(nom_fichier)
        )

        if fichiers:

            return fichiers[0]


        # Recherche sans tenir compte des majuscules/minuscules
        nom_recherche = nom_fichier.lower()

        for fichier in projet.rglob("*"):

            if (
                fichier.is_file()
                and fichier.name.lower() == nom_recherche
            ):

                return fichier


    return None


# ============================================================
# RECHERCHE DES FICHIERS
# ============================================================

FICHIER_CAMIONS = trouver_fichier(
    "Camions.xlsx"
)

FICHIER_OM = trouver_fichier(
    "OM.xlsx"
)


# ============================================================
# TITRE
# ============================================================

st.title("🚚 Gestion des Camions")

st.subheader(
    "Parc automobile - TMF LOGISTICS"
)


# ============================================================
# DIAGNOSTIC DES FICHIERS
# ============================================================

with st.expander("📁 Informations et diagnostic des fichiers"):

    st.write(
        "**Fichier Python actuel :**"
    )

    st.code(
        str(CURRENT_DIR)
    )


    st.write(
        "**Racine supposée du projet :**"
    )

    st.code(
        str(CURRENT_DIR.parent.parent)
    )


    st.write(
        "**Fichier Camions.xlsx trouvé :**"
    )

    if FICHIER_CAMIONS:

        st.success(
            str(FICHIER_CAMIONS)
        )

    else:

        st.error(
            "❌ Camions.xlsx NON TROUVÉ"
        )


    st.write(
        "**Fichier OM.xlsx trouvé :**"
    )

    if FICHIER_OM:

        st.success(
            str(FICHIER_OM)
        )

    else:

        st.warning(
            "⚠️ OM.xlsx NON TROUVÉ"
        )


    # --------------------------------------------------------
    # Liste des fichiers Excel trouvés
    # --------------------------------------------------------

    st.write(
        "**Tous les fichiers Excel trouvés dans le projet :**"
    )

    projet = CURRENT_DIR.parent.parent

    fichiers_excel = []

    if projet.exists():

        fichiers_excel = list(
            projet.rglob("*.xlsx")
        )


    if fichiers_excel:

        for fichier in fichiers_excel:

            st.write(
                f"📄 `{fichier}`"
            )

    else:

        st.error(
            "❌ Aucun fichier .xlsx n'a été trouvé."
        )


# ============================================================
# VÉRIFICATION CAMIONS
# ============================================================

if FICHIER_CAMIONS is None:

    st.error(
        """
        ❌ **Le fichier Camions.xlsx est introuvable.**

        Le programme a recherché automatiquement le fichier
        dans le projet.

        Vérifiez que votre dépôt contient bien :

        `Data/Camions.xlsx`

        Si le fichier existe sur votre ordinateur mais pas sur
        GitHub, il faut également l'ajouter au dépôt GitHub.
        """
    )

    st.stop()


# ============================================================
# LECTURE CAMIONS
# ============================================================

def charger_camions():

    try:

        df = pd.read_excel(
            FICHIER_CAMIONS,
            engine="openpyxl"
        )


        # ----------------------------------------------------
        # Nettoyage des noms de colonnes
        # ----------------------------------------------------

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )


        # ----------------------------------------------------
        # Suppression lignes complètement vides
        # ----------------------------------------------------

        df = df.dropna(
            how="all"
        )


        # ----------------------------------------------------
        # Nettoyage des colonnes texte
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


    except Exception as e:

        st.error(
            f"""
            ❌ Erreur lors de la lecture de Camions.xlsx :

            {e}
            """
        )

        return pd.DataFrame()


# ============================================================
# CHARGEMENT CAMIONS
# ============================================================

df_camions = charger_camions()


# ============================================================
# VÉRIFICATION
# ============================================================

if df_camions.empty:

    st.error(
        "❌ Le fichier Camions.xlsx est vide."
    )

    st.stop()


# ============================================================
# LECTURE OM
# ============================================================

def charger_om():

    if FICHIER_OM is None:

        return pd.DataFrame()


    try:

        df = pd.read_excel(
            FICHIER_OM,
            sheet_name="Input OM fini",
            engine="openpyxl"
        )


        # ----------------------------------------------------
        # Nettoyage colonnes
        # ----------------------------------------------------

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )


        # ----------------------------------------------------
        # Suppression lignes vides
        # ----------------------------------------------------

        df = df.dropna(
            how="all"
        )


        return df


    except ValueError:

        st.warning(
            """
            ⚠️ La feuille **Input OM fini** n'existe pas
            dans OM.xlsx.
            """
        )

        return pd.DataFrame()


    except Exception as e:

        st.warning(
            f"""
            ⚠️ Impossible de lire OM.xlsx :

            {e}
            """
        )

        return pd.DataFrame()


# ============================================================
# CHARGEMENT OM
# ============================================================

df_om = charger_om()


# ============================================================
# FONCTION NETTOYAGE CAMION
# ============================================================

def nettoyer_camion(valeur):

    if pd.isna(valeur):

        return ""

    return (
        str(valeur)
        .strip()
        .upper()
    )


# ============================================================
# IDENTIFICATION COLONNE CAMION DANS CAMIONS.XLSX
# ============================================================

colonne_camion = None


colonnes_camion_possibles = [

    "Numero Camion",

    "Numéro Camion",

    "N° Camion",

    "Camion",

    "Matricule",

    "Matricule Camion",

    "N°",

]


for colonne in colonnes_camion_possibles:

    if colonne in df_camions.columns:

        colonne_camion = colonne

        break


# ============================================================
# STATISTIQUES PAR CAMION DEPUIS OM.XLSX
# ============================================================

if (
    not df_om.empty
    and "Numero Camion" in df_om.columns
):

    df_om["CAMION_ANALYSE"] = (
        df_om["Numero Camion"]
        .apply(nettoyer_camion)
    )


    # ========================================================
    # NOMBRE DE MISSIONS
    # ========================================================

    missions_par_camion = (

        df_om[
            df_om["CAMION_ANALYSE"] != ""
        ]

        .groupby(
            "CAMION_ANALYSE"
        )

        .size()

        .reset_index(
            name="Nombre de Missions"
        )
    )


    # ========================================================
    # KILOMÉTRAGE
    # ========================================================

    if "Kilometrage Parcouru" in df_om.columns:

        df_om["KM_ANALYSE"] = pd.to_numeric(
            df_om["Kilometrage Parcouru"],
            errors="coerce"
        ).fillna(0)


        km_par_camion = (

            df_om[
                df_om["CAMION_ANALYSE"] != ""
            ]

            .groupby(
                "CAMION_ANALYSE"
            )["KM_ANALYSE"]

            .sum()

            .reset_index()
        )


        km_par_camion = (
            km_par_camion
            .rename(
                columns={
                    "KM_ANALYSE":
                    "Kilométrage Parcouru"
                }
            )
        )


    else:

        km_par_camion = pd.DataFrame(
            columns=[
                "CAMION_ANALYSE",
                "Kilométrage Parcouru"
            ]
        )


    # ========================================================
    # FUSION MISSIONS + KM
    # ========================================================

    statistiques_camions = (
        missions_par_camion
        .merge(
            km_par_camion,
            on="CAMION_ANALYSE",
            how="outer"
        )
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
# COPIE DU FICHIER CAMIONS
# ============================================================

df_affichage = df_camions.copy()


# ============================================================
# AJOUT DES STATISTIQUES
# ============================================================

if colonne_camion is not None:

    df_affichage["CAMION_ANALYSE"] = (
        df_affichage[
            colonne_camion
        ]
        .apply(nettoyer_camion)
    )


    df_affichage = (
        df_affichage
        .merge(
            statistiques_camions,
            on="CAMION_ANALYSE",
            how="left"
        )
    )


    df_affichage = (
        df_affichage
        .drop(
            columns=[
                "CAMION_ANALYSE"
            ],
            errors="ignore"
        )
    )


else:

    st.warning(
        """
        ⚠️ Impossible d'identifier automatiquement
        la colonne contenant le numéro du camion
        dans Camions.xlsx.
        """
    )


    df_affichage[
        "Nombre de Missions"
    ] = 0


    df_affichage[
        "Kilométrage Parcouru"
    ] = 0


# ============================================================
# NETTOYAGE DES INDICATEURS
# ============================================================

df_affichage[
    "Nombre de Missions"
] = (

    pd.to_numeric(
        df_affichage[
            "Nombre de Missions"
        ],
        errors="coerce"
    )

    .fillna(0)

    .astype(int)
)


df_affichage[
    "Kilométrage Parcouru"
] = (

    pd.to_numeric(
        df_affichage[
            "Kilométrage Parcouru"
        ],
        errors="coerce"
    )

    .fillna(0)
)


# ============================================================
# STATISTIQUES GÉNÉRALES
# ============================================================

total_camions = len(
    df_affichage
)


total_missions = int(
    df_affichage[
        "Nombre de Missions"
    ].sum()
)


total_km = float(
    df_affichage[
        "Kilométrage Parcouru"
    ].sum()
)


# ============================================================
# STATUTS
# ============================================================

if "Statut" in df_affichage.columns:

    nombre_operationnels = (

        df_affichage[
            "Statut"
        ]

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
    total_camions
    - nombre_operationnels
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

st.subheader(
    "🔎 Recherche"
)


recherche = st.text_input(
    "Rechercher un camion",
    placeholder=(
        "Matricule, camion, remorque, "
        "chauffeur, client ou statut..."
    ),
    key="recherche_camions"
)


# ============================================================
# FILTRAGE
# ============================================================

df_filtre = (
    df_affichage
    .copy()
)


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


    df_filtre = (
        df_filtre[
            masque
        ]
    )


# ============================================================
# TABLEAU
# ============================================================

st.divider()

st.subheader(
    f"🚚 Liste des camions ({len(df_filtre)})"
)


# ============================================================
# ORDRE DES COLONNES
# ============================================================

colonnes_prioritaires = []


for colonne in [

    "N°",

    "Numéro",

    "Numero Camion",

    "Numéro Camion",

    "Camion",

    "Matricule",

    "Remorque",

    "Chauffeur",

    "Statut",

    "Client",

    "Mission",

    "Nombre de Missions",

    "Kilométrage Parcouru",

]:

    if (
        colonne in df_filtre.columns
        and colonne not in colonnes_prioritaires
    ):

        colonnes_prioritaires.append(
            colonne
        )


autres_colonnes = [

    colonne

    for colonne in df_filtre.columns

    if colonne not in colonnes_prioritaires

]


df_tableau = df_filtre[
    colonnes_prioritaires
    + autres_colonnes
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
# ANALYSE DÉTAILLÉE
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


        ligne_camion = (

            df_affichage[

                df_affichage[
                    colonne_camion
                ]
                .apply(
                    nettoyer_camion
                )

                == camion_selectionne

            ]

        )


        if not ligne_camion.empty:

            ligne = (
                ligne_camion.iloc[0]
            )


            col1, col2, col3, col4 = (
                st.columns(4)
            )


            with col1:

                st.metric(
                    "🚚 Camion",
                    camion_selectionne
                )


            with col2:

                st.metric(

                    "📋 Nombre de Missions",

                    int(
                        ligne.get(
                            "Nombre de Missions",
                            0
                        )
                    )

                )


            with col3:

                st.metric(

                    "🛣️ Kilométrage Parcouru",

                    f"{float(ligne.get('Kilométrage Parcouru', 0)):,.0f}"

                )


            with col4:

                if "Statut" in ligne.index:

                    st.metric(

                        "📌 Statut",

                        str(
                            ligne[
                                "Statut"
                            ]
                        )

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

    fichier_excel = (
        convertir_excel(
            df_filtre
        )
    )


    st.download_button(

        label=(
            "📥 Télécharger "
            "la liste des camions"
        ),

        data=fichier_excel,

        file_name=(
            "Camions_Analyse.xlsx"
        ),

        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),

        key=(
            "download_camions_analyse"
        )

    )


except Exception as e:

    st.error(
        f"""
        ❌ Impossible de créer
        le fichier Excel :

        {e}
        """
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

    st.rerun()
