import streamlit as st
import pandas as pd
from utils import get_om

st.set_page_config(layout="wide")

st.title("🚛 Gestion des Ordres de Mission")

df = get_om()

st.subheader("Feuille de saisie")

df = st.data_editor(
    df,

    use_container_width=True,

    hide_index=True,

    num_rows="dynamic",

    column_config={

        "Status": st.column_config.SelectboxColumn(
            "Status",
            options=["En cours","Terminé","Annulé"]
        ),

        "Numero Camion": st.column_config.TextColumn(
            "Camion"
        ),

        "Chauffeur": st.column_config.TextColumn(
            "Chauffeur"
        ),

        "Date Depart": st.column_config.DateColumn(
            "Date Départ"
        ),

        "Date de Retour": st.column_config.DateColumn(
            "Date Retour"
        ),

        "Kilometrage Parcouru": st.column_config.NumberColumn(
            "KM",
            format="%d"
        )

    }

)

col1,col2,col3,col4=st.columns(4)

with col1:
    if st.button("💾 Enregistrer"):
        df.to_excel("OM_Modifie.xlsx",index=False)
        st.success("Sauvegardé")

with col2:
    st.button("➕ Nouveau OM")

with col3:
    st.button("🗑 Supprimer")

with col4:
    st.download_button(
        "📥 Télécharger",
        df.to_csv(index=False),
        "OM.csv"
    )
