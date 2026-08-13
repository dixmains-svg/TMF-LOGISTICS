import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TMF LOGISTICS",
    page_icon="🚛",
    layout="wide"
)


# ============================================================
# UTILISATEURS
# ============================================================

UTILISATEURS = {
    "admin": "1234",
    "transport": "tmf2026",
    "direction": "tmf@2026"
}


# ============================================================
# CONNEXION
# ============================================================

if "connecte" not in st.session_state:
    st.session_state.connecte = False


if not st.session_state.connecte:

    st.title("🚛 TMF LOGISTICS")

    st.subheader("Connexion")

    utilisateur = st.text_input(
        "👤 Nom d'utilisateur"
    )

    mot_de_passe = st.text_input(
        "🔑 Mot de passe",
        type="password"
    )

    if st.button(
        "🔐 Se connecter",
        use_container_width=True
    ):

        if (
            utilisateur in UTILISATEURS
            and UTILISATEURS[utilisateur] == mot_de_passe
        ):

            st.session_state.connecte = True
            st.session_state.utilisateur = utilisateur

            st.rerun()

        else:

            st.error(
                "❌ Nom d'utilisateur ou mot de passe incorrect."
            )

    st.stop()


# ============================================================
# NAVIGATION
# ============================================================

home = st.Page(
    "app_home.py",
    title="Tableau de bord",
    icon="🏠"
)

ordres = st.Page(
    "Pages/1_Ordres_de_Mission.py",
    title="Ordres de Mission",
    icon="📋"
)

camions = st.Page(
    "Pages/2_Camions.py",
    title="Camions",
    icon="🚚"
)

chauffeurs = st.Page(
    "Pages/3_Chauffeurs.py",
    title="Chauffeurs",
    icon="👷"
)

clients = st.Page(
    "Pages/4_Clients.py",
    title="Clients",
    icon="👥"
)

rapports = st.Page(
    "Pages/5_Rapports.py",
    title="Rapports",
    icon="📊"
)


navigation = st.navigation(
    [
        home,
        ordres,
        camions,
        chauffeurs,
        clients,
        rapports
    ]
)


# ============================================================
# DÉCONNEXION
# ============================================================

with st.sidebar:

    st.divider()

    st.write(
        f"👤 Connecté : "
        f"**{st.session_state.get('utilisateur', '')}**"
    )

    if st.button(
        "🚪 Se déconnecter",
        use_container_width=True
    ):

        st.session_state.connecte = False

        if "utilisateur" in st.session_state:
            del st.session_state["utilisateur"]

        st.rerun()


# ============================================================
# LANCEMENT
# ============================================================

navigation.run()
