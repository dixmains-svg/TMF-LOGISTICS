import streamlit as st
import pandas as pd
from io import BytesIO
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

    st.title("👷 Gestion des Chauffeurs")

    df = pd.DataFrame({
        "N°": [1, 2],
        "Badge": ["123456", "987654"],
        "Chauffeur": ["Nadjib Benali", "Karim Bensaci"],
        "Fonction": ["Chauffeur SR", "Chauffeur SP"],
        "Section/Affectation": ["Port/Akbou", "Port/Akbou"],
        "Superviseur": ["Redjdal", "Redjdal"]
    })

    df_modifie = st.data_editor(
        df,
        key="chauffeurs",
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Enregistrer", key="save_chauffeurs"):
            st.success("Les modifications ont été enregistrées.")
            st.dataframe(df_modifie)

    with col2:

        buffer = BytesIO()

        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df_modifie.to_excel(
                writer,
                index=False,
                sheet_name="Chauffeurs"
            )

        buffer.seek(0)

        st.download_button(
            label="📥 Exporter en Excel",
            data=buffer,
            file_name="chauffeurs.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="download_chauffeurs"
        )
elif menu == "👥 Clients":

    st.title("👥 Gestion des Clients")

    df = pd.DataFrame({
        "N°": [1, 2],
        "Code Client": ["CL001", "CL002"],
        "Client": ["CEVITAL", "FRUITAL"],
        "Ville": ["Béjaïa", "Alger"],
        "Adresse": ["Zone Industrielle", "Rouiba"],
        "Téléphone": ["0550123456", "0661234567"],
        "Email": ["contact@cevital.com", "transport@fruital.dz"],
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

        buffer = BytesIO()

        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df_modifie.to_excel(
                writer,
                index=False,
                sheet_name="Clients"
            )

        buffer.seek(0)

        st.download_button(
            label="📥 Exporter en Excel",
            data=buffer,
            file_name="clients.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
elif menu == "📊 Rapports":
    st.title("Rapports")

