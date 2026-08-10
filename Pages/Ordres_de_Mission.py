import streamlit as st
import pandas as pd
from io import BytesIO

from database.database import (
    get_ordres_mission,
    ajouter_ordre_mission,
    get_camions,
    get_chauffeurs,
    get_clients
)


# ============================================================
# CONFIGURATION
# ============================================================

st.title("📋 Ordres de Mission")

st.caption(
    "Gestion et suivi des Ordres de Mission - TMF LOGISTICS"
)

st.divider()


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

df_om = get_ordres_mission()
df_camions = get_camions()
df_chauffeurs = get_chauffeurs()
df_clients = get_clients()


# ============================================================
# INDICATEURS
# ============================================================

nombre_om = len(df_om)

if not df_om.empty and "statut" in df_om.columns:
    nombre_en_cours = (
        df_om["statut"]
        .astype(str)
        .str.lower()
        .eq("En cours".lower())
        .sum()
    )
else:
    nombre_en_cours = 0


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📋 Total OM",
        nombre_om
    )

with col2:
    st.metric(
        "🚛 OM en cours",
        nombre_en_cours
    )

with col3:
    if not df_om.empty and "client" in df_om.columns:
        nombre_clients = df_om["client"].nunique()
    else:
        nombre_clients = 0

    st.metric(
        "👥 Clients concernés",
        nombre_clients
    )


st.divider()


# ============================================================
# RECHERCHE
# ============================================================

recherche = st.text_input(
    "🔍 Rechercher un OM",
    placeholder="N° OM, camion, chauffeur ou client..."
)


df_affichage = df_om.copy()


if recherche and not df_affichage.empty:

    masque = (
        df_affichage["numero_om"]
        .astype(str)
        .str.contains(
            recherche,
            case=False,
            na=False
        )
        |
        df_affichage["camion"]
        .astype(str)
        .str.contains(
            recherche,
            case=False,
            na=False
        )
        |
        df_affichage["chauffeur"]
        .astype(str)
        .str.contains(
            recherche,
            case=False,
            na=False
        )
        |
        df_affichage["client"]
        .astype(str)
        .str.contains(
            recherche,
            case=False,
            na=False
        )
    )

    df_affichage = df_affichage[masque]


# ============================================================
# AJOUTER UN ORDRE DE MISSION
# ============================================================

with st.expander("➕ Créer un nouvel Ordre de Mission"):

    st.subheader("Informations générales")

    col1, col2, col3 = st.columns(3)

    with col1:

        numero_om = st.text_input(
            "📋 N° OM",
            placeholder="OM-2026-001"
        )

        commande = st.text_input(
            "📦 N° Commande"
        )

    with col2:

        # Liste des camions
        if not df_camions.empty and "camion" in df_camions.columns:

            liste_camions = (
                df_camions["camion"]
                .dropna()
                .astype(str)
                .tolist()
            )

        else:

            liste_camions = []

        if liste_camions:

            camion = st.selectbox(
                "🚚 Camion",
                [""] + liste_camions
            )

        else:

            camion = st.text_input(
                "🚚 Camion"
            )

    with col3:

        if (
            not df_camions.empty
            and "remorque" in df_camions.columns
        ):

            liste_remorques = (
                df_camions["remorque"]
                .dropna()
                .astype(str)
                .drop_duplicates()
                .tolist()
            )

        else:

            liste_remorques = []

        if liste_remorques:

            remorque = st.selectbox(
                "🔗 Remorque",
                [""] + liste_remorques
            )

        else:

            remorque = st.text_input(
                "🔗 Remorque"
            )


    # ========================================================
    # CHAUFFEUR / CLIENT
    # ========================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        if (
            not df_chauffeurs.empty
            and "chauffeur" in df_chauffeurs.columns
        ):

            liste_chauffeurs = (
                df_chauffeurs["chauffeur"]
                .dropna()
                .astype(str)
                .tolist()
            )

        else:

            liste_chauffeurs = []

        if liste_chauffeurs:

            chauffeur = st.selectbox(
                "👷 Chauffeur",
                [""] + liste_chauffeurs
            )

        else:

            chauffeur = st.text_input(
                "👷 Chauffeur"
            )

    with col2:

        if (
            not df_clients.empty
            and "client" in df_clients.columns
        ):

            liste_clients = (
                df_clients["client"]
                .dropna()
                .astype(str)
                .tolist()
            )

        else:

            liste_clients = []

        if liste_clients:

            client = st.selectbox(
                "👥 Client",
                [""] + liste_clients
            )

        else:

            client = st.text_input(
                "👥 Client"
            )

    with col3:

        mission = st.text_input(
            "📍 Mission / Trajet"
        )


    # ========================================================
    # DATES
    # ========================================================

    st.subheader("🕐 Départ et retour")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        date_depart = st.date_input(
            "Date départ"
        )

    with col2:

        heure_depart = st.time_input(
            "Heure départ"
        )

    with col3:

        date_retour = st.date_input(
            "Date retour"
        )

    with col4:

        heure_retour = st.time_input(
            "Heure retour"
        )


    # ========================================================
    # KILOMÉTRAGE
    # ========================================================

    st.subheader("🛣️ Kilométrage")

    col1, col2, col3 = st.columns(3)

    with col1:

        km_depart = st.number_input(
            "KM départ",
            min_value=0.0,
            step=1.0
        )

    with col2:

        km_retour = st.number_input(
            "KM retour",
            min_value=0.0,
            step=1.0
        )

    with col3:

        km_parcourus = max(
            0,
            km_retour - km_depart
        )

        st.number_input(
            "KM parcourus",
            value=float(km_parcourus),
            disabled=True
        )


    # ========================================================
    # STATUT
    # ========================================================

    statut = st.selectbox(
        "📌 Statut",
        [
            "Planifié",
            "En cours",
            "Terminé",
            "Annulé"
        ]
    )


    # ========================================================
    # ENREGISTREMENT
    # ========================================================

    if st.button(
        "💾 Enregistrer l'Ordre de Mission",
        type="primary"
    ):

        if not numero_om.strip():

            st.error(
                "⚠️ Veuillez saisir le N° OM."
            )

        elif not camion:

            st.error(
                "⚠️ Veuillez sélectionner un camion."
            )

        elif not chauffeur:

            st.error(
                "⚠️ Veuillez sélectionner un chauffeur."
            )

        elif not client:

            st.error(
                "⚠️ Veuillez sélectionner un client."
            )

        else:

            try:

                ajouter_ordre_mission({

                    "numero_om": numero_om,

                    "commande": commande,

                    "camion": camion,

                    "remorque": remorque,

                    "chauffeur": chauffeur,

                    "client": client,

                    "mission": mission,

                    "date_depart": str(date_depart),

                    "heure_depart": str(heure_depart),

                    "date_retour": str(date_retour),

                    "heure_retour": str(heure_retour),

                    "km_depart": km_depart,

                    "km_retour": km_retour,

                    "km_parcourus": km_parcourus,

                    "statut": statut
                })

                st.success(
                    f"✅ L'OM {numero_om} a été enregistré."
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"❌ Erreur lors de l'enregistrement : {e}"
                )


