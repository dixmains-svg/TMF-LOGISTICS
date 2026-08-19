import streamlit as st
from login import afficher_login
from app_home import afficher_home

# Configuration de la page
st.set_page_config(
    page_title="TMF LOGISTICS",
    page_icon="🚛",
    layout="wide",
)

# 1. Vérification : Si l'utilisateur n'est PAS connecté -> Afficher Login
if not st.session_state.get("connecte", False):
    afficher_login()
    st.stop()  # Empêche l'affichage de la suite

# 2. Si l'utilisateur EST connecté -> Afficher la page d'accueil
afficher_home()
