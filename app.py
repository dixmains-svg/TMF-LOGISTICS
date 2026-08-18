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
# CHEMINS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "Data"

FICHIER_CAMIONS = DATA_DIR / "Camions.xlsx"
FICHIER_OM = DATA_DIR / "OM.xlsx"


# ============================================================
# RECHERCHE DU FICHIER COMMANDE DE VENTE
# ============================================================

FICHIERS_CV = [
    DATA_DIR / "CV.xlsx",
    DATA_DIR / "Commande_de_Vente.xlsx",
    DATA_DIR / "Commande de Vente.xlsx",
    DATA_DIR / "Commande_Vente.xlsx",
    DATA_DIR / "CommandeVente.xlsx"
]


def trouver_fichier_cv():

    for fichier in FICHIERS_CV:

        if fichier.exists():
            return fichier

    return None


FICHIER_CV = trouver_fichier_cv()


# ============================================================
# TITRE
# ============================================================

st.title("🚚 Gestion des Camions")

st.subheader(
    "Parc automobile - TMF LOGISTICS"
)


# ============================================================
# FONCTION DE LECTURE EXCEL
# ============================================================

def lire_excel(fichier, feuille=None):

    if fichier is None:
        return pd.DataFrame()

    if not fichier.exists():
        return pd.DataFrame()

    try:

        if feuille:

            df = pd.read_excel(
                fichier,
                sheet_name=feuille,
                engine="openpyxl"
            )

        else:

            df = pd.read_excel(
                fichier,
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
        # Suppression lignes totalement vides
        # ----------------------------------------------------

        df = df.dropna(
            how="all"
        )

        # ----------------------------------------------------
        # Nettoyage texte
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
            f"❌ Erreur de lecture de `{fichier.name}` : {e}"
        )

        return pd.DataFrame()


# ============================================================
# FONCTION POUR TROUVER UNE COLONNE
# ============================================================

def trouver_colonne(df, candidats):

    if df.empty:
        return None

    colonnes = {
        str(col).strip().lower(): col
        for col in df.columns
    }

    for candidat in candidats:

        candidat_normalise = (
            candidat
            .strip()
            .lower()
        )

        if candidat_normalise in colonnes:

            return colonnes[candidat_normalise]

    return None


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

df_camions = lire_excel(
    FICHIER_CAMIONS
)

df_om = lire_excel(
    FICHIER_OM,
    feuille="Input OM fini"
)

df_cv = lire_excel(
    FICHIER_CV
)


# ============================================================
# VÉRIFICATION CAMIONS
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
# IDENTIFICATION DES COLONNES CAMIONS
# ============================================================

col_camion = trouver_colonne(
    df_camions,
    [
        "Numero Camion",
        "Numéro Camion",
        "N° Camion",
        "Camion",
        "Matricule",
        "Immatriculation"
    ]
)


if col_camion is None:

    st.error(
        """
        ❌ Impossible de trouver la colonne identifiant le camion
        dans Camions.xlsx.

        Colonnes recherchées :
        Numero Camion, Numéro Camion, N° Camion,
        Camion, Matricule ou Immatriculation.
        """
    )

    st.stop()


# ============================================================
# IDENTIFICATION DES COLONNES OM
# ============================================================

col_om_camion = trouver_colonne(
    df_om,
    [
        "Numero Camion",
        "Numéro Camion",
        "N° Camion",
        "Camion"
    ]
)

col_om_commande = trouver_colonne(
    df_om,
    [
        "N° Commande",
        "No Commande",
        "Numero Commande",
        "Numéro Commande",
        "Commande"
    ]
)

col_om_numero = trouver_colonne(
    df_om,
    [
        "Numéro",
        "N° OM",
        "Numero OM",
        "OM"
    ]
)

col_om_km = trouver_colonne(
    df_om,
    [
        "Kilometrage Parcouru",
        "Kilométrage Parcouru",
        "KM Parcourus",
        "KM Parcouru",
        "Kilometrage parcouru"
    ]
)


# ============================================================
# IDENTIFICATION DES COLONNES CV
# ============================================================

col_cv_commande = trouver_colonne(
    df_cv,
    [
        "N° Commande",
        "No Commande",
        "Numero Commande",
        "Numéro Commande",
        "Commande",
        "N° commande de vente",
        "N° Commande de Vente"
    ]
)

