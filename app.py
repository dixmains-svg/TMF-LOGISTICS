import streamlit as st
import pandas as pd
from io import BytesIO
from utils import get_om
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

df_camions = pd.read_excel("camion.xlsx")

nombre_camions = df_camions["Camion"].count()

col2.metric("🚚 Nombre de camions", nombre_camions)
col3.metric("Chauffeurs","0")
col4.metric("Clients","0")


st.divider()
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

    st.title("📋 Ordres de Mission")

    df = pd.read_excel("OM.xlsx")

    df.columns = df.columns.str.strip()

    df_om = df[
        [
            "Numéro",
            "N° Commande",
            "Numero Camion",
            "Remorque",
            "Chauffeur",
            "Client",
            "Trajet Réel",
            "Date Depart",
            "Time Depart",
            "Date de Retour",
            "Time Retour",
            "Kilometrage au Depart",
            "Kilometrage au Retour",
            "Kilometrage Parcouru",
            "Status"
        ]
    ].copy()

    df_om.columns = [
        "N° OM",
        "Commande",
        "Camion",
        "Remorque",
        "Chauffeur",
        "Client",
        "Mission",
        "Date Départ",
        "Heure Départ",
        "Date Retour",
        "Heure Retour",
        "KM Départ",
        "KM Retour",
        "KM Parcourus",
        "Statut"
    ]

    recherche = st.text_input(
        "🔍 Rechercher un OM, un camion, un chauffeur ou un client"
    )

    if recherche:
        masque = (
            df_om["N° OM"].astype(str).str.contains(recherche, case=False, na=False)
            | df_om["Camion"].astype(str).str.contains(recherche, case=False, na=False)
            | df_om["Chauffeur"].astype(str).str.contains(recherche, case=False, na=False)
            | df_om["Client"].astype(str).str.contains(recherche, case=False, na=False)
        )
        df_om = df_om[masque]

    # Tableau modifiable
    df_modifie = st.data_editor(
        df_om,
        key="ordre_mission",
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Enregistrer", key="save_om"):
            df_modifie.to_excel("OM.xlsx", index=False)
            st.success("Les modifications ont été enregistrées.")

    with col2:
        st.download_button(
            label="📥 Télécharger",
            data=df_modifie.to_csv(index=False).encode("utf-8"),
            file_name="OM.csv",
            mime="text/csv"
        )
elif menu == "🚚 Camions":

    st.title("🚚 Gestion des Camions")

    # Charger le fichier camion.xlsx
    df_camions = pd.read_excel("camion.xlsx")

    # Nettoyer les noms des colonnes
    df_camions.columns = df_camions.columns.str.strip()

    # Ajouter une numérotation si elle n'existe pas
    if "N°" not in df_camions.columns:
        df_camions.insert(0, "N°", range(1, len(df_camions) + 1))

    # Barre de recherche
    recherche = st.text_input(
        "🔍 Rechercher un camion",
        placeholder="Ex : 16-123-456"
    )

    if recherche:
        df_camions = df_camions[
            df_camions.astype(str)
            .apply(lambda x: x.str.contains(recherche, case=False, na=False))
            .any(axis=1)
        ]

    # Tableau modifiable
    df_modifie = st.data_editor(
        df_camions,
        key="camions",
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Enregistrer", key="save_camions"):
            df_modifie.to_excel("camion.xlsx", index=False)
            st.success("Les modifications ont été enregistrées.")

    with col2:
        st.download_button(
            "📥 Télécharger",
            data=df_modifie.to_csv(index=False).encode("utf-8"),
            file_name="camion.csv",
            mime="text/csv"
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

