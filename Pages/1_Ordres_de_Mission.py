import streamlit as st
import pandas as pd

from database import (
    get_ordres_mission,
    get_camions,
    ajouter_ordre_mission
)
st.title("📋 Ordres de Mission")

# Récupérer les OM
df_om = get_ordres_mission()

# Récupérer les camions
df_camions = get_camions()

# Recherche
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

# Affichage
st.data_editor(
    df_om,
    key="ordre_mission",
    use_container_width=True,
    hide_index=True,
    num_rows="dynamic"
)
