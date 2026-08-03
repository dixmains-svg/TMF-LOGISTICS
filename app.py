import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="TMF LOGISTICS",
    page_icon="🚛",
    layout="wide"
)

st.title("🚛 TMF LOGISTICS")
st.write("Application de suivi des missions")

# Charger le fichier Excel
@st.cache_data
def charger_donnees():
    fichier = "DECOUCHE V1.4.xlsx"
    feuilles = pd.read_excel(fichier, sheet_name=None)

    if "Input OM Fini" in feuilles:
        return feuilles["Input OM Fini"]

    return list(feuilles.values())[0]

df = charger_donnees()

st.success("Fichier chargé avec succès")

# Affichage
st.subheader("Données")

st.dataframe(df, use_container_width=True)

# Recherche
st.subheader("Recherche")

texte = st.text_input("Rechercher")

if texte:
    resultat = df.astype(str).apply(
        lambda x: x.str.contains(texte, case=False, na=False)
    ).any(axis=1)

    st.dataframe(df[resultat], use_container_width=True)

# Statistiques
st.subheader("Statistiques")

col1, col2 = st.columns(2)

with col1:
    st.metric("Nombre de lignes", len(df))

with col2:
    st.metric("Nombre de colonnes", len(df.columns))

# Colonnes disponibles
st.subheader("Colonnes")

st.write(df.columns.tolist())