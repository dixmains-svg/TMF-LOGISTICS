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

Pages = {
    "🏠 Accueil": [
        st.Pages(
            "app_home.py",
            title="Tableau de bord",
            icon="📊"
        )
    ],

    "🚛 Gestion Transport": [
        st.Pages(
            "Pages/1_Ordres_de_Mission.py",
            title="Ordres de Mission",
            icon="📋"
        ),

        st.Pages(
            "Pages/2_Camions.py",
            title="Camions",
            icon="🚚"
        ),

        st.Page(
            "Pages/3_Chauffeurs.py",
            title="Chauffeurs",
            icon="👷"
        ),

        st.Page(
            "Pages/4_Clients.py",
            title="Clients",
            icon="👥"
        ),

        st.Page(
            "Pages/5_Rapports.py",
            title="Rapports",
            icon="📊"
        )
    ]
}

# ============================================================
# LANCER LA NAVIGATION
# ============================================================

navigation = st.navigation(Pages)

navigation.run()
