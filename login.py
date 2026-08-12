import streamlit as st


# ============================================================
# UTILISATEURS
# ============================================================

UTILISATEURS = {
    "admin": "1234",
    "transport": "tmf2026",
    "direction": "tmf@2026"
}


# ============================================================
# FONCTION DE CONNEXION
# ============================================================

def connexion():

    # Déjà connecté
    if st.session_state.get("connecte", False):
        return True

    st.set_page_config(
        page_title="TMF LOGISTICS - Connexion",
        page_icon="🚛",
        layout="centered"
    )

    st.markdown(
        """
        <style>

        .login-title {
            text-align: center;
            font-size: 32px;
            font-weight: bold;
        }

        .login-subtitle {
            text-align: center;
            font-size: 18px;
            margin-bottom: 30px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-title">🚛 TMF LOGISTICS</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-subtitle">'
        'Système de Gestion du Transport'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    with st.form("login_form"):

        utilisateur = st.text_input(
            "👤 Nom d'utilisateur"
        )

        mot_de_passe = st.text_input(
            "🔑 Mot de passe",
            type="password"
        )

        bouton = st.form_submit_button(
            "🔐 Se connecter",
            use_container_width=True
        )

        if bouton:

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

    st.divider()

    st.caption(
        "TMF LOGISTICS — Accès sécurisé"
    )

    return False


# ============================================================
# FONCTION DÉCONNEXION
# ============================================================

def deconnexion():

    st.sidebar.divider()

    utilisateur = st.session_state.get(
        "utilisateur",
        ""
    )

    st.sidebar.write(
        f"👤 Connecté : **{utilisateur}**"
    )

    if st.sidebar.button(
        "🚪 Déconnexion",
        use_container_width=True
    ):

        # Supprimer les informations de connexion
        st.session_state.connecte = False

        if "utilisateur" in st.session_state:
            del st.session_state["utilisateur"]

        # Revenir à la page de connexion
        st.rerun()
