import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Ordres de Mission - TMF LOGISTICS",
    page_icon="📋",
    layout="wide"
)


# ============================================================
# CHEMIN DU FICHIER EXCEL
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

EXCEL_FILE = BASE_DIR / "Data" / "OM.xlsx"

SHEET_NAME = "Input OM fini"


# ============================================================
# FONCTION : CHARGER LES ORDRES DE MISSION
# ============================================================

@st.cache_data
def charger_ordres_mission():

    if not EXCEL_FILE.exists():

        return None

    try:

        df = pd.read_excel(
            EXCEL_FILE,
            sheet_name=SHEET_NAME
        )

        return df

    except Exception as e:

        st.error(
            f"Erreur lors de la lecture du fichier Excel : {e}"
        )

        return None


# ============================================================
# CHARGEMENT
# ============================================================

df_om = charger_ordres_mission()


# ============================================================
# VÉRIFICATION
# ============================================================

if df_om is None:

    st.error(
        "❌ Le fichier Excel des Ordres de Mission est introuvable."
    )

    st.info(
        f"Fichier recherché : {EXCEL_FILE}"
    )

    st.stop()


if df_om.empty:

    st.warning(
        "⚠️ Le fichier Excel ne contient aucun Ordre de Mission."
    )

    st.stop()


# ============================================================
# NETTOYAGE DES NOMS DE COLONNES
# ============================================================

df_om.columns = (
    df_om.columns
    .astype(str)
    .str.strip()
)


# ============================================================
# TITRE
# ============================================================

st.title("📋 Ordres de Mission")

st.subheader(
    "Gestion des Ordres de Mission - TMF LOGISTICS"
)

st.divider()


# ============================================================
# INFORMATIONS
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "📋 Nombre total d'OM",
        len(df_om)
    )


with col2:

    if "Numero Camion" in df_om.columns:

        nombre_camions = (
            df_om["Numero Camion"]
            .dropna()
            .astype(str)
            .nunique()
        )

    else:

        nombre_camions = 0

    st.metric(
        "🚚 Camions",
        nombre_camions
    )


with col3:

    if "Chauffeur" in df_om.columns:

        nombre_chauffeurs = (
            df_om["Chauffeur"]
            .dropna()
            .astype(str)
            .nunique()
        )

    else:

        nombre_chauffeurs = 0

    st.metric(
        "👷 Chauffeurs",
        nombre_chauffeurs
    )


st.divider()


# ============================================================
# RECHERCHE
# ============================================================

st.subheader("🔎 Recherche d'un Ordre de Mission")


recherche = st.text_input(
    "Rechercher par N° OM, commande, camion, remorque, chauffeur ou trajet",
    placeholder="Exemple : 26/OM/34146"
)


# ============================================================
# FILTRAGE
# ============================================================

df_filtre = df_om.copy()


