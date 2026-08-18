
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
FICHIER_CV = DATA_DIR / "CV.xlsx"

FEUILLE_OM = "Input OM fini"


# ============================================================
# COLONNES UTILISÉES
# ============================================================

COLONNE_CAMION_OM = "Numero Camion"
COLONNE_COMMANDE_OM = "N° Commande"
COLONNE_KM = "Kilometrage Parcouru"

COLONNE_COMMANDE_CV = "N° Commande"
COLONNE_MONTANT_CV = "Montant ligne HT"


# ============================================================
# FONCTION DE LECTURE EXCEL
# ============================================================

def lire_excel(fichier, feuille=None):

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

        # Nettoyage des noms de colonnes
        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        # Suppression des lignes complètement vides
        df = df.dropna(how="all")

        # Nettoyage des colonnes texte
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
# CHARGEMENT DES DONNÉES
# ============================================================

df_camions = lire_excel(FICHIER_CAMIONS)

df_om = lire_excel(
    FICHIER_OM,
    FEUILLE_OM
)

df_cv = lire_excel(FICHIER_CV)


# ============================================================
# VÉRIFICATION CAMIONS
# ============================================================

if df_camions.empty:

    st.error(
        f"""
        ❌ Le fichier **Camions.xlsx** est introuvable ou vide.

        Fichier recherché :

        `{FICHIER_CAMIONS}`
        """
    )

    st.stop()


# ============================================================
# VÉRIFICATION OM
# ============================================================

if df_om.empty:

    st.error(
        f"""
        ❌ Le fichier **OM.xlsx** est introuvable, vide,
        ou la feuille **{FEUILLE_OM}** n'existe pas.

        Fichier recherché :

        `{FICHIER_OM}`
        """
    )

    st.stop()


# ============================================================
# VÉRIFICATION DES COLONNES OM
# ============================================================

colonnes_om_manquantes = [
    colonne
    for colonne in [
        COLONNE_CAMION_OM,
        COLONNE_COMMANDE_OM,
        COLONNE_KM
    ]
    if colonne not in df_om.columns
]

if colonnes_om_manquantes:

    st.error(
        "❌ Colonnes manquantes dans OM.xlsx : "
        + ", ".join(colonnes_om_manquantes)
    )

    st.stop()


# ============================================================
# VÉRIFICATION CV
# ============================================================

if df_cv.empty:

    st.warning(
        f"""
        ⚠️ Le fichier **CV.xlsx** est introuvable ou vide.

        Les informations suivantes seront donc calculées :

        ✅ Nombre de missions
        ✅ Kilométrage parcouru

        ❌ Montant ligne HT

        Fichier recherché :

        `{FICHIER_CV}`
        """
    )

    cv_disponible = False

else:

    cv_disponible = True


# ============================================================
# PRÉPARATION OM
# ============================================================

df_om_analyse = df_om.copy()


# ------------------------------------------------------------
# Nettoyage camion
# ------------------------------------------------------------

df_om_analyse[COLONNE_CAMION_OM] = (
    df_om_analyse[COLONNE_CAMION_OM]
    .fillna("")
    .astype(str)
    .str.strip()
)


# ------------------------------------------------------------
# Nettoyage commande
# ------------------------------------------------------------

df_om_analyse[COLONNE_COMMANDE_OM] = (
    df_om_analyse[COLONNE_COMMANDE_OM]
    .fillna("")
    .astype(str)
    .str.strip()
)


# ------------------------------------------------------------
# Conversion kilométrage
# ------------------------------------------------------------

df_om_analyse[COLONNE_KM] = pd.to_numeric(
    df_om_analyse[COLONNE_KM],
    errors="coerce"
).fillna(0)


# ============================================================
# ANALYSE DES MISSIONS PAR CAMION
# ============================================================

analyse_om = (
    df_om_analyse[
        df_om_analyse[COLONNE_CAMION_OM] != ""
    ]
    .groupby(COLONNE_CAMION_OM)
    .agg(
        Nombre_Missions=(
            COLONNE_COMMANDE_OM,
            "count"
        ),
        Kilometrage_Parcouru=(
            COLONNE_KM,
            "sum"
        )
    )
    .reset_index()
)


# ============================================================
# PRÉPARATION COMMANDE DE VENTE
# ============================================================

if cv_disponible:

    if (
        COLONNE_COMMANDE_CV not in df_cv.columns
        or COLONNE_MONTANT_CV not in df_cv.columns
    ):

        st.warning(
            f"""
            ⚠️ Les colonnes nécessaires ne sont pas présentes
            dans CV.xlsx.

            Colonnes recherchées :

            • **{COLONNE_COMMANDE_CV}**
            • **{COLONNE_MONTANT_CV}**

            Le montant sera donc affiché à **0**.
            """
        )

        cv_disponible = False


