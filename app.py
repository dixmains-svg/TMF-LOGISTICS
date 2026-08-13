import streamlit as st

from login import connexion, deconnexion


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TMF LOGISTICS",
    page_icon="🚛",
    layout="wide"
)


# ============================================================
# CONNEXION
# ============================================================

if not connexion():
    st.stop()


# ============================================================
# DÉCONNEXION
# ============================================================

deconnexion()

# ============================================================
# NAVIGATION
# ============================================================

pages = [
    st.Page("app_home.py", title="Accueil", icon="🏠"),
    st.Page(
        "Pages/1_Ordres_de_Mission.py",
        title="Ordres de Mission",
        icon="📋"
    ),
    st.Page(
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

navigation = st.navigation(pages)

navigation.run()
# ============================================================
# APPLICATION
# ============================================================

# Votre code actuel ici

# navigation.run()
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
        st.Page(
            "app_home.py",
            title="Tableau de bord",
            icon="📊"
        )
    ],

    "🚛 Gestion Transport": [
        st.Page(
            "Pages/1_Ordres_de_Mission.py",
            title="Ordres de Mission",
            icon="📋"
        ),

        st.Page(
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
