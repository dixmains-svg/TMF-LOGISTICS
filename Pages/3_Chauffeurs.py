import streamlit as st
import pandas as pd
from io import BytesIO

from database import (
    get_chauffeurs,
    ajouter_chauffeur,
    supprimer_chauffeur
)


# ============================================================
# CONFIGURATION
# ============================================================

st.title("👷 Gestion des Chauffeurs")

st.caption(
    "Gestion des chauffeurs TMF LOGISTICS"
)

st.divider()


# ============================================================
# CHARGER LES CHAUFFEURS
# ============================================================

df = get_chauffeurs()


# ============================================================
# INDICATEURS
# ============================================================

nombre_chauffeurs = len(df)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "👷 Nombre de chauffeurs",
        nombre_chauffeurs
    )

with col2:
    if not df.empty and "fonction" in df.columns:
        nombre_fonctions = df["fonction"].nunique()
    else:
        nombre_fonctions = 0

    st.metric(
        "📋 Fonctions",
        nombre_fonctions
    )


st.divider()


# ============================================================
# RECHERCHE
# ============================================================

recherche = st.text_input(
    "🔍 Rechercher un chauffeur",
    placeholder="Nom, badge, fonction, section..."
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
# AJOUTER UN CHAUFFEUR
# ============================================================

with st.expander("➕ Ajouter un chauffeur"):

    col1, col2 = st.columns(2)

    with col1:

        badge = st.text_input(
            "🪪 Badge"
        )

        chauffeur = st.text_input(
            "👷 Nom et prénom"
        )

        fonction = st.selectbox(
            "📋 Fonction",
            [
                "Chauffeur PL",
                "Chauffeur SPL",
                "Chauffeur SR",
                "Chauffeur SP",
                "Autre"
            ]
        )

    with col2:

        section_affectation = st.text_input(
            "📍 Section / Affectation"
        )

        superviseur = st.text_input(
            "👤 Superviseur"
        )

    if st.button(
        "💾 Ajouter le chauffeur",
        type="primary"
    ):

        if not chauffeur.strip():

            st.error(
                "⚠️ Veuillez saisir le nom du chauffeur."
            )

        else:

            try:

                ajouter_chauffeur(
                    badge=badge,
                    chauffeur=chauffeur,
                    fonction=fonction,
                    section_affectation=section_affectation,
                    superviseur=superviseur
                )

                st.success(
                    f"✅ {chauffeur} a été ajouté."
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"❌ Erreur : {e}"
                )


# ============================================================
# LISTE DES CHAUFFEURS
# ============================================================

st.subheader("👷 Liste des chauffeurs")


if df.empty:

    st.info(
        "Aucun chauffeur enregistré dans la base de données."
    )

else:

    df_affichage = df.copy()

    # Renommer les colonnes
    renommage = {
        "id": "ID",
        "badge": "Badge",
        "chauffeur": "Chauffeur",
        "fonction": "Fonction",
        "section_affectation": "Section / Affectation",
        "superviseur": "Superviseur",
        "created_at": "Date création"
    }

    df_affichage.rename(
        columns=renommage,
        inplace=True
    )

    # Numérotation
    df_affichage.insert(
        0,
        "N°",
        range(1, len(df_affichage) + 1)
    )

    st.dataframe(
        df_affichage,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# EXPORT
# ============================================================

st.divider()

if not df.empty:

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # EXPORT EXCEL
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
                sheet_name="Chauffeurs"
            )

        buffer.seek(0)

        st.download_button(
            label="📥 Exporter en Excel",
            data=buffer,
            file_name="chauffeurs.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            )
        )

    # --------------------------------------------------------
    # EXPORT CSV
    # --------------------------------------------------------

    with col2:

        csv = df_affichage.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📄 Exporter en CSV",
            data=csv,
            file_name="chauffeurs.csv",
            mime="text/csv"
        )
