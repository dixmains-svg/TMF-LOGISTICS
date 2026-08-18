```python
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

# 2_Camions.py se trouve dans /Pages/
# parents[1] = racine du projet TMF-LOGISTICS

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "Data"

FICHIER_CAMIONS = DATA_DIR / "Camions.xlsx"
FICHIER_OM = DATA_DIR / "OM.xlsx"
FICHIER_CV = DATA_DIR / "CV.xlsx"

FEUILLE_OM = "Input OM fini"


# ============================================================
# FONCTION LECTURE EXCEL
# ============================================================

def lire_excel(fichier, sheet_name=None):

    if not fichier.exists():
        return pd.DataFrame()

    try:

        if sheet_name:

            df = pd.read_excel(
                fichier,
                sheet_name=sheet_name,
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

        # Nettoyage des valeurs texte

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
            f"❌ Erreur lors de la lecture de "
            f"`{fichier.name}` : {e}"
        )

        return pd.DataFrame()


# ============================================================
# CHARGEMENT DES FICHIERS
# ============================================================

df_camions = lire_excel(
    FICHIER_CAMIONS
)

df_om = lire_excel(
    FICHIER_OM,
    FEUILLE_OM
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
❌ **Le fichier Camions.xlsx est introuvable ou vide.**

Fichier recherché :

`{FICHIER_CAMIONS}`
"""
    )

    st.stop()


# ============================================================
# FONCTION RECHERCHE COLONNE
# ============================================================

def trouver_colonne(df, noms_possibles):

    if df.empty:
        return None

    colonnes = {
        str(colonne).strip().lower(): colonne
        for colonne in df.columns
    }

    for nom in noms_possibles:

        nom_normalise = (
            str(nom)
            .strip()
            .lower()
        )

        if nom_normalise in colonnes:

            return colonnes[nom_normalise]

    return None


# ============================================================
# IDENTIFICATION COLONNES OM
# ============================================================

COL_CAMION_OM = trouver_colonne(
    df_om,
    [
        "Numero Camion",
        "Numéro Camion",
        "N° Camion",
        "No Camion",
        "Camion",
        "Matricule Camion"
    ]
)


COL_COMMANDE_OM = trouver_colonne(
    df_om,
    [
        "N° Commande",
        "No Commande",
        "Numéro Commande",
        "Numero Commande",
        "Commande"
    ]
)


COL_KM = trouver_colonne(
    df_om,
    [
        "Kilometrage Parcouru",
        "Kilométrage Parcouru",
        "KM Parcourus",
        "Km Parcourus",
        "Kilometrage parcouru"
    ]
)


# ============================================================
# IDENTIFICATION COLONNES CV
# ============================================================

COL_COMMANDE_CV = trouver_colonne(
    df_cv,
    [
        "N° Commande",
        "No Commande",
        "Numéro Commande",
        "Numero Commande",
        "Commande",
        "N° commande",
        "No commande"
    ]
)


COL_MONTANT_CV = trouver_colonne(
    df_cv,
    [
        "Montant ligne HT",
        "Montant Ligne HT",
        "Montant ligne ht",
        "Montant HT",
        "Montant HT Ligne",
        "Montant"
    ]
)


# ============================================================
# TITRE
# ============================================================

st.title(
    "🚚 Gestion des Camions"
)

st.subheader(
    "Parc automobile et analyse des performances par camion - TMF LOGISTICS"
)

st.divider()


# ============================================================
# INFORMATIONS TECHNIQUES
# ============================================================

with st.expander("ℹ️ Informations sur les sources de données"):

    st.write(
        f"📁 **Camions :** `{FICHIER_CAMIONS}`"
    )

    st.write(
        f"📁 **Ordres de Mission :** `{FICHIER_OM}`"
    )

    st.write(
        f"📁 **Commande de Vente :** `{FICHIER_CV}`"
    )

    if COL_CAMION_OM:
        st.success(
            f"✅ Colonne camion OM : **{COL_CAMION_OM}**"
        )
    else:
        st.warning(
            "⚠️ Colonne camion non trouvée dans OM.xlsx."
        )

    if COL_COMMANDE_OM:
        st.success(
            f"✅ Colonne commande OM : **{COL_COMMANDE_OM}**"
        )
    else:
        st.warning(
            "⚠️ Colonne commande non trouvée dans OM.xlsx."
        )

    if COL_KM:
        st.success(
            f"✅ Colonne kilométrage OM : **{COL_KM}**"
        )
    else:
        st.warning(
            "⚠️ Colonne `Kilometrage Parcouru` non trouvée dans OM.xlsx."
        )

    if COL_COMMANDE_CV:
        st.success(
            f"✅ Colonne commande CV : **{COL_COMMANDE_CV}**"
        )
    else:
        st.warning(
            "⚠️ Colonne commande non trouvée dans CV.xlsx."
        )

    if COL_MONTANT_CV:
        st.success(
            f"✅ Colonne montant CV : **{COL_MONTANT_CV}**"
        )
    else:
        st.warning(
            "⚠️ Colonne `Montant ligne HT` non trouvée dans CV.xlsx."
        )


# ============================================================
# PRÉPARATION OM
# ============================================================

df_missions = pd.DataFrame()

if (
    not df_om.empty
    and COL_CAMION_OM
):

    df_missions = df_om.copy()

    # Camion sous forme texte

    df_missions["_CAMION"] = (
        df_missions[COL_CAMION_OM]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # Commande

    if COL_COMMANDE_OM:

        df_missions["_COMMANDE"] = (
            df_missions[COL_COMMANDE_OM]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    else:

        df_missions["_COMMANDE"] = ""

    # Kilométrage

    if COL_KM:

        df_missions["_KM"] = pd.to_numeric(
            df_missions[COL_KM],
            errors="coerce"
        ).fillna(0)

    else:

        df_missions["_KM"] = 0


# ============================================================
# PRÉPARATION CV
# ============================================================

df_ventes = pd.DataFrame()

if (
    not df_cv.empty
    and COL_COMMANDE_CV
    and COL_MONTANT_CV
):

    df_ventes = df_cv.copy()

    df_ventes["_COMMANDE"] = (
        df_ventes[COL_COMMANDE_CV]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # Conversion du montant

    montant = (
        df_ventes[COL_MONTANT_CV]
        .astype(str)
        .str.replace("\u00a0", "", regex=False)
        .str.replace(" ", "", regex=False)
        .str.replace(",", ".", regex=False)
    )

    df_ventes["_MONTANT_HT"] = pd.to_numeric(
        montant,
        errors="coerce"
    ).fillna(0)


# ============================================================
# CALCUL DES STATISTIQUES PAR CAMION
# ============================================================

if not df_missions.empty:

    analyse = (
        df_missions
        .groupby("_CAMION", as_index=False)
        .agg(
            Nombre_Missions=(
                "_COMMANDE",
                "size"
            ),
            Kilometrage_Parcouru=(
                "_KM",
                "sum"
            )
        )
    )

else:

    analyse = pd.DataFrame(
        columns=[
            "_CAMION",
            "Nombre_Missions",
            "Kilometrage_Parcouru"
        ]
    )


# ============================================================
# CALCUL DU MONTANT PAR CAMION
# ============================================================

if (
    not df_missions.empty
    and not df_ventes.empty
):

    # --------------------------------------------------------
    # Pour chaque OM :
    # retrouver le montant de la commande dans CV
    # --------------------------------------------------------

    montants_commande = (
        df_ventes
        .groupby("_COMMANDE", as_index=False)
        ["_MONTANT_HT"]
        .sum()
    )

    df_missions = df_missions.merge(
        montants_commande,
        on="_COMMANDE",
        how="left"
    )

    df_missions["_MONTANT_HT"] = (
        df_missions["_MONTANT_HT"]
        .fillna(0)
    )

    # --------------------------------------------------------
    # Montant par camion
    # --------------------------------------------------------

    montant_camion = (
        df_missions
        .groupby("_CAMION", as_index=False)
        ["_MONTANT_HT"]
        .sum()
        .rename(
            columns={
                "_MONTANT_HT":
                "Montant_Ligne_HT"
            }
        )
    )

    analyse = analyse.merge(
        montant_camion,
        on="_CAMION",
        how="left"
    )

else:

    analyse["Montant_Ligne_HT"] = 0


analyse["Montant_Ligne_HT"] = (
    analyse["Montant_Ligne_HT"]
    .fillna(0)
)

analyse["Kilometrage_Parcouru"] = (
    pd.to_numeric(
        analyse["Kilometrage_Parcouru"],
        errors="coerce"
    )
    .fillna(0)
)


# ============================================================
# AJOUT DES CAMIONS SANS MISSION
# ============================================================

# Chercher la colonne camion dans Camions.xlsx

COL_CAMION_PARCOURS = trouver_colonne(
    df_camions,
    [
        "Numero Camion",
        "Numéro Camion",
        "N° Camion",
        "No Camion",
        "Camion",
        "Matricule",
        "Matricule Camion"
    ]
)


if COL_CAMION_PARCOURS:

    liste_camions = (
        df_camions[COL_CAMION_PARCOURS]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    liste_camions = [
        camion
        for camion in liste_camions
        if camion
    ]

    df_parc = pd.DataFrame(
        {
            "_CAMION": liste_camions
        }
    ).drop_duplicates()

    analyse = df_parc.merge(
        analyse,
        on="_CAMION",
        how="left"
    )

else:

    analyse = analyse.copy()


# ============================================================
# REMPLACEMENT DES VALEURS VIDES
# ============================================================

for colonne in [
    "Nombre_Missions",
    "Kilometrage_Parcouru",
    "Montant_Ligne_HT"
]:

    if colonne not in analyse.columns:

        analyse[colonne] = 0

    analyse[colonne] = (
        pd.to_numeric(
            analyse[colonne],
            errors="coerce"
        )
        .fillna(0)
    )


# ============================================================
# RECHERCHE
# ============================================================

st.subheader("🔎 Recherche")

recherche = st.text_input(
    "Rechercher un camion",
    placeholder=(
        "Matricule, camion, remorque, chauffeur, "
        "client ou statut..."
    ),
    key="recherche_camions"
)


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
                na=False,
                regex=False
            )
        )
        .any(axis=1)
    )

    df_filtre = df_filtre[masque]


# ============================================================
# LISTE DES CAMIONS FILTRÉS
# ============================================================

if COL_CAMION_PARCOURS:

    camions_selectionnes = (
        df_filtre[COL_CAMION_PARCOURS]
        .fillna("")
        .astype(str)
        .str.strip()
        .tolist()
    )

    analyse_filtre = analyse[
        analyse["_CAMION"]
        .isin(camions_selectionnes)
    ].copy()

else:

    analyse_filtre = analyse.copy()


# ============================================================
# STATISTIQUES GÉNÉRALES
# ============================================================

total_camions = len(df_camions)

total_missions = int(
    analyse_filtre["Nombre_Missions"].sum()
)

total_km = float(
    analyse_filtre["Kilometrage_Parcouru"].sum()
)

total_montant = float(
    analyse_filtre["Montant_Ligne_HT"].sum()
)


st.divider()

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🚚 Total Camions",
        total_camions
    )


with col2:

    st.metric(
        "📋 Nombre de Missions",
        f"{total_missions:,}".replace(",", " ")
    )


with col3:

    st.metric(
        "🛣️ Kilométrage",
        f"{total_km:,.0f} km".replace(",", " ")
    )


with col4:

    st.metric(
        "💰 Montant Ligne HT",
        f"{total_montant:,.2f}".replace(",", " ")
    )


# ============================================================
# STATISTIQUES STATUT
# ============================================================

st.divider()

col1, col2, col3, col4 = st.columns(4)


if "Statut" in df_camions.columns:

    statut = (
        df_camions["Statut"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    nombre_operationnels = statut.isin(
        [
            "opérationnel",
            "operationnel",
            "disponible",
            "en service"
        ]
    ).sum()

else:

    nombre_operationnels = 0


nombre_non_operationnels = (
    total_camions - nombre_operationnels
)


with col1:

    st.metric(
        "🚚 Parc",
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
        "📊 Camions analysés",
        len(analyse_filtre)
    )


# ============================================================
# ANALYSE PAR CAMION
# ============================================================

st.divider()

st.subheader(
    "📊 Analyse par camion"
)


tableau_analyse = analyse_filtre.copy()

tableau_analyse = tableau_analyse.rename(
    columns={
        "_CAMION": "Camion",
        "Nombre_Missions": "Nombre de Missions",
        "Kilometrage_Parcouru": "Kilométrage Parcouru",
        "Montant_Ligne_HT": "Montant Ligne HT"
    }
)


colonnes_analyse = [
    "Camion",
    "Nombre de Missions",
    "Kilométrage Parcouru",
    "Montant Ligne HT"
]


tableau_analyse = tableau_analyse[
    [
        colonne
        for colonne in colonnes_analyse
        if colonne in tableau_analyse.columns
    ]
].copy()


# Formatage

tableau_analyse["Kilométrage Parcouru"] = (
    pd.to_numeric(
        tableau_analyse["Kilométrage Parcouru"],
        errors="coerce"
    )
    .fillna(0)
    .round(0)
)


tableau_analyse["Montant Ligne HT"] = (
    pd.to_numeric(
        tableau_analyse["Montant Ligne HT"],
        errors="coerce"
    )
    .fillna(0)
    .round(2)
)


st.dataframe(
    tableau_analyse,
    use_container_width=True,
    hide_index=True,
    height=550,
    column_config={
        "Camion": st.column_config.TextColumn(
            "🚚 Camion"
        ),
        "Nombre de Missions": st.column_config.NumberColumn(
            "📋 Missions",
            format="%d"
        ),
        "Kilométrage Parcouru": st.column_config.NumberColumn(
            "🛣️ Kilométrage",
            format="%.0f km"
        ),
        "Montant Ligne HT": st.column_config.NumberColumn(
            "💰 Montant Ligne HT",
            format="%.2f"
        )
    }
)


# ============================================================
# DÉTAIL DU CAMION
# ============================================================

st.divider()

st.subheader(
    "🔍 Détail d'un camion"
)


liste_camions_analyse = (
    tableau_analyse["Camion"]
    .dropna()
    .astype(str)
    .tolist()
)


if liste_camions_analyse:

    camion_selectionne = st.selectbox(
        "Sélectionner un camion",
        liste_camions_analyse,
        key="camion_detail"
    )

    detail_camion = tableau_analyse[
        tableau_analyse["Camion"].astype(str)
        == str(camion_selectionne)
    ]

    if not detail_camion.empty:

        ligne = detail_camion.iloc[0]

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "📋 Nombre de missions",
                int(
                    ligne["Nombre de Missions"]
                )
            )

        with col2:

            st.metric(
                "🛣️ Kilométrage parcouru",
                f"{ligne['Kilométrage Parcouru']:,.0f} km"
                .replace(",", " ")
            )

        with col3:

            st.metric(
                "💰 Montant Ligne HT",
                f"{ligne['Montant Ligne HT']:,.2f}"
                .replace(",", " ")
            )

        # Informations présentes dans Camions.xlsx

        if COL_CAMION_PARCOURS:

            informations = df_camions[
                df_camions[
                    COL_CAMION_PARCOURS
                ]
                .astype(str)
                .str.strip()
                == str(camion_selectionne)
            ]

            if not informations.empty:

                st.markdown(
                    "### 🚚 Informations du véhicule"
                )

                st.dataframe(
                    informations,
                    use_container_width=True,
                    hide_index=True
                )


# ============================================================
# EXPORT
# ============================================================

st.divider()

st.subheader(
    "📥 Export"
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
            sheet_name="Analyse Camions"
        )

    return buffer.getvalue()


try:

    fichier_excel = convertir_excel(
        tableau_analyse
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
    "🔄 Actualiser les données depuis les fichiers Excel",
    use_container_width=True,
    key="actualiser_camions"
):

    st.rerun()


# ============================================================
# INFORMATION
# ============================================================

st.info(
    """
💡 **Mise à jour des données**

Les données sont relues directement depuis :

- `Camions.xlsx`
- `OM.xlsx`
- `CV.xlsx`

Après avoir enregistré une modification dans vos fichiers Excel,
cliquez sur **🔄 Actualiser les données depuis les fichiers Excel**.
"""
)
```
