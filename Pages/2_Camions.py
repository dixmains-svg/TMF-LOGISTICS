import streamlit as st
import pandas as pd

from database import (
    get_camions,
    ajouter_camion,
    supprimer_camion
)

st.title("🚚 Gestion des Camions")

# ============================================================
# CHARGER LES CAMIONS
# ============================================================

df_camions = get_camions()

# ============================================================
# RECHERCHE
# ============================================================

recherche = st.text_input(
    "🔍 Rechercher un camion",
    placeholder="Numéro camion, chauffeur, client..."
)

if recherche:
    masque = (
        df_camions.astype(str)
        .apply(
            lambda colonne: colonne.str.contains(
                recherche,
                case=False,
                na=False
            )
        )
        .any(axis=1)
    )

    df_camions = df_camions[masque]

# ============================================================
# AFFICHAGE
# ============================================================

st.data_editor(
    df_camions,
    key="tableau_camions",
    use_container_width=True,
    hide_index=True,
    num_rows="dynamic"
)
