import pandas as pd
import requests
import streamlit as st
from requests_ntlm import HttpNtlmAuth

# Remplacez par les informations réelles de votre serveur Navision
NAV_SERVER = "http://VOTRE_SERVEUR_NAV:7048/NAV/OData/Company('TMF')"
NAV_USER = "domaine\\utilisateur"
NAV_PASSWORD = "votre_mot_de_passe"


@st.cache_data(ttl=300)  # Conserve les données en cache pendant 5 minutes
def charger_donnees_nav(endpoint: str) -> pd.DataFrame:
    """Récupère une table ou une page exposée dans les Web Services OData de Navision."""
    url = f"{NAV_SERVER}/{endpoint}"

    try:
        response = requests.get(
            url, auth=HttpNtlmAuth(NAV_USER, NAV_PASSWORD), timeout=10
        )
        response.raise_for_status()

        data = response.json().get("value", [])
        return pd.DataFrame(data)

    except Exception as e:
        st.error(f"❌ Erreur de connexion à Navision ({endpoint}) : {e}")
        return pd.DataFrame()
