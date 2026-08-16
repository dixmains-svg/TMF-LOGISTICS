import streamlit as st
import base64
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TMF LOGISTICS - Connexion",
    page_icon="🚛",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CHEMINS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

LOGO_PATH = BASE_DIR / "logo.png"
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
# IMAGE EN BASE64
# ============================================================

def image_base64(chemin):

    if not chemin.exists():
        return None

    with open(chemin, "rb") as fichier:
        return base64.b64encode(
            fichier.read()
        ).decode("utf-8")


# ============================================================
# IMAGES
# ============================================================

logo_base64 = image_base64(LOGO_PATH)
background_base64 = image_base64(BACKGROUND_PATH)


# ============================================================
# ARRIÈRE-PLAN
# ============================================================

if background_base64:

    st.markdown(
        f"""
        <style>

        .stApp {{
            background-image:
                linear-gradient(
                    rgba(0, 0, 0, 0.55),
                    rgba(0, 0, 0, 0.55)
                ),
                url("data:image/jpeg;base64,{background_base64}");

            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# STYLE PAGE DE CONNEXION
# ============================================================

st.markdown(
    """
    <style>

    /* --------------------------------------------------------
       MASQUER LE MENU ET LE FOOTER STREAMLIT
       -------------------------------------------------------- */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }


    /* --------------------------------------------------------
       CONTENEUR PRINCIPAL
       -------------------------------------------------------- */

    .login-container {

        max-width: 520px;

        margin: 40px auto;

        padding: 35px 45px;

        background: rgba(255, 255, 255, 0.94);

        border-radius: 20px;

        box-shadow:
            0 10px 40px
            rgba(0, 0, 0, 0.35);

        text-align: center;
    }


    /* --------------------------------------------------------
       LOGO
       -------------------------------------------------------- */

    .logo-image {

        width: 180px;

        max-width: 100%;

        height: auto;

        margin: 0 auto 15px auto;

        display: block;
    }


    /* --------------------------------------------------------
       TITRE
       -------------------------------------------------------- */

    .login-title {

        font-size: 32px;

        font-weight: 700;

        color: #17365D;

        margin-bottom: 5px;
    }


    /* --------------------------------------------------------
       SOUS-TITRE
       -------------------------------------------------------- */

    .login-subtitle {

        font-size: 17px;

        color: #555;

        margin-bottom: 25px;
    }


    /* --------------------------------------------------------
       INFORMATIONS
       -------------------------------------------------------- */

    .login-info {

        font-size: 13px;

        color: #666;

        margin-top: 20px;
    }


    /* --------------------------------------------------------
       INPUTS
       -------------------------------------------------------- */

    div[data-baseweb="input"] {

        border-radius: 10px;
    }


    /* --------------------------------------------------------
       BOUTON
       -------------------------------------------------------- */

    .stButton > button {

        width: 100%;

        border-radius: 10px;

        height: 48px;

        font-size: 16px;

        font-weight: 600;
    }


    /* --------------------------------------------------------
       FORMULAIRE
       -------------------------------------------------------- */

    div[data-testid="stForm"] {

        border: none !important;

        background: transparent !important;

    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# CONTENEUR
# ============================================================

st.markdown(
    '<div class="login-container">',
    unsafe_allow_html=True
)


# ============================================================
# LOGO
# ============================================================

if logo_base64:

    st.markdown(
        f"""
        <img
            src="data:image/png;base64,{logo_base64}"
            class="logo-image"
        >
        """,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        """
        <div style="
            font-size: 70px;
            margin-bottom: 10px;
        ">
            🚛
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# TITRE
# ============================================================

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


# ============================================================
# FORMULAIRE DE CONNEXION
# ============================================================

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
        "🔐 Se connecter",
        use_container_width=True
    )


# ============================================================
# VÉRIFICATION
# ============================================================

if connexion:

    utilisateur = utilisateur.strip()

    if (
        utilisateur in UTILISATEURS
        and UTILISATEURS[utilisateur] == mot_de_passe
    ):

        st.session_state["connecte"] = True

        st.session_state["utilisateur"] = utilisateur

        st.success(
            "✅ Connexion réussie..."
        )

        st.rerun()

    else:

        st.error(
            "❌ Nom d'utilisateur ou mot de passe incorrect."
        )


# ============================================================
# INFORMATION
# ============================================================

st.markdown(
    """
    <div class="login-info">
        🔒 Accès sécurisé<br>
        TMF LOGISTICS — Système de Gestion du Transport
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FIN CONTENEUR
# ============================================================

st.markdown(
    "</div>",
    unsafe_allow_html=True
)
