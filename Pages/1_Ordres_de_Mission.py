import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TMF LOGISTICS - Ordres de Mission",
    page_icon="📋",
    layout="wide"
)


# ============================================================
# CHEMIN DU FICHIER EXCEL
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

FICHIER_OM = BASE_DIR / "Data" / "OM.xlsx"

FEUILLE_OM = "Input OM fini"


# ============================================================
# COLONNES PRINCIPALES À AFFICHER
# ============================================================

COLONNES_OM = [
    "Status",
    "Numéro",
    "N° Commande",
    "Numero Camion",
    "Remorque",
    "Chauffeur",
    "Matricule du Chauffeur",
    "Trajet Réel",
    "Date Depart",
    "Time Depart",
    "Date de Retour",
    "Time Retour",
    "Kilometrage au Depart",
    "Kilometrage au Retour",
    "Kilometrage Parcouru",
    "Date & Heure Dechargement",
    "Date Arrivée Destination",
    "Section",
    "Lieu de Chargement",
    "Lieu de DéChargement",
    "Client",
    "Objet de la Mission",
    "Nom du destinataire",
    "Tonnage",
    "Nature du Chargement",
    "Affectation",
    "Produit_Transporté"
]


# ============================================================
# LECTURE DU FICHIER EXCEL
# ============================================================

def charger_om():

    if not EXCEL_OM.exists():
        return pd.DataFrame()

    try:

        df = pd.read_excel(
            EXCEL_OM,
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

    except Exception as e:

        st.error(
            f"❌ Erreur lors de la lecture de OM.xlsx : {e}"
        )

        return pd.DataFrame()

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
            f"❌ Erreur lors de la lecture du fichier OM.xlsx : {e}"
        )

        return pd.DataFrame()


# ============================================================
# CHARGEMENT
# ============================================================

df_om = charger_om()


# ============================================================
# VÉRIFICATION
# ============================================================

if df_om.empty:

    st.error(
        f"""
        ❌ Le fichier OM.xlsx est introuvable ou vide.

        Fichier recherché :

        `{FICHIER_OM}`
        """
    )

    st.stop()


# ============================================================
# TITRE
# ============================================================

st.title("📋 Ordres de Mission")

st.subheader(
    "Gestion des Ordres de Mission - TMF LOGISTICS"
)


# ============================================================
# INFORMATIONS SUR LE FICHIER
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "📋 Total OM",
        len(df_om)
    )


with col2:

    if "Status" in df_om.columns:

        nombre_statuts = (
            df_om["Status"]
            .replace("", pd.NA)
            .nunique()
        )

    else:

        nombre_statuts = 0

    st.metric(
        "📊 Statuts",
        nombre_statuts
    )


with col3:

    if "Numero Camion" in df_om.columns:

        nombre_camions = (
            df_om["Numero Camion"]
            .replace("", pd.NA)
            .nunique()
        )

    else:

        nombre_camions = 0

    st.metric(
        "🚚 Camions",
        nombre_camions
    )


