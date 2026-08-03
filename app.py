import streamlit as st
import pandas as pd
st.set_page_config(
    page_title="TMF LOGISTICS",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.logo("https://img.icons8.com/color/96/truck.png")

st.title("🚛 TMF LOGISTICS")
st.caption("Système de Gestion des Ordres de Mission")

st.sidebar.title("Navigation")

st.sidebar.success("Choisissez une page")

st.markdown("""
## Bienvenue

Ma Première Application Logistique :

---
""")

col1,col2,col3,col4=st.columns(4)

col1.metric("Ordres de Mission","0")
col2.metric("Camions","0")
col3.metric("Chauffeurs","0")
col4.metric("Clients","0")


st.divider()

st.write("Version 1.0")
from utils import get_om

df = get_om()

st.dataframe(df.head())
import streamlit as st

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Tableau de bord",
        "📋 Ordres de Mission",
        "🚚 Camions",
        "👷 Chauffeurs",
        "👥 Clients",
        "📊 Rapports"
    ]
)

if menu == "🏠 Tableau de bord":
    st.title("Tableau de bord")
❤️❤️❤️❤️❤️
elif menu == "📋 Ordres de Mission":
    st.title("Ordres de Mission")

elif menu == "🚚 Camions":
    st.title("Camions")

elif menu == "👷 Chauffeurs":
    st.title("Chauffeurs")

elif menu == "👥 Clients":
    st.title("Clients")

elif menu == "📊 Rapports":
    st.title("Rapports")
df = pd.read_excel("DECOUCHE V1.4.xlsx")