col_cv_montant = trouver_colonne(
    df_cv,
    [
        "Montant ligne HT",
        "Montant Ligne HT",
        "Montant ligne HT ",
        "Montant HT",
        "Montant"
    ]
)


# ============================================================
# INFORMATIONS SUR LES SOURCES
# ============================================================

with st.expander("ℹ️ Informations sur les fichiers utilisés"):

    st.write(
        f"**Camions :** {FICHIER_CAMIONS.name}"
    )

    st.write(
        f"**Ordres de Mission :** {FICHIER_OM.name}"
    )

    if FICHIER_CV:

        st.write(
            f"**Commande de Vente :** {FICHIER_CV.name}"
        )

    else:

        st.warning(
            "⚠️ Aucun fichier Commande de Vente trouvé."
        )

    st.write(
        f"**Colonne camion :** {col_camion}"
    )

    st.write(
        f"**OM - camion :** {col_om_camion}"
    )

    st.write(
        f"**OM - commande :** {col_om_commande}"
    )

    st.write(
        f"**OM - N° OM :** {col_om_numero}"
    )

    st.write(
        f"**OM - KM :** {col_om_km}"
    )

    st.write(
        f"**CV - commande :** {col_cv_commande}"
    )

    st.write(
        f"**CV - Montant ligne HT :** {col_cv_montant}"
    )


# ============================================================
# PRÉPARATION DU PARC CAMIONS
# ============================================================

df_resultat = df_camions.copy()


# ============================================================
# NORMALISATION DU NUMÉRO CAMION
# ============================================================

df_resultat["_CAMION_KEY"] = (
    df_resultat[col_camion]
    .fillna("")
    .astype(str)
    .str.strip()
)


# ============================================================
# INITIALISATION DES INDICATEURS
# ============================================================

df_resultat["Nombre de Missions"] = 0

df_resultat["Kilometrage Parcouru"] = 0.0

df_resultat["Montant Parc Camion HT"] = 0.0


# ============================================================
# ANALYSE DES ORDRES DE MISSION
# ============================================================

if (
    not df_om.empty
    and col_om_camion
):

    df_analyse_om = df_om.copy()

    # --------------------------------------------------------
    # Clé camion
    # --------------------------------------------------------

    df_analyse_om["_CAMION_KEY"] = (
        df_analyse_om[col_om_camion]
        .fillna("")
        .astype(str)
        .str.strip()
    )


    # --------------------------------------------------------
    # KILOMÉTRAGE
    # --------------------------------------------------------

    if col_om_km:

        df_analyse_om["_KM"] = pd.to_numeric(
            df_analyse_om[col_om_km],
            errors="coerce"
        ).fillna(0)

    else:

        df_analyse_om["_KM"] = 0


    # --------------------------------------------------------
    # NOMBRE DE MISSIONS
    # --------------------------------------------------------

    if col_om_numero:

        missions_par_camion = (
            df_analyse_om
            .groupby("_CAMION_KEY")[col_om_numero]
            .nunique()
            .reset_index(name="Nombre de Missions")
        )

    else:

        missions_par_camion = (
            df_analyse_om
            .groupby("_CAMION_KEY")
            .size()
            .reset_index(name="Nombre de Missions")
        )


    # --------------------------------------------------------
    # KM PAR CAMION
    # --------------------------------------------------------

    km_par_camion = (
        df_analyse_om
        .groupby("_CAMION_KEY")["_KM"]
        .sum()
        .reset_index(name="Kilometrage Parcouru")
    )


    # --------------------------------------------------------
    # FUSION MISSIONS
    # --------------------------------------------------------

    df_resultat = df_resultat.merge(
        missions_par_camion,
        on="_CAMION_KEY",
        how="left",
        suffixes=("", "_NEW")
    )


    if "Nombre de Missions_NEW" in df_resultat.columns:

        df_resultat["Nombre de Missions"] = (
            df_resultat["Nombre de Missions_NEW"]
            .fillna(0)
        )

        df_resultat = df_resultat.drop(
            columns=["Nombre de Missions_NEW"]
        )


    # --------------------------------------------------------
    # FUSION KM
    # --------------------------------------------------------

    df_resultat = df_resultat.merge(
        km_par_camion,
        on="_CAMION_KEY",
        how="left",
        suffixes=("", "_NEW")
    )


    if "Kilometrage Parcouru_NEW" in df_resultat.columns:

        df_resultat["Kilometrage Parcouru"] = (
            df_resultat["Kilometrage Parcouru_NEW"]
            .fillna(0)
        )

        df_resultat = df_resultat.drop(
            columns=["Kilometrage Parcouru_NEW"]
        )


