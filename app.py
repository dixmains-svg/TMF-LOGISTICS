import streamlit as st

st.set_page_config(
    page_title="TMF LOGISTICS",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.logo("https://img.icons8.com/color/96/truck.png")

# ============================================================
# NAVIGATION
# ============================================================

pages = {
    "🏠 Accueil": [
        st.Page(
            "app_home.py",
            title="Tableau de bord",
            icon="📊"
        )
    ],

    "🚛 Gestion Transport": [
        st.Page(
            "pages/1_Ordres_de_Mission.py",
            title="Ordres de Mission",
            icon="📋"
        ),

        st.Page(
            "pages/2_Camions.py",
            title="Camions",
            icon="🚚"
        ),

        st.Page(
            "pages/3_Chauffeurs.py",
            title="Chauffeurs",
            icon="👷"
        ),

        st.Page(
            "pages/4_Clients.py",
            title="Clients",
            icon="👥"
        ),

        st.Page(
            "pages/5_Rapports.py",
            title="Rapports",
            icon="📊"
        )
    ]
}

navigation = st.navigation(pages)

navigation.run()
