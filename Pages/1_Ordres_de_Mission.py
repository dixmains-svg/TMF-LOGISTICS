import streamlit as st
import pandas as pd

from database import (
    get_ordres_mission,
    get_camions,
    ajouter_ordre_mission
)


# ============================================================
# CONFIGURATION
# ============================================================

st.title("📋 Ordres de Mission")

st.subheader(
    "Gestion des Ordres de Mission"
)

st.divider()


# ============================================================
# RÉCUPÉRER LES DONNÉES
# ============================================================

df_om = get_ordres_mission()

df_camions = get_camions()


# ============================================================
# RECHERCHE
# ============================================================

recherche = st.text_input(
    "🔍 Rechercher un OM, camion, chauffeur ou client"
)


if recherche:

    masque = (
        df_om.astype(str)
        .apply(
            lambda colonne: colonne.str.contains(
                recherche,
                case=False,
                na=False
            )
        )
        .any(axis=1)
    )

    df_om = df_om[masque]


# ============================================================
# STATISTIQUES
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📋 Total OM",
        len(df_om)
    )

with col2:
    st.metric(
        "🚚 Camions",
        len(df_camions)
    )

with col3:
    st.metric(
        "🔎 Résultats",
        len(df_om)
    )


st.divider()


# ============================================================
# AFFICHAGE DES ORDRES DE MISSION
# ============================================================

st.subheader("📋 Liste des Ordres de Mission")


if df_om.empty:

    st.info(
        "Aucun Ordre de Mission trouvé."
    )

else:

    st.data_editor(
        df_om,
        key="ordre_mission",
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic"
    )