# ============================================================
# CALCUL DU MONTANT PAR CAMION
# ============================================================

if (
    not df_om.empty
    and not df_cv.empty
    and col_om_camion
    and col_om_commande
    and col_cv_commande
    and col_cv_montant
):

    # --------------------------------------------------------
    # COPIE OM
    # --------------------------------------------------------

    df_montant = df_om.copy()


    # --------------------------------------------------------
    # CLÉ CAMION
    # --------------------------------------------------------

    df_montant["_CAMION_KEY"] = (
        df_montant[col_om_camion]
        .fillna("")
        .astype(str)
        .str.strip()
    )


    # --------------------------------------------------------
    # CLÉ COMMANDE
    # --------------------------------------------------------

    df_montant["_COMMANDE_KEY"] = (
        df_montant[col_om_commande]
        .fillna("")
        .astype(str)
        .str.strip()
    )


    # --------------------------------------------------------
    # COPIE CV
    # --------------------------------------------------------

    df_commandes = df_cv.copy()


    # --------------------------------------------------------
    # CLÉ COMMANDE CV
    # --------------------------------------------------------

    df_commandes["_COMMANDE_KEY"] = (
        df_commandes[col_cv_commande]
        .fillna("")
        .astype(str)
        .str.strip()
    )


    # --------------------------------------------------------
    # MONTANT LIGNE HT
    # --------------------------------------------------------

    df_commandes["_MONTANT_HT"] = pd.to_numeric(
        df_commandes[col_cv_montant],
        errors="coerce"
    ).fillna(0)


    # --------------------------------------------------------
    # TOTAL CV PAR COMMANDE
    #
    # Si une commande possède plusieurs lignes,
    # les montants ligne HT sont additionnés.
    # --------------------------------------------------------

    montant_par_commande = (
        df_commandes
        .groupby("_COMMANDE_KEY")["_MONTANT_HT"]
        .sum()
        .reset_index()
    )


    # --------------------------------------------------------
    # RAPPROCHEMENT OM / CV
    # --------------------------------------------------------

    df_montant = df_montant.merge(
        montant_par_commande,
        on="_COMMANDE_KEY",
        how="left"
    )


    df_montant["_MONTANT_HT"] = (
        df_montant["_MONTANT_HT"]
        .fillna(0)
    )


    # --------------------------------------------------------
    # ÉVITER DE COMPTER DEUX FOIS LA MÊME COMMANDE
    # POUR UN MÊME CAMION
    # --------------------------------------------------------

    df_montant = (
        df_montant[
            [
                "_CAMION_KEY",
                "_COMMANDE_KEY",
                "_MONTANT_HT"
            ]
        ]
        .drop_duplicates(
            subset=[
                "_CAMION_KEY",
                "_COMMANDE_KEY"
            ]
        )
    )


    # --------------------------------------------------------
    # TOTAL PAR CAMION
    # --------------------------------------------------------

    montant_par_camion = (
        df_montant
        .groupby("_CAMION_KEY")["_MONTANT_HT"]
        .sum()
        .reset_index(
            name="Montant Parc Camion HT"
        )
    )


    # --------------------------------------------------------
    # FUSION AVEC PARC CAMIONS
    # --------------------------------------------------------

    df_resultat = df_resultat.merge(
        montant_par_camion,
        on="_CAMION_KEY",
        how="left",
        suffixes=("", "_NEW")
    )


    if "Montant Parc Camion HT_NEW" in df_resultat.columns:

        df_resultat["Montant Parc Camion HT"] = (
            df_resultat["Montant Parc Camion HT_NEW"]
            .fillna(0)
        )

        df_resultat = df_resultat.drop(
            columns=["Montant Parc Camion HT_NEW"]
        )


# ============================================================
# NETTOYAGE DES INDICATEURS
# ============================================================

df_resultat["Nombre de Missions"] = pd.to_numeric(
    df_resultat["Nombre de Missions"],
    errors="coerce"
).fillna(0).astype(int)


df_resultat["Kilometrage Parcouru"] = pd.to_numeric(
    df_resultat["Kilometrage Parcouru"],
    errors="coerce"
).fillna(0)


