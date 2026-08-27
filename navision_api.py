import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import streamlit as st


def obtenir_config_nav():
    """Récupère les identifiants depuis st.secrets."""
    if "navision" in st.secrets:
        return (
            st.secrets["navision"]["server"],
            st.secrets["navision"]["user"],
            st.secrets["navision"]["password"],
        )
    # Valeurs de secours
    return (
        "http://navisio:7048/DynamicsNAV110/ODataV4/Company('TMF')",
        "h.redjedal",
        "Hr0920@2019*",
    )


@st.cache_data(ttl=300)
def charger_donnees_nav(endpoint: str) -> pd.DataFrame:
    """Interroge l'API OData Navision et retourne un DataFrame."""
    nav_server, nav_user, nav_password = obtenir_config_nav()
    url = f"{nav_server}/{endpoint}"

    try:
        response = requests.get(
            url, auth=HTTPBasicAuth(nav_user, nav_password), timeout=15
        )
        response.raise_for_status()

        data = response.json().get("value", [])
        return pd.DataFrame(data)

    except Exception as e:
        st.error(f"❌ Erreur de connexion Navision ({endpoint}) : {e}")
        return pd.DataFrame()