# ============================================================
# CALCUL DU MONTANT PAR COMMANDE
# ============================================================

if cv_disponible:

    df_cv_analyse = df_cv.copy()

    # Nettoyage numéro commande
    df_cv_analyse[COLONNE_COMMANDE_CV] = (
        df_cv_analyse[COLONNE_COMMANDE_CV]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # Conversion montant
    df_cv_analyse[COLONNE_MONTANT_CV] = (
        df_cv_analyse[COLONNE_MONTANT_CV]
        .astype(str)
        .str.replace(
            "\u00a0",
            "",
            regex=False
        )
        .str.replace(
            " ",
            "",
            regex=False
        )
        .str.replace(
            ",",
            ".",
            regex=False
        )
    )

    df_cv_analyse[COLONNE_MONTANT_CV] = pd.to_numeric(
        df_cv_analyse[COLONNE_MONTANT_CV],
        errors="coerce"
    ).fillna(0)

    # --------------------------------------------------------
    # Total CV par commande
    # --------------------------------------------------------

    montant_par_commande = (
        df_cv_analyse[
            df_cv_analyse[COLONNE_COMMANDE_CV] != ""
        ]
        .groupby(COLONNE_COMMANDE_CV)[
            COLONNE_MONTANT_CV
        ]
        .sum()
        .reset_index()
    )

    # --------------------------------------------------------
    # Renommage pour liaison
    # --------------------------------------------------------

    montant_par_commande = montant_par_commande.rename(
        columns={
            COLONNE_COMMANDE_CV: COLONNE_COMMANDE_OM,
            COLONNE_MONTANT_CV: "Montant_Ligne_HT"
        }
    )

    # --------------------------------------------------------
    # Liaison OM → CV
    # --------------------------------------------------------

    df_om_analyse = df_om_analyse.merge(
        montant_par_commande,
        on=COLONNE_COMMANDE_OM,
        how="left"
    )

    df_om_analyse["Montant_Ligne_HT"] = (
        pd.to_numeric(
            df_om_analyse["Montant_Ligne_HT"],
            errors="coerce"
        )
        .fillna(0)
    )

    # --------------------------------------------------------
    # Total montant par camion
    # --------------------------------------------------------

    analyse_montant = (
        df_om_analyse[
            df_om_analyse[COLONNE_CAMION_OM] != ""
        ]
        .groupby(COLONNE_CAMION_OM)[
            "Montant_Ligne_HT"
        ]
        .sum()
        .reset_index()
    )

else:

    analyse_montant = pd.DataFrame(
        columns=[
            COLONNE_CAMION_OM,
            "Montant_Ligne_HT"
        ]
    )


# ============================================================
# FUSION ANALYSE
# ============================================================

analyse = analyse_om.merge(
    analyse_montant,
    on=COLONNE_CAMION_OM,
    how="left"
)


analyse["Montant_Ligne_HT"] = (
    pd.to_numeric(
        analyse["Montant_Ligne_HT"],
        errors="coerce"
    )
    .fillna(0)
)


# ============================================================
# LIAISON AVEC CAMIONS.XLSX
# ============================================================

# Recherche automatique de la colonne camion
colonne_camion = None

possibilites_camion = [
    "Numero Camion",
    "Numéro Camion",
    "Camion",
    "Matricule",
    "Matricule Camion",
    "N° Camion"
]

for colonne in possibilites_camion:

    if colonne in df_camions.columns:

        colonne_camion = colonne
        break


if colonne_camion:

    df_camions[colonne_camion] = (
        df_camions[colonne_camion]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    analyse = analyse.rename(
        columns={
            COLONNE_CAMION_OM: colonne_camion
        }
    )

    df_resultat = df_camions.merge(
        analyse,
        on=colonne_camion,
        how="left"
    )

else:

    st.warning(
        """
        ⚠️ La colonne permettant d'identifier le camion
        n'a pas été trouvée dans Camions.xlsx.

        L'analyse des missions est néanmoins disponible.
        """
    )

    df_resultat = analyse.copy()


# ============================================================
# REMPLACEMENT DES VALEURS VIDES
# ============================================================

for colonne in [
    "Nombre_Missions",
    "Kilometrage_Parcouru",
    "Montant_Ligne_HT"
]:

    if colonne in df_resultat.columns:

        df_resultat[colonne] = (
            pd.to_numeric(
                df_resultat[colonne],
                errors="coerce"
            )
            .fillna(0)
        )


# ============================================================
# TITRE
# ============================================================

st.title("🚚 Gestion des Camions")

st.subheader(
    "Parc automobile et analyse de l'activité - TMF LOGISTICS"
)


st.divider()


# ============================================================
# STATISTIQUES GÉNÉRALES
# ============================================================

total_camions = len(df_camions)

total_missions = int(
    df_resultat["Nombre_Missions"].sum()
)

total_km = float(
    df_resultat["Kilometrage_Parcouru"].sum()
)

total_montant = float(
    df_resultat["Montant_Ligne_HT"].sum()
)


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
        "🛣️ Kilométrage",
        f"{total_km:,.0f} km".replace(",", " ")
    )


with col4:

    st.metric(
        "💰 Montant HT",
        f"{total_montant:,.2f}".replace(",", " ")
    )


# ============================================================
# RECHERCHE
# ============================================================

st.divider()

st.subheader("🔎 Recherche")

recherche = st.text_input(
    "Rechercher un camion",
    placeholder=(
        "Camion, matricule, chauffeur, client, "
        "statut..."
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

    df_filtre = df_filtre[masque]


# ============================================================
# TABLEAU ANALYTIQUE
# ============================================================

st.divider()

st.subheader(
    f"🚚 Analyse par camion ({len(df_filtre)})"
)


# ============================================================
# COLONNES D'AFFICHAGE
# ============================================================

colonnes_analyse = []

for colonne in df_resultat.columns:

    if colonne not in [
        "Nombre_Missions",
        "Kilometrage_Parcouru",
        "Montant_Ligne_HT"
    ]:

        colonnes_analyse.append(colonne)


colonnes_analyse += [
    "Nombre_Missions",
    "Kilometrage_Parcouru",
    "Montant_Ligne_HT"
]


colonnes_analyse = [
    colonne
    for colonne in colonnes_analyse
    if colonne in df_filtre.columns
]


df_affichage = df_filtre[
    colonnes_analyse
].copy()


# ============================================================
# RENOMMAGE
# ============================================================

df_affichage = df_affichage.rename(
    columns={
        "Nombre_Missions": "Nombre de Missions",
        "Kilometrage_Parcouru": "Kilométrage Parcouru",
        "Montant_Ligne_HT": "Montant Parc HT"
    }
)


# ============================================================
# AFFICHAGE FORMATÉ
# ============================================================

if "Kilométrage Parcouru" in df_affichage.columns:

    df_affichage[
        "Kilométrage Parcouru"
    ] = df_affichage[
        "Kilométrage Parcouru"
    ].round(0)


if "Montant Parc HT" in df_affichage.columns:

    df_affichage[
        "Montant Parc HT"
    ] = df_affichage[
        "Montant Parc HT"
    ].round(2)


st.dataframe(
    df_affichage,
    use_container_width=True,
    hide_index=True,
    height=600
)


# ============================================================
# CLASSEMENT DES CAMIONS
# ============================================================

st.divider()

st.subheader(
    "🏆 Classement des camions"
)


classement = df_resultat.copy()


# ------------------------------------------------------------
# TOP MISSIONS
# ------------------------------------------------------------

st.markdown("### 📋 Plus grand nombre de missions")

top_missions = (
    classement
    .sort_values(
        "Nombre_Missions",
        ascending=False
    )
    .head(10)
)


if colonne_camion and colonne_camion in top_missions.columns:

    st.dataframe(
        top_missions[
            [
                colonne_camion,
                "Nombre_Missions"
            ]
        ].rename(
            columns={
                colonne_camion: "Camion",
                "Nombre_Missions": "Nombre de Missions"
            }
        ),
        use_container_width=True,
        hide_index=True
    )


# ------------------------------------------------------------
# TOP KILOMÉTRAGE
# ------------------------------------------------------------

st.markdown("### 🛣️ Plus grand kilométrage")

top_km = (
    classement
    .sort_values(
        "Kilometrage_Parcouru",
        ascending=False
    )
    .head(10)
)


if colonne_camion and colonne_camion in top_km.columns:

    st.dataframe(
        top_km[
            [
                colonne_camion,
                "Kilometrage_Parcouru"
            ]
        ].rename(
            columns={
                colonne_camion: "Camion",
                "Kilometrage_Parcouru":
                    "Kilométrage Parcouru"
            }
        ),
        use_container_width=True,
        hide_index=True
    )


# ------------------------------------------------------------
# TOP MONTANT
# ------------------------------------------------------------

st.markdown("### 💰 Plus grand montant HT")

top_montant = (
    classement
    .sort_values(
        "Montant_Ligne_HT",
        ascending=False
    )
    .head(10)
)


if colonne_camion and colonne_camion in top_montant.columns:

    st.dataframe(
        top_montant[
            [
                colonne_camion,
                "Montant_Ligne_HT"
            ]
        ].rename(
            columns={
                colonne_camion: "Camion",
                "Montant_Ligne_HT":
                    "Montant Parc HT"
            }
        ),
        use_container_width=True,
        hide_index=True
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
```
