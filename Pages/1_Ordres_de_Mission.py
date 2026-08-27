import streamlit as st
# Importation depuis le nouveau fichier navision_api.py
from navision_api import charger_donnees_nav

st.title("📋 Ordres de Mission")

# Remplacez 'OrdresDeMission' par le nom exact de votre Web Service OData Navision
with st.spinner("Chargement des données depuis Navision..."):
    df_om = charger_donnees_nav("OrdresDeMission")

if not df_om.empty:
    st.dataframe(df_om, use_container_width=True)
else:
    st.warning("Aucune donnée disponible dans Navision.")
