# ============================================================
# CHEMINS DES PAGES
# ============================================================

PAGE_HOME = BASE_DIR / "app_home.py"

PAGE_OM = BASE_DIR / "Pages" / "om.py"

PAGE_CAMIONS = BASE_DIR / "Pages" / "camions.py"

PAGE_CHAUFFEURS = BASE_DIR / "Pages" / "chauffeurs.py"

PAGE_CLIENTS = BASE_DIR / "Pages" / "clients.py"

PAGE_RAPPORTS = BASE_DIR / "Pages" / "rapports.py"


# ============================================================
# VÉRIFICATION DES PAGES
# ============================================================

pages_fichiers = {
    "Accueil": PAGE_HOME,
    "Ordres de Mission": PAGE_OM,
    "Camions": PAGE_CAMIONS,
    "Chauffeurs": PAGE_CHAUFFEURS,
    "Clients": PAGE_CLIENTS,
    "Rapports": PAGE_RAPPORTS
}


for nom, fichier in pages_fichiers.items():

    if not fichier.exists():

        st.error(
            f"❌ Page introuvable : {nom}\n\n"
            f"Fichier recherché : `{fichier}`"
        )

        st.stop()


# ============================================================
# NAVIGATION
# ============================================================

pages = {

    "🏠 Accueil": st.Page(
        str(PAGE_HOME),
        title="Accueil",
        icon="🏠"
    ),

    "📋 Ordres de Mission": st.Page(
        str(PAGE_OM),
        title="Ordres de Mission",
        icon="📋"
    ),

    "🚚 Camions": st.Page(
        str(PAGE_CAMIONS),
        title="Camions",
        icon="🚚"
    ),

    "👷 Chauffeurs": st.Page(
        str(PAGE_CHAUFFEURS),
        title="Chauffeurs",
        icon="👷"
    ),

    "👥 Clients": st.Page(
        str(PAGE_CLIENTS),
        title="Clients",
        icon="👥"
    ),

    "📊 Rapports": st.Page(
        str(PAGE_RAPPORTS),
        title="Rapports",
        icon="📊"
    )
}


navigation = st.navigation(pages)

navigation.run()
