import streamlit as st
import pandas as pd
import os

# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TMF LOGISTICS",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# STYLE
# ============================================================

st.markdown("""
<style>

.main-title {
    font-size: 36px;
    font-weight: bold;
}

.subtitle {
    font-size: 18px;
    color: #666;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# LOGO
# ============================================================

try:
    st.logo("https://img.icons8.com/color/96/truck.png")
except Exception:
    pass

# ============================================================
# TITRE
# ============================================================

st.markdown(
    '<div class="main-title">🚛 TMF LOGISTICS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Système de Gestion du Transport et des Ordres de Mission</div>',
    unsafe_allow_html=True
)

st.divider()

# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

def charger_excel(fichier):

    chemin = os.path.join("data", fichier)

    if os.path.exists(chemin):
        try:
            df = pd.read_excel(chemin)
            df.columns = df.columns.astype(str).str.strip()
            return df

        except Exception as e:
            st.error(f"Erreur lors de la lecture de {fichier} : {e}")
            return pd.DataFrame()

    return pd.DataFrame()


df_om = charger_excel("OM.xlsx")
df_camions = charger_excel("camion.xlsx")
df_chauffeurs = charger_excel("chauffeurs.xlsx")
df_clients = charger_excel("clients.xlsx")

# ============================================================
# CALCUL DES INDICATEURS
# ============================================================

nombre_om = len(df_om)

if "Camion" in df_camions.columns:
    nombre_camions = df_camions["Camion"].nunique()
elif "Numero Camion" in df_camions.columns:
    nombre_camions = df_camions["Numero Camion"].nunique()
else:
    nombre_camions = len(df_camions)

nombre_chauffeurs = len(df_chauffeurs)
nombre_clients = len(df_clients)

# ============================================================
# TABLEAU DE BORD
# ============================================================

st.subheader("📊 Tableau de bord")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📋 Ordres de Mission",
        nombre_om
    )

with col2:
    st.metric(
        "🚚 Camions",
        nombre_camions
    )

with col3:
    st.metric(
        "👷 Chauffeurs",
        nombre_chauffeurs
    )

with col4:
    st.metric(
        "👥 Clients",
        nombre_clients
    )

st.divider()

# ============================================================
# INFORMATIONS
# ============================================================

st.subheader("Bienvenue dans TMF LOGISTICS 👋")

st.write(
    """
    Cette application permet de gérer les principales opérations
    de transport de TMF LOGISTICS.
    """
)

col1, col2 = st.columns(2)

with col1:

    st.info(
        """
        📋 **Ordres de Mission**

        Gestion des missions, camions, chauffeurs,
        clients, dates et kilométrages.
        """
    )

with col2:

    st.success(
        """
        🚚 **Gestion du parc**

        Suivi des camions, remorques,
        chauffeurs et affectations.
        """
    )

st.divider()

st.caption("TMF LOGISTICS — Système de Gestion du Transport — Version 2.0")