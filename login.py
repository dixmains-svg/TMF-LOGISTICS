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
# CHEMINS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

LOGO_PATH = BASE_DIR / "logo.png"

BACKGROUND_PATH = BASE_DIR / "TMF.jpg"


# ============================================================
# CONFIGURATION DE LA PAGE
# ============================================================

st.set_page_config(
    page_title="TMF LOGISTICS - Connexion",
    page_icon="🚛",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ============================================================
# ARRIÈRE-PLAN + STYLE
# ============================================================

def appliquer_style():

    # --------------------------------------------------------
    # Vérifier l'image d'arrière-plan
    # --------------------------------------------------------

    if BACKGROUND_PATH.exists():

        with open(
            BACKGROUND_PATH,
            "rb"
        ) as image_file:

            encoded_image = base64.b64encode(
                image_file.read()
            ).decode("utf-8")

        background_css = f"""
        background-image:
            linear-gradient(
                rgba(0, 0, 0, 0.58),
                rgba(0, 0, 0, 0.58)
            ),
            url("data:image/jpeg;base64,{encoded_image}");
        """

    else:

        background_css = """
        background:
            linear-gradient(
                135deg,
                #0f172a,
                #1e3a5f
            );
        """


    # --------------------------------------------------------
    # CSS
    # --------------------------------------------------------

    st.markdown(
        f"""
        <style>

        /* ==================================================
           APPLICATION
           ================================================== */

        .stApp {{

            {background_css}

            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;

        }}


        /* ==================================================
           CACHER LES ÉLÉMENTS STREAMLIT
           ================================================== */

        #MainMenu {{
            visibility: hidden;
        }}

        header {{
            visibility: hidden;
        }}

        footer {{
            visibility: hidden;
        }}


        /* ==================================================
           CONTENEUR PRINCIPAL
           ================================================== */

        .block-container {{

            padding-top: 3rem;
            padding-bottom: 2rem;

        }}


        /* ==================================================
           PANNEAU DE CONNEXION
           ================================================== */

        .login-box {{

            max-width: 450px;

            margin: 30px auto;

            padding: 40px 45px;

            background:
                rgba(
                    255,
                    255,
                    255,
                    0.96
                );

            border-radius: 22px;

            box-shadow:
                0px 15px 45px
                rgba(
                    0,
                    0,
                    0,
                    0.40
                );

            border:
                1px solid
                rgba(
                    255,
                    255,
                    255,
                    0.5
                );

        }}


        /* ==================================================
           LOGO
           ================================================== */

        .logo-container {{

            text-align: center;

            margin-bottom: 18px;

        }}


        .logo-image {{

            width: 135px;

            height: 135px;

            object-fit: contain;

            border-radius: 18px;

        }}


        /* ==================================================
           LOGO DE SECOURS
           ================================================== */

        .logo-fallback {{

            font-size: 75px;

            text-align: center;

            margin-bottom: 15px;

        }}


        /* ==================================================
           TITRE
           ================================================== */

        .login-title {{

            text-align: center;

            font-size: 34px;

            font-weight: 800;

            color: #172033;

            margin-bottom: 5px;

            letter-spacing: 1px;

        }}


        /* ==================================================
           SOUS-TITRE
           ================================================== */

        .login-subtitle {{

            text-align: center;

            font-size: 16px;

            color: #64748b;

            margin-bottom: 28px;

        }}


        /* ==================================================
           TEXTE SÉCURITÉ
           ================================================== */

        .security-text {{

            text-align: center;

            color: #64748b;

            font-size: 13px;

            margin-top: 20px;

        }}


        /* ==================================================
           FOOTER
           ================================================== */

        .login-footer {{

            text-align: center;

            color: white;

            font-size: 14px;

            margin-top: 20px;

            text-shadow:
                0px 2px 5px
                rgba(
                    0,
                    0,
                    0,
                    0.8
                );

        }}


        /* ==================================================
           BOUTON
           ================================================== */

        div.stButton > button {{

            border-radius: 10px;

            font-weight: 600;

        }}


        /* ==================================================
           MOBILE
           ================================================== */

        @media (max-width: 600px) {{

            .login-box {{

                margin: 15px;

                padding:
                    30px 25px;

            }}

            .login-title {{

                font-size: 28px;

            }}

            .logo-image {{

                width: 110px;

                height: 110px;

            }}

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
    # SI DÉJÀ CONNECTÉ
    # --------------------------------------------------------

    if st.session_state.get(
        "connecte",
        False
    ):

        return True


    # --------------------------------------------------------
    # APPLIQUER LE STYLE
    # --------------------------------------------------------

    appliquer_style()


    # --------------------------------------------------------
    # ESPACE
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


    # ========================================================
    # LOGO
    # ========================================================

    if LOGO_PATH.exists():

        with open(
            LOGO_PATH,
            "rb"
        ) as image_file:

            logo_base64 = base64.b64encode(
                image_file.read()
            ).decode("utf-8")


        st.markdown(
            f"""
            <div class="logo-container">

                <img
                    src="data:image/png;base64,{logo_base64}"
                    class="logo-image"
                >

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="logo-fallback">
                🚛
            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # TITRE
    # ========================================================

    st.markdown(
        """
        <div class="login-title">
            TMF LOGISTICS
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # SOUS-TITRE
    # ========================================================

    st.markdown(
        """
        <div class="login-subtitle">
            Système de Gestion du Transport
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # FORMULAIRE
    # ========================================================

    with st.form(
        "login_form",
        clear_on_submit=False
    ):

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


        # ====================================================
        # VALIDATION
        # ====================================================

        if bouton:

            utilisateur = utilisateur.strip()


            if (
                utilisateur in UTILISATEURS
                and
                UTILISATEURS[utilisateur]
                == mot_de_passe
            ):

                # --------------------------------------------
                # Connexion réussie
                # --------------------------------------------

                st.session_state.connecte = True

                st.session_state.utilisateur = (
                    utilisateur
                )

                # Supprimer ancienne erreur

                if "login_error" in st.session_state:

                    del st.session_state[
                        "login_error"
                    ]


                # Actualiser

                st.rerun()


            else:

                st.session_state.login_error = True


    # ========================================================
    # MESSAGE D'ERREUR
    # ========================================================

    if st.session_state.get(
        "login_error",
        False
    ):

        st.error(
            "❌ Nom d'utilisateur ou mot de passe incorrect."
        )


    # ========================================================
    # MESSAGE SÉCURITÉ
    # ========================================================

    st.markdown(
        """
        <div class="security-text">

            🔒 Accès réservé aux utilisateurs autorisés

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # FIN DU PANNEAU
    # ========================================================

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown(
        """
        <div class="login-footer">

            <b>TMF LOGISTICS</b><br>

            Système de Gestion du Transport<br>

            © 2026

        </div>
        """,
        unsafe_allow_html=True
    )


    return False


# ============================================================
# FONCTION DE DÉCONNEXION
# ============================================================

def deconnexion():

    # --------------------------------------------------------
    # Vérifier si l'utilisateur est connecté
    # --------------------------------------------------------

    if not st.session_state.get(
        "connecte",
        False
    ):

        return


    # ========================================================
    # SIDEBAR
    # ========================================================

    st.sidebar.divider()


    # ========================================================
    # UTILISATEUR CONNECTÉ
    # ========================================================

    utilisateur = st.session_state.get(
        "utilisateur",
        ""
    )


    st.sidebar.markdown(
        f"""
        ### 👤 Utilisateur

        **{utilisateur}**
        """
    )


    # ========================================================
    # BOUTON DÉCONNEXION
    # ========================================================

    if st.sidebar.button(
        "🚪 Déconnexion",
        use_container_width=True
    ):

        # --------------------------------------------
        # Supprimer la session
        # --------------------------------------------

        st.session_state.connecte = False


        if "utilisateur" in st.session_state:

            del st.session_state[
                "utilisateur"
            ]


        if "login_error" in st.session_state:

            del st.session_state[
                "login_error"
            ]


        # --------------------------------------------
        # Retour à la connexion
        # --------------------------------------------

        st.rerun()