if recherche:

    recherche = recherche.strip()

    masque = (
        df_filtre
        .astype(str)
        .apply(
            lambda colonne: colonne.str.contains(
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
# NOMBRE DE RÉSULTATS
# ============================================================

st.write(
    f"🔎 **{len(df_filtre)}** Ordre(s) de Mission trouvé(s)."
)


# ============================================================
# SÉLECTION DE L'OM
# ============================================================

if df_filtre.empty:

    st.warning(
        "Aucun Ordre de Mission ne correspond à votre recherche."
    )

    st.stop()


# ============================================================
# CRÉATION DE LA LISTE DES OM
# ============================================================

if "Numéro" in df_filtre.columns:

    liste_om = (
        df_filtre["Numéro"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

else:

    liste_om = []


if not liste_om:

    st.warning(
        "La colonne 'Numéro' ne contient aucune donnée."
    )

    st.stop()


# ============================================================
# CHOIX DE L'OM
# ============================================================

numero_om = st.selectbox(
    "📋 Sélectionner un Ordre de Mission",
    liste_om
)


# ============================================================
# RÉCUPÉRER L'OM SÉLECTIONNÉ
# ============================================================

om_selectionne = df_filtre[
    df_filtre["Numéro"]
    .astype(str)
    == str(numero_om)
]


if om_selectionne.empty:

    st.warning(
        "Ordre de Mission introuvable."
    )

    st.stop()


om = om_selectionne.iloc[0]


st.divider()


# ============================================================
# INFORMATIONS GÉNÉRALES
# ============================================================

st.subheader(
    f"📋 Ordre de Mission : {numero_om}"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    if "Status" in om.index:

        st.metric(
            "📌 Statut",
            str(om["Status"])
        )


with col2:

    if "N° Commande" in om.index:

        st.metric(
            "📦 Commande",
            str(om["N° Commande"])
        )


with col3:

    if "Numero Camion" in om.index:

        st.metric(
            "🚚 Camion",
            str(om["Numero Camion"])
        )


with col4:

    if "Remorque" in om.index:

        st.metric(
            "🚛 Remorque",
            str(om["Remorque"])
        )


st.divider()


# ============================================================
# CAMION / CHAUFFEUR
# ============================================================

st.subheader("🚚 Informations Transport")


col1, col2 = st.columns(2)


with col1:

    st.write("### 🚚 Camion")

    if "Numero Camion" in om.index:

        st.write(
            f"**Numéro camion :** {om['Numero Camion']}"
        )

    if "Remorque" in om.index:

        st.write(
            f"**Remorque :** {om['Remorque']}"
        )

    if "Cde Jumelé" in om.index:

        st.write(
            f"**Commande jumelée :** {om['Cde Jumelé']}"
        )


with col2:

    st.write("### 👷 Chauffeur")

    if "Chauffeur" in om.index:

        st.write(
            f"**Chauffeur :** {om['Chauffeur']}"
        )


st.divider()


# ============================================================
# TRAJET
# ============================================================

st.subheader("📍 Informations Trajet")


if "Trajet Réel" in om.index:

    st.info(
        f"🛣️ **Trajet réel :** {om['Trajet Réel']}"
    )


if "Date & Heure Chargement" in om.index:

    st.write(
        f"📦 **Date & Heure Chargement :** "
        f"{om['Date & Heure Chargement']}"
    )


st.divider()


# ============================================================
# DÉPART
# ============================================================

st.subheader("🟢 Départ")


col1, col2, col3 = st.columns(3)


with col1:

    if "Date Depart" in om.index:

        st.write(
            f"📅 **Date départ :** {om['Date Depart']}"
        )


with col2:

    if "Time Depart" in om.index:

        st.write(
            f"🕐 **Heure départ :** {om['Time Depart']}"
        )


with col3:

    if "Kilometrage au Depart" in om.index:

        st.write(
            f"🛣️ **KM départ :** "
            f"{om['Kilometrage au Depart']}"
        )


st.divider()


# ============================================================
# RETOUR
# ============================================================

st.subheader("🔴 Retour")


col1, col2, col3 = st.columns(3)


with col1:

    if "Date de Retour" in om.index:

        st.write(
            f"📅 **Date retour :** {om['Date de Retour']}"
        )


with col2:

    if "Time Retour" in om.index:

        st.write(
            f"🕐 **Heure retour :** {om['Time Retour']}"
        )


with col3:

    if "Kilometrage au Retour" in om.index:

        st.write(
            f"🛣️ **KM retour :** "
            f"{om['Kilometrage au Retour']}"
        )


st.divider()


# ============================================================
# CALCUL KM PARCOURUS
# ============================================================

st.subheader("📏 Kilométrage")


km_depart = None
km_retour = None


if "Kilometrage au Depart" in om.index:

    try:

        km_depart = float(
            om["Kilometrage au Depart"]
        )

    except:

        km_depart = None


if "Kilometrage au Retour" in om.index:

    try:

        km_retour = float(
            om["Kilometrage au Retour"]
        )

    except:

        km_retour = None


if km_depart is not None and km_retour is not None:

    km_parcourus = km_retour - km_depart

    st.metric(
        "📏 KM parcourus",
        f"{km_parcourus:,.0f} km"
    )

else:

    st.info(
        "ℹ️ Le kilométrage parcouru ne peut pas "
        "être calculé car le KM départ ou le KM retour est manquant."
    )


st.divider()


# ============================================================
# AFFICHAGE COMPLET DE L'OM
# ============================================================

with st.expander(
    "📊 Afficher toutes les informations de l'OM"
):

    df_detail = (
        om_selectionne
        .T
        .reset_index()
    )

    df_detail.columns = [
        "Champ",
        "Valeur"
    ]

    st.dataframe(
        df_detail,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# EXPORT EXCEL
# ============================================================

st.divider()

st.subheader("📥 Exporter l'Ordre de Mission")


def generer_excel(df):

    buffer = BytesIO()

    with pd.ExcelWriter(
        buffer,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Ordre de Mission"
        )

    buffer.seek(0)

    return buffer


fichier_excel = generer_excel(
    om_selectionne
)


nom_fichier = (
    f"OM_{str(numero_om)}"
    .replace("/", "_")
    .replace("\\", "_")
    .replace(" ", "_")
    + ".xlsx"
)


st.download_button(
    label="📥 Télécharger cet Ordre de Mission en Excel",
    data=fichier_excel,
    file_name=nom_fichier,
    mime=(
        "application/vnd.openxmlformats-officedocument"
        ".spreadsheetml.sheet"
    ),
    use_container_width=True
)


# ============================================================
# APERÇU DU TABLEAU
# ============================================================

st.divider()

st.subheader("📋 Liste des Ordres de Mission")


colonnes_affichage = [
    "Status",
    "Numéro",
    "N° Commande",
    "Numero Camion",
    "Remorque",
    "Chauffeur",
    "Cde Jumelé",
    "Trajet Réel",
    "Date & Heure Chargement",
    "Date Depart",
    "Time Depart",
    "Date de Retour",
    "Time Retour",
    "Kilometrage au Depart",
    "Kilometrage au Retour"
]


colonnes_existantes = [
    colonne
    for colonne in colonnes_affichage
    if colonne in df_filtre.columns
]


st.dataframe(
    df_filtre[colonnes_existantes],
    use_container_width=True,
    hide_index=True
)
