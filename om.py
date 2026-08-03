import streamlit as st
import pandas as pd
from utils import get_om

st.set_page_config(
    page_title="Ordres de Mission",
    page_icon="🚛",
    layout="wide"
)

st.title("🚛 Gestion des Ordres de Mission")

# Chargement des données
df = get_om()

st.write(f"Nombre d'OM : {len(df)}")

# Barre de recherche
recherche = st.text_input("Recherche")

if recherche:
    masque = (
        df.astype(str)
          .apply(lambda col: col.str.contains(recherche, case=False, na=False))
          .any(axis=1)
    )
    df = df[masque]

# Feuille Excel éditable
df_modifie = st.data_editor(
    df,
    use_container_width=True,
    num_rows="dynamic",
    hide_index=True
)

col1, col2 = st.columns(2)

with col1:
    if st.button("💾 Enregistrer en Excel"):
        df_modifie.to_excel("OM_Modifie.xlsx", index=False)
        st.success("Le fichier OM_Modifie.xlsx a été créé.")

with col2:
    if st.button("🔄 Recharger"):
        st.rerun()