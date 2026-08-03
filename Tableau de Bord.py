import streamlit as st
import plotly.express as px
from utils import get_om, statistiques

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Tableau de bord")

# Chargement des données
df = get_om()

# Statistiques générales
stats = statistiques(df)

col1, col2, col3 = st.columns(3)

col1.metric("Ordres de Mission", stats["lignes"])
col2.metric("Colonnes", stats["colonnes"])
col3.metric("Feuille", "Input OM Fini")

st.divider()

st.subheader("Aperçu des données")

st.dataframe(df.head(20), use_container_width=True)

st.divider()

st.subheader("Informations générales")

st.write(f"Nombre de lignes : **{stats['lignes']}**")
st.write(f"Nombre de colonnes : **{stats['colonnes']}**")

st.divider()

# Sélection d'une colonne pour afficher les statistiques
colonnes = df.columns.tolist()

colonne = st.selectbox(
    "Choisir une colonne",
    colonnes
)

if colonne:

    compte = (
        df[colonne]
        .fillna("Vide")
        .astype(str)
        .value_counts()
        .head(20)
        .reset_index()
    )

    compte.columns = ["Valeur", "Nombre"]

    st.subheader(f"Répartition : {colonne}")

    fig = px.bar(
        compte,
        x="Valeur",
        y="Nombre",
        text="Nombre"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

with st.expander("Liste des colonnes"):

    for c in colonnes:
        st.write("•", c)