with col4:

    if "Chauffeur" in df_om.columns:

        nombre_chauffeurs = (
            df_om["Chauffeur"]
            .replace("", pd.NA)
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

st.subheader("🔎 Recherche")

recherche = st.text_input(
    "Rechercher un Ordre de Mission",
    placeholder=(
        "N° OM, commande, camion, chauffeur, client, "
        "mission, trajet..."
    )
)


# ============================================================
# FILTRES
# ============================================================

col1, col2, col3 = st.columns(3)


# ------------------------------------------------------------
# FILTRE STATUT
# ------------------------------------------------------------

with col1:

    if "Status" in df_om.columns:

        statuts = sorted(
            [
                str(x)
                for x in df_om["Status"]
                .dropna()
                .unique()
                if str(x).strip()
            ]
        )

        filtre_statut = st.multiselect(
            "📊 Statut",
            statuts
        )

    else:

        filtre_statut = []


# ------------------------------------------------------------
# FILTRE CAMION
# ------------------------------------------------------------

with col2:

    if "Numero Camion" in df_om.columns:

        camions = sorted(
            [
                str(x)
                for x in df_om["Numero Camion"]
                .dropna()
                .unique()
                if str(x).strip()
            ]
        )

        filtre_camion = st.multiselect(
            "🚚 Camion",
            camions
        )

    else:

        filtre_camion = []


# ------------------------------------------------------------
# FILTRE CLIENT
# ------------------------------------------------------------

with col3:

    if "Client" in df_om.columns:

        clients = sorted(
            [
                str(x)
                for x in df_om["Client"]
                .dropna()
                .unique()
                if str(x).strip()
            ]
        )

        filtre_client = st.multiselect(
            "👥 Client",
            clients
        )

    else:

        filtre_client = []


# ============================================================
# DEUXIÈME LIGNE DE FILTRES
# ============================================================

col1, col2, col3 = st.columns(3)


# ------------------------------------------------------------
# CHAUFFEUR
# ------------------------------------------------------------

with col1:

    if "Chauffeur" in df_om.columns:

        chauffeurs = sorted(
            [
                str(x)
                for x in df_om["Chauffeur"]
                .dropna()
                .unique()
                if str(x).strip()
            ]
        )

        filtre_chauffeur = st.multiselect(
            "👷 Chauffeur",
            chauffeurs
        )

    else:

        filtre_chauffeur = []


# ------------------------------------------------------------
# AFFECTATION
# ------------------------------------------------------------

with col2:

    if "Affectation" in df_om.columns:

        affectations = sorted(
            [
                str(x)
                for x in df_om["Affectation"]
                .dropna()
                .unique()
                if str(x).strip()
            ]
        )

        filtre_affectation = st.multiselect(
            "📍 Affectation",
            affectations
        )

    else:

        filtre_affectation = []


# ------------------------------------------------------------
# SECTION
# ------------------------------------------------------------

with col3:

    if "Section" in df_om.columns:

        sections = sorted(
            [
                str(x)
                for x in df_om["Section"]
                .dropna()
                .unique()
                if str(x).strip()
            ]
        )

        filtre_section = st.multiselect(
            "🏢 Section",
            sections
        )

    else:

        filtre_section = []


# ============================================================
# FILTRAGE
# ============================================================

df_filtre = df_om.copy()


# ------------------------------------------------------------
# RECHERCHE GÉNÉRALE
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
# STATUT
# ------------------------------------------------------------

if filtre_statut:

    df_filtre = df_filtre[
        df_filtre["Status"].isin(
            filtre_statut
        )
    ]


# ------------------------------------------------------------
# CAMION
# ------------------------------------------------------------

if filtre_camion:

    df_filtre = df_filtre[
        df_filtre["Numero Camion"].isin(
            filtre_camion
        )
    ]


# ------------------------------------------------------------
# CLIENT
# ------------------------------------------------------------

if filtre_client:

    df_filtre = df_filtre[
        df_filtre["Client"].isin(
            filtre_client
        )
    ]


# ------------------------------------------------------------
# CHAUFFEUR
# ------------------------------------------------------------

if filtre_chauffeur:

    df_filtre = df_filtre[
        df_filtre["Chauffeur"].isin(
            filtre_chauffeur
        )
    ]


# ------------------------------------------------------------
# AFFECTATION
# ------------------------------------------------------------

if filtre_affectation:

    df_filtre = df_filtre[
        df_filtre["Affectation"].isin(
            filtre_affectation
        )
    ]


# ------------------------------------------------------------
# SECTION
# ------------------------------------------------------------

if filtre_section:

    df_filtre = df_filtre[
        df_filtre["Section"].isin(
            filtre_section
        )
    ]


# ============================================================
# RÉSULTAT
# ============================================================

st.divider()

st.subheader(
    f"📋 Liste des Ordres de Mission ({len(df_filtre)})"
)


# ============================================================
# TABLEAU PRINCIPAL
# ============================================================

colonnes_disponibles = [
    colonne
    for colonne in COLONNES_OM
    if colonne in df_filtre.columns
]


df_affichage = df_filtre[
    colonnes_disponibles
].copy()


st.dataframe(
    df_affichage,
    use_container_width=True,
    hide_index=True,
    height=550
)


# ============================================================
# DÉTAIL D'UN ORDRE DE MISSION
# ============================================================

st.divider()

st.subheader("🔍 Détails d'un Ordre de Mission")


if "Numéro" in df_om.columns:

    numeros_om = [
        str(x)
        for x in df_om["Numéro"]
        .dropna()
        .unique()
        if str(x).strip()
    ]

    numero_selectionne = st.selectbox(
        "Sélectionner un N° OM",
        numeros_om
    )

    if numero_selectionne:

        detail = df_om[
            df_om["Numéro"].astype(str)
            == numero_selectionne
        ]

        if not detail.empty:

            ligne = detail.iloc[0]

            col1, col2, col3 = st.columns(3)

            with col1:

                st.markdown("### 📋 Mission")

                st.write(
                    f"**N° OM :** {ligne.get('Numéro', '')}"
                )

                st.write(
                    f"**Statut :** {ligne.get('Status', '')}"
                )

                st.write(
                    f"**Commande :** {ligne.get('N° Commande', '')}"
                )

                st.write(
                    f"**Client :** {ligne.get('Client', '')}"
                )

                st.write(
                    f"**Objet :** {ligne.get('Objet de la Mission', '')}"
                )

            with col2:

                st.markdown("### 🚚 Transport")

                st.write(
                    f"**Camion :** {ligne.get('Numero Camion', '')}"
                )

                st.write(
                    f"**Remorque :** {ligne.get('Remorque', '')}"
                )

                st.write(
                    f"**Chauffeur :** {ligne.get('Chauffeur', '')}"
                )

                st.write(
                    f"**Matricule :** {ligne.get('Matricule du Chauffeur', '')}"
                )

                st.write(
                    f"**Affectation :** {ligne.get('Affectation', '')}"
                )

            with col3:

                st.markdown("### 📍 Trajet")

                st.write(
                    f"**Trajet :** {ligne.get('Trajet Réel', '')}"
                )

                st.write(
                    f"**Chargement :** {ligne.get('Lieu de Chargement', '')}"
                )

                st.write(
                    f"**Déchargement :** {ligne.get('Lieu de DéChargement', '')}"
                )

                st.write(
                    f"**Section :** {ligne.get('Section', '')}"
                )

                st.write(
                    f"**Destination :** {ligne.get('Adresse destinataire', '')}"
                )


            st.markdown("### 🕐 Dates et horaires")

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.write(
                    f"**Départ :** {ligne.get('Date Depart', '')}"
                )

            with col2:

                st.write(
                    f"**Heure départ :** {ligne.get('Time Depart', '')}"
                )

            with col3:

                st.write(
                    f"**Retour :** {ligne.get('Date de Retour', '')}"
                )

            with col4:

                st.write(
                    f"**Heure retour :** {ligne.get('Time Retour', '')}"
                )


            st.markdown("### 🛣️ Kilométrage")

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "KM Départ",
                    ligne.get(
                        "Kilometrage au Depart",
                        ""
                    )
                )

            with col2:

                st.metric(
                    "KM Retour",
                    ligne.get(
                        "Kilometrage au Retour",
                        ""
                    )
                )

            with col3:

                st.metric(
                    "KM Parcourus",
                    ligne.get(
                        "Kilometrage Parcouru",
                        ""
                    )
                )


            st.markdown("### 📦 Chargement")

            col1, col2, col3 = st.columns(3)

            with col1:

                st.write(
                    f"**Tonnage :** {ligne.get('Tonnage', '')}"
                )

            with col2:

                st.write(
                    f"**Nature :** {ligne.get('Nature du Chargement', '')}"
                )

            with col3:

                st.write(
                    f"**Produit :** {ligne.get('Produit_Transporté', '')}"
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

        # Données filtrées
        df.to_excel(
            writer,
            index=False,
            sheet_name="Ordres de Mission"
        )

        # Si possible, ajouter les informations complètes
        # dans une deuxième feuille
        df.to_excel(
            writer,
            index=False,
            sheet_name="Données"
        )

    return buffer.getvalue()


fichier_excel = convertir_excel(df_filtre)


st.download_button(
    label="📥 Télécharger les OM filtrés",
    data=fichier_excel,
    file_name="Ordres_de_Mission_filtrés.xlsx",
    mime=(
        "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet"
    )
)


# ============================================================
# ACTUALISER LES DONNÉES
# ============================================================

st.divider()

if st.button("🔄 Actualiser les données"):

    st.cache_data.clear()

    st.rerun()
