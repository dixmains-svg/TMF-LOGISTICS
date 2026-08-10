import streamlit as st
from database import get_camions

st.title("🚚 Gestion des Camions")

df = get_camions()

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)import streamlit as st
import pandas as pd
from io import BytesIO

from database.database import (
    get_camions,
    ajouter_camion,
    supprimer_camion
)


# ============================================================
# CONFIGURATION
# ============================================================

st.title("🚚 Gestion des Camions")

st.caption(
    "Gestion de la flotte des véhicules TMF LOGISTICS"
)

st.divider()


# ============================================================
# CHARGER LES CAMIONS
# ============================================================

df = get_camions()


# ============================================================
# INDICATEURS
# ============================================================

nombre_camions = len(df)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🚚 Nombre de camions",
        nombre_camions
    )

with col2:
    if not df.empty and "statut" in df.columns:
        disponibles = (
            df["statut"]
            .astype(str)
            .str.lower()
            .eq("disponible")
            .sum()
        )
    else:
        disponibles = 0

    st.metric(
        "✅ Disponibles",
        disponibles
    )

with col3:
    if not df.empty and "statut" in df.columns:
        en_mission = (
            df["statut"]
            .astype(str)
            .str.lower()
            .eq("en mission")
            .sum()
        )
    else:
        en_mission = 0

    st.metric(
        "🚛 En mission",
        en_mission
    )


st.divider()


# ============================================================
# BARRE DE RECHERCHE
# ============================================================

recherche = st.text_input(
    "🔍 Rechercher",
    placeholder="Camion, remorque, chauffeur, client..."
)


if recherche and not df.empty:

    masque = (
        df.astype(str)
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

    df = df[masque]


# ============================================================
# FORMULAIRE AJOUT CAMION
# ============================================================

with st.expander("➕ Ajouter un camion"):

    col1, col2 = st.columns(2)

    with col1:

        camion = st.text_input(
            "🚚 Numéro du camion"
        )

        remorque = st.text_input(
            "🔗 Remorque"
        )

        chauffeur = st.text_input(
            "👷 Chauffeur"
        )

    with col2:

        statut = st.selectbox(
            "📌 Statut",
            [
                "Disponible",
                "En mission",
                "En maintenance",
                "Immobilisé"
            ]
        )

        client = st.text_input(
            "👥 Client"
        )

        mission = st.text_input(
            "📦 Mission"
        )

    if st.button(
        "💾 Ajouter le camion",
        type="primary"
    ):

        if not camion.strip():

            st.error(
                "⚠️ Veuillez saisir le numéro du camion."
            )

        else:

            try:

                ajouter_camion(
                    camion=camion,
                    remorque=remorque,
                    chauffeur=chauffeur,
                    statut=statut,
                    client=client,
                    mission=mission
                )

                st.success(
                    f"✅ Le camion {camion} a été ajouté."
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"❌ Erreur : {e}"
                )


# ============================================================
# TABLEAU DES CAMIONS
# ============================================================

st.subheader("🚚 Liste des camions")


if df.empty:

    st.info(
        "Aucun camion enregistré dans la base de données."
    )

else:

    # Renommer les colonnes pour l'affichage
    df_affichage = df.copy()

    renommage = {
        "id": "ID",
        "camion": "Camion",
        "remorque": "Remorque",
        "chauffeur": "Chauffeur",
        "statut": "Statut",
        "client": "Client",
        "mission": "Mission",
        "created_at": "Date création"
    }

    df_affichage.rename(
        columns=renommage,
        inplace=True
    )

    # Ajouter une numérotation
    df_affichage.insert(
        0,
        "N°",
        range(1, len(df_affichage) + 1)
    )

    # Tableau
    st.dataframe(
        df_affichage,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# EXPORT EXCEL
# ============================================================

st.divider()

if not df.empty:

    col1, col2 = st.columns(2)

    with col1:

        buffer = BytesIO()

        with pd.ExcelWriter(
            buffer,
            engine="openpyxl"
        ) as writer:

            df_affichage.to_excel(
                writer,
                index=False,
                sheet_name="Camions"
            )

        buffer.seek(0)

        st.download_button(
            label="📥 Exporter en Excel",
            data=buffer,
            file_name="camions.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            )
        )

    with col2:

        csv = df_affichage.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📄 Exporter en CSV",
            data=csv,
            file_name="camions.csv",
            mime="text/csv"
        )