# ============================================================
# LISTE DES ORDRES DE MISSION
# ============================================================

st.divider()

st.subheader("📋 Liste des Ordres de Mission")


if df_affichage.empty:

    st.info(
        "Aucun Ordre de Mission enregistré."
    )

else:

    # --------------------------------------------------------
    # Préparer les colonnes d'affichage
    # --------------------------------------------------------

    colonnes = [
        "id",
        "numero_om",
        "commande",
        "camion",
        "remorque",
        "chauffeur",
        "client",
        "mission",
        "date_depart",
        "heure_depart",
        "date_retour",
        "heure_retour",
        "km_depart",
        "km_retour",
        "km_parcourus",
        "statut"
    ]

    colonnes_existantes = [
        colonne
        for colonne in colonnes
        if colonne in df_affichage.columns
    ]

    df_affichage = df_affichage[
        colonnes_existantes
    ].copy()


    # --------------------------------------------------------
    # Renommer
    # --------------------------------------------------------

    renommage = {

        "id": "ID",

        "numero_om": "N° OM",

        "commande": "Commande",

        "camion": "Camion",

        "remorque": "Remorque",

        "chauffeur": "Chauffeur",

        "client": "Client",

        "mission": "Mission",

        "date_depart": "Date Départ",

        "heure_depart": "Heure Départ",

        "date_retour": "Date Retour",

        "heure_retour": "Heure Retour",

        "km_depart": "KM Départ",

        "km_retour": "KM Retour",

        "km_parcourus": "KM Parcourus",

        "statut": "Statut"
    }

    df_affichage.rename(
        columns=renommage,
        inplace=True
    )


    # --------------------------------------------------------
    # Numérotation
    # --------------------------------------------------------

    df_affichage.insert(
        0,
        "N°",
        range(
            1,
            len(df_affichage) + 1
        )
    )


    # --------------------------------------------------------
    # Affichage
    # --------------------------------------------------------

    st.dataframe(
        df_affichage,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# EXPORT EXCEL / CSV
# ============================================================

if not df_affichage.empty:

    st.divider()

    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # EXCEL
    # --------------------------------------------------------

    with col1:

        buffer = BytesIO()

        with pd.ExcelWriter(
            buffer,
            engine="openpyxl"
        ) as writer:

            df_affichage.to_excel(
                writer,
                index=False,
                sheet_name="Ordres de Mission"
            )

        buffer.seek(0)

        st.download_button(
            label="📥 Exporter en Excel",
            data=buffer,
            file_name="ordres_de_mission.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            )
        )


    # --------------------------------------------------------
    # CSV
    # --------------------------------------------------------

    with col2:

        csv = df_affichage.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📄 Exporter en CSV",
            data=csv,
            file_name="ordres_de_mission.csv",
            mime="text/csv"
        )