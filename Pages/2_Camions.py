import streamlit as st

from database import (
    get_camions,
    ajouter_camion,
    supprimer_camion
)

st.title("🚚 Gestion des Camions")

df_camions = get_camions()

st.data_editor(
    df_camions,
    key="camions",
    use_container_width=True,
    hide_index=True,
    num_rows="dynamic"
)
