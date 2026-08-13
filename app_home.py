# ============================================================
# NAVIGATION
# ============================================================

pages = {

    "🏠 Accueil": st.Page(
        "app_home.py",
        title="Accueil",
        icon="🏠"
    ),

    "📋 Ordres de Mission": st.Page(
        "Pages/om.py",
        title="Ordres de Mission",
        icon="📋"
    ),

    "🚚 Camions": st.Page(
        "Pages/camions.py",
        title="Camions",
        icon="🚚"
    ),

    "👷 Chauffeurs": st.Page(
        "Pages/chauffeurs.py",
        title="Chauffeurs",
        icon="👷"
    ),

    "👥 Clients": st.Page(
        "Pages/clients.py",
        title="Clients",
        icon="👥"
    ),

    "📊 Rapports": st.Page(
        "Pages/rapports.py",
        title="Rapports",
        icon="📊"
    )
}


navigation = st.navigation(pages)

navigation.run()
