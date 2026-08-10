import streamlit as st


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
# LOGO
# ============================================================

st.logo(
    "https://img.icons8.com/color/96/truck.png"
)


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
            "pages/om.py",
            title="Ordres de Mission",
            icon="📋"
        ),

        st.Page(
            "pages/camions.py",
            title="Camions",
            icon="🚚"
        ),

        st.Page(
            "pages/chauffeurs.py",
            title="Chauffeurs",
            icon="👷"
        ),

        st.Page(
            "pages/clients.py",
            title="Clients",
            icon="👥"
        ),

        st.Page(
            "pages/rapports.py",
            title="Rapports",
            icon="📊"
        )
    ]
}


# ============================================================
# LANCER LA NAVIGATION
# ============================================================

navigation = st.navigation(pages)

navigation.run()
