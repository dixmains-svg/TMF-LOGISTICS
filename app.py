import streamlit as st
import base64
from pathlib import Path


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
# CHEMINS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

BACKGROUND_PATH = BASE_DIR / "TMF.jpg"


# ============================================================
# UTILISATEURS
# ============================================================

UTILISATEURS = {
    "admin": "1234",
    "transport": "tmf2026",
    "direction": "tmf@2026"
}


# ============================================================
# INITIALISATION SESSION
# ============================================================

if "connecte" not in st.session_state:
    st.session_state.connecte = False

if "utilisateur" not in st.session_state:
    st.session_state.utilisateur = ""


# ============================================================
# ARRIÈRE-PLAN
# ============================================================

def charger_arriere_plan():

    if not BACKGROUND_PATH.exists():
        return ""

    try:

        with open(BACKGROUND_PATH, "rb") as fichier:

            image_base64 = base64.b64encode(
                fichier.read()
            ).decode("utf-8")

        return image_base64

    except Exception:
        return ""


BACKGROUND_BASE64 = charger_arriere_plan()


# ============================================================
# PAGE DE CONNEXION
# ============================================================

def afficher_connexion():

    # --------------------------------------------------------
    # CSS
    # --------------------------------------------------------

    st.markdown(
        """
        <style>

        /* ==================================================
           PAGE COMPLÈTE
           ================================================== */

        .stApp {

            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            background-attachment: fixed;

        }


        /* ==================================================
           COUCHE SOMBRE
           ================================================== */

        .login-overlay {

            position: fixed;

            top: 0;
            left: 0;

            width: 100%;
            height: 100%;

            background:
                linear-gradient(
                    rgba(0, 0, 0, 0.48),
                    rgba(0, 0, 0, 0.48)
                );

            z-index: -1;

        }


        /* ==================================================
           CONTENEUR PRINCIPAL
           ================================================== */

        .login-container {

            max-width: 600px;

            margin-left: auto;
            margin-right: auto;

            padding-top: 70px;

        }


        /* ==================================================
           TITRE
           ================================================== */

        .login-title {

            text-align: center;

            font-size: 72px;

            font-weight: 800;

            color: white;

            letter-spacing: 2px;

            text-shadow:
                2px 2px 8px rgba(0, 0, 0, 0.8);

            margin-bottom: 5px;

        }


        /* ==================================================
           SOUS-TITRE
           ================================================== */

        .login-subtitle {

            text-align: center;

            font-size: 30px;

            font-weight: 400;

            color: white;

            text-shadow:
                2px 2px 6px rgba(0, 0, 0, 0.9);

            margin-bottom: 45px;

        }


        /* ==================================================
           LABELS
           ================================================== */

        div[data-testid="stTextInput"] label {

            color: white !important;

            font-size: 18px !important;

            font-weight: 600 !important;

        }


        /* ==================================================
           CHAMPS
           ================================================== */

        div[data-testid="stTextInput"] input {

            background-color:
                rgba(20, 20, 20, 0.45) !important;

            color: white !important;

            border:
                1px solid rgba(255, 255, 255, 0.65) !important;

            border-radius: 14px !important;

            height: 60px !important;

            font-size: 18px !important;

            padding-left: 18px !important;

        }


        div[data-testid="stTextInput"] input::placeholder {

            color:
                rgba(255, 255, 255, 0.70) !important;

        }


        /* ==================================================
           BOUTON CONNEXION
           ================================================== */

        div.stButton > button {

            width: 100%;

            height: 60px;

            border-radius: 14px;

            border: none;

            background:
                linear-gradient(
                    90deg,
                    #ff6a00,
                    #ff4b00
                );

            color: white;

            font-size: 20px;

            font-weight: 700;

            box-shadow:
                0 5px 15px
                rgba(0, 0, 0, 0.35);

            transition: 0.2s;

        }


        div.stButton > button:hover {

            background:
                linear-gradient(
                    90deg,
                    #ff7b1a,
                    #ff5a0a
                );

            transform: scale(1.01);

        }


        /* ==================================================
           FORMULAIRE
           ================================================== */

        [data-testid="stForm"] {

            background:
                rgba(0, 0, 0, 0.18);

            border:
                1px solid
                rgba(255, 255, 255, 0.20);

            border-radius: 18px;

            padding: 25px;

        }


        /* ==================================================
           MESSAGE SÉCURITÉ
           ================================================== */

        .security-text {

            text-align: center;

            color: white;

            font-size: 18px;

            margin-top: 25px;

            text-shadow:
                1px 1px 5px
                rgba(0, 0, 0, 0.8);

        }


        /* ==================================================
           ERREUR
           ================================================== */

        div[data-testid="stAlert"] {

            border-radius: 12px;

        }

        </style>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # BACKGROUND
    # --------------------------------------------------------

    if BACKGROUND_BASE64:

        st.markdown(
            f"""
            <style>

            .stApp {{

                background-image:
                    linear-gradient(
                        rgba(0, 0, 0, 0.48),
                        rgba(0, 0, 0, 0.48)
                    ),
                    url(
                        "data:image/jpeg;base64,{BACKGROUND_BASE64}"
                    );

                background-size: cover;

                background-position:
                    center center;

                background-repeat: no-repeat;

                background-attachment: fixed;

            }}

            </style>
            """,
            unsafe_allow_html=True
        )

    else:

        st.warning(
            f"⚠️ Image d'arrière-plan introuvable : "
            f"{BACKGROUND_PATH}"
        )


    # --------------------------------------------------------
    # ESPACE
    # --------------------------------------------------------

    st.markdown(
        "<div style='height:30px'></div>",
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # TITRE
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="login-title">
            TMF LOGISTICS
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="login-subtitle">
            Système de Gestion du Transport
        </div>
        """,
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

        connexion = st.form_submit_button(
            "🔐  Se connecter",
            use_container_width=True
        )


        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if connexion:

            utilisateur = utilisateur.strip()

            if (
                utilisateur in UTILISATEURS
                and
                UTILISATEURS[utilisateur] == mot_de_passe
            ):

                st.session_state.connecte = True

                st.session_state.utilisateur = utilisateur

                st.rerun()

            else:

                st.error(
                    "❌ Nom d'utilisateur ou mot de passe incorrect."
                )


    # --------------------------------------------------------
    # SÉCURITÉ
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="security-text">
            🔒 Accès sécurisé
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DÉCONNEXION
# ============================================================

def afficher_deconnexion():

    st.sidebar.divider()

    st.sidebar.markdown(
        f"""
        <div style="
            padding: 10px;
            border-radius: 10px;
            background: rgba(128,128,128,0.10);
        ">

        👤 <b>Utilisateur connecté</b><br>

        <span style="font-size:18px;">
        {st.session_state.utilisateur}
        </span>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.write("")

    if st.sidebar.button(
        "🚪 Déconnexion",
        use_container_width=True
    ):

        st.session_state.connecte = False

        st.session_state.utilisateur = ""

        st.rerun()


# ============================================================
# SI PAS CONNECTÉ
# ============================================================

if not st.session_state.connecte:

    afficher_connexion()

    st.stop()


# ============================================================
# UTILISATEUR CONNECTÉ
# ============================================================

afficher_deconnexion()


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
        "Pages/1_Ordres_de_Mission.py",
        title="Ordres de Mission",
        icon="📋"
    ),

    "🚚 Camions": st.Page(
        "Pages/2_Camions.py",
        title="Camions",
        icon="🚚"
    ),

    "👷 Chauffeurs": st.Page(
        "Pages/3_Chauffeurs.py",
        title="Chauffeurs",
        icon="👷"
    ),

    "👥 Clients": st.Page(
        "Pages/4_Clients.py",
        title="Clients",
        icon="👥"
    ),

    "📊 Rapports": st.Page(
        "Pages/5_Rapports.py",
        title="Rapports",
        icon="📊"
    )
}

navigation = st.navigation(
    pages,
    position="sidebar"
)

navigation.run()
