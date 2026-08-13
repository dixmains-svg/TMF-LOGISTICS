import streamlit as st
import base64
from pathlib import Path


# ============================================================
# UTILISATEURS
# ============================================================

UTILISATEURS = {
    "admin": "1234",
    "transport": "tmf2026",
    "direction": "tmf@2026"
}


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TMF LOGISTICS - Connexion",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# IMAGE DE FOND
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

BACKGROUND_PATH = BASE_DIR / "TMF.jpg"


def image_fond():

    if not BACKGROUND_PATH.exists():
        return

    with open(BACKGROUND_PATH, "rb") as image_file:

        encoded_image = base64.b64encode(
            image_file.read()
        ).decode("utf-8")

    st.markdown(
        f"""
        <style>

        /* ==========================================
           ARRIÈRE-PLAN
           ========================================== */

        .stApp {{
            background-image:
                linear-gradient(
                    rgba(0, 0, 0, 0.55),
                    rgba(0, 0, 0, 0.55)
                ),
                url("data:image/jpeg;base64,{encoded_image}");

            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}


        /* ==========================================
           CACHER MENU STREAMLIT
           ========================================== */

        #MainMenu {{
            visibility: hidden;
        }}

        footer {{
            visibility: hidden;
        }}

        header {{
            visibility: hidden;
        }}


        /* ==========================================
           CENTRER LA PAGE
           ========================================== */

        .block-container {{
            padding-top: 5rem;
            padding-bottom: 2rem;
        }}


        /* ==========================================
           PANNEAU DE CONNEXION
           ========================================== */

        .login-box {{

            max-width: 450px;

            margin: auto;

            padding: 40px;

            background: rgba(255, 255, 255, 0.95);

            border-radius: 20px;

            box-shadow:
                0px 10px 40px
                rgba(0, 0, 0, 0.35);

        }}


        /* ==========================================
           TITRE
           ========================================== */

        .login-title {{

            text-align: center;

            font-size: 36px;

            font-weight: 800;

            color: #1f2937;

            margin-bottom: 5px;

        }}


        .login-subtitle {{

            text-align: center;

            font-size: 17px;

            color: #6b7280;

            margin-bottom: 30px;

        }}


        /* ==========================================
           LOGO
           ========================================== */

        .logo {{

            text-align: center;

            font-size: 70px;

            margin-bottom: 10px;

        }}


        /* ==========================================
           MESSAGE BAS DE PAGE
           ========================================== */

        .login-footer {{

            text-align: center;

            color: white;

            font-size: 14px;

            margin-top: 25px;

            text-shadow:
                0px 1px 3px rgba(0,0,0,0.8);

        }}

        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FONCTION DE CONNEXION
# ============================================================

def connexion():

    # --------------------------------------------------------
    # Déjà connecté
    # --------------------------------------------------------

    if st.session_state.get(
        "connecte",
        False
    ):

        return True


    # --------------------------------------------------------
    # Arrière-plan
    # --------------------------------------------------------

    image_fond()


    # --------------------------------------------------------
    # ESPACE HAUT
    # --------------------------------------------------------

    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # PANNEAU
    # --------------------------------------------------------

    st.markdown(
        '<div class="login-box">',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # LOGO
    # --------------------------------------------------------

    st.markdown(
        '<div class="logo">🚛</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # TITRE
    # --------------------------------------------------------

    st.markdown(
        '<div class="login-title">'
        'TMF LOGISTICS'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="login-subtitle">'
        'Système de Gestion du Transport'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # FORMULAIRE
    # --------------------------------------------------------

    with st.form("login_form"):

        utilisateur = st.text_input(
            "👤 Nom d'utilisateur",
            placeholder="Entrez votre nom d'utilisateur"
        )

        mot_de_passe = st.text_input(
            "🔑 Mot de passe",
            type="password",
            placeholder="Entrez votre mot de passe"
        )

        bouton = st.form_submit_button(
            "🔐  SE CONNECTER",
            use_container_width=True
        )


        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if bouton:

            utilisateur = utilisateur.strip()

            if (
                utilisateur in UTILISATEURS
                and
                UTILISATEURS[utilisateur]
                == mot_de_passe
            ):

                st.session_state.connecte = True

                st.session_state.utilisateur = (
                    utilisateur
                )

                st.session_state.login_error = False

                st.rerun()

            else:

                st.session_state.login_error = True


    # --------------------------------------------------------
    # ERREUR
    # --------------------------------------------------------

    if st.session_state.get(
        "login_error",
        False
    ):

        st.error(
            "❌ Nom d'utilisateur ou mot de passe incorrect."
        )


    # --------------------------------------------------------
    # FIN PANNEAU
    # --------------------------------------------------------

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="login-footer">

        🔒 Accès sécurisé<br>

        TMF LOGISTICS © 2026

        </div>
        """,
        unsafe_allow_html=True
    )


    return False


# ============================================================
# FONCTION DÉCONNEXION
# ============================================================

def deconnexion():

    # --------------------------------------------------------
    # Vérifier la connexion
    # --------------------------------------------------------

    if not st.session_state.get(
        "connecte",
        False
    ):

        return


    st.sidebar.divider()


    # --------------------------------------------------------
    # UTILISATEUR CONNECTÉ
    # --------------------------------------------------------

    utilisateur = st.session_state.get(
        "utilisateur",
        ""
    )


    st.sidebar.markdown(
        f"""
        👤 **Utilisateur**

        `{utilisateur}`
        """
    )


    # --------------------------------------------------------
    # BOUTON DÉCONNEXION
    # --------------------------------------------------------

    if st.sidebar.button(
        "🚪 Déconnexion",
        use_container_width=True
    ):

        # Supprimer la session

        st.session_state.connecte = False

        if "utilisateur" in st.session_state:

            del st.session_state[
                "utilisateur"
            ]

        if "login_error" in st.session_state:

            del st.session_state[
                "login_error"
            ]

        # Retour connexion

        st.rerun()
