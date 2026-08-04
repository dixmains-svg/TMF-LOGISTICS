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

elif menu == "📋 Ordres de Mission":
    st.title("Ordres de Mission")

elif menu == "🚚 Camions":
    st.title("Camions")

elif menu == "👷 Chauffeurs":

    st.title("👷 Chauffeurs")

    df = pd.DataFrame({
        "N°": [1, 2],
        "Badge": ["123456", "987654"],
        "Chauffeur": ["Ahmed Benali", "Karim Bensalem"],
        "Fonction": ["Chauffeur PL", "Chauffeur SPL"],
        "Section/Affectation": ["Transport Oran", "Transport Alger"],
        "Superviseur": ["M. Rahmani", "M. Khelifi"]
    })

    df_modifie = st.data_editor(
        df,
        key="chauffeurs",
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic"
    )

    if st.button("💾 Enregistrer", key="save_chauffeurs"):
        st.write(df_modifie)

elif menu == "👥 Clients":
    st.title("Clients")

df = pd.DataFrame({
    "N°": [1, 2],
    "Code Client": ["CL001", "CL002"],
    "Client": ["CEVITAL", "SONATRACH"],
    "Ville": ["Béjaïa", "Alger"],
    "Adresse": ["Zone Industrielle", "Hydra"],
    "Téléphone": ["0550123456", "0661234567"],
    "Email": ["contact@cevital.com", "transport@sonatrach.dz"],
    "Contact": ["M. Benali", "Mme Amrani"]
})

df_modifie = st.data_editor(
    df,
    key="clients",
    use_container_width=True,
    hide_index=True,
    num_rows="dynamic"
)

col1, col2 = st.columns(2)

with col1:
    if st.button("💾 Enregistrer", key="save_clients"):
        st.write(df_modifie)

with col2:
    st.download_button(
        label="📥 Exporter en CSV",
        data=df_modifie.to_csv(index=False).encode("utf-8"),
        file_name="clients.csv",
        mime="text/csv"
    )
elif menu == "📊 Rapports":
    st.title("Rapports")