df_resultat["Montant Parc Camion HT"] = pd.to_numeric(
    df_resultat["Montant Parc Camion HT"],
    errors="coerce"
).fillna(0)


# ============================================================
# SUPPRESSION COLONNE TECHNIQUE
# ============================================================

if "_CAMION_KEY" in df_resultat.columns:

    df_resultat = df_resultat.drop(
        columns=["_CAMION_KEY"]
    )


# ============================================================
# STATISTIQUES GLOBALES
# ============================================================

total_camions = len(df_resultat)

total_missions = int(
    df_resultat["Nombre de Missions"].sum()
)

total_km = float(
    df_resultat["Kilometrage Parcouru"].sum()
)

total_montant = float(
    df_resultat["Montant Parc Camion HT"].sum()
)


# ============================================================
# KPI
# ============================================================

st.divider()

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🚚 Total Camions",
        total_camions
    )


with col2:

    st.metric(
        "📋 Total Missions",
        f"{total_missions:,}".replace(",", " ")
    )


with col3:

    st.metric(
        "🛣️ Kilométrage Total",
        f"{total_km:,.0f} km".replace(",", " ")
    )


with col4:

    st.metric(
        "💰 Montant Parc HT",
        f"{total_montant:,.2f} DA".replace(",", " ")
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

df_filtre = df_resultat.copy()


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
# STATISTIQUES FILTRÉES
# ============================================================

st.divider()

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🚚 Camions",
        len(df_filtre)
    )


with col2:

    st.metric(
        "📋 Missions",
        int(
            df_filtre[
                "Nombre de Missions"
            ].sum()
        )
    )


with col3:

    st.metric(
        "🛣️ KM Parcourus",
        f"{df_filtre['Kilometrage Parcouru'].sum():,.0f} km"
        .replace(",", " ")
    )


with col4:

    st.metric(
        "💰 Montant HT",
        f"{df_filtre['Montant Parc Camion HT'].sum():,.2f} DA"
        .replace(",", " ")
    )


# ============================================================
# TABLEAU PAR CAMION
# ============================================================

st.divider()

st.subheader(
    f"🚚 Analyse par camion ({len(df_filtre)})"
)


# ============================================================
# COLONNES À AFFICHER
# ============================================================

colonnes_indicateurs = [
    col_camion,
    "Nombre de Missions",
    "Kilometrage Parcouru",
    "Montant Parc Camion HT"
]


# Ajouter certaines colonnes existantes du fichier Camions

colonnes_supplementaires = [
    "Remorque",
    "Chauffeur",
    "Statut",
    "Client",
    "Mission",
    "Affectation"
]


for colonne in colonnes_supplementaires:

    if (
        colonne in df_filtre.columns
        and colonne not in colonnes_indicateurs
    ):

        colonnes_indicateurs.append(
            colonne
        )


colonnes_affichage = [
    colonne
    for colonne in colonnes_indicateurs
    if colonne in df_filtre.columns
]


df_affichage = df_filtre[
    colonnes_affichage
].copy()


# ============================================================
# FORMATAGE
# ============================================================

if "Kilometrage Parcouru" in df_affichage.columns:

    df_affichage[
        "Kilometrage Parcouru"
    ] = (
        pd.to_numeric(
            df_affichage[
                "Kilometrage Parcouru"
            ],
            errors="coerce"
        )
        .fillna(0)
        .round(0)
    )


if "Montant Parc Camion HT" in df_affichage.columns:

    df_affichage[
        "Montant Parc Camion HT"
    ] = (
        pd.to_numeric(
            df_affichage[
                "Montant Parc Camion HT"
            ],
            errors="coerce"
        )
        .fillna(0)
        .round(2)
    )


# ============================================================
# AFFICHAGE
# ============================================================

st.dataframe(
    df_affichage,
    use_container_width=True,
    hide_index=True,
    height=600
)


# ============================================================
# EXPORT EXCEL
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
            sheet_name="Analyse Camions"
        )

    return buffer.getvalue()


try:

    fichier_excel = convertir_excel(
        df_affichage
    )

    st.download_button(
        label="📥 Télécharger l'analyse des camions",
        data=fichier_excel,
        file_name="Analyse_Camions.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        use_container_width=True
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
    use_container_width=True
):

    st.rerun()
