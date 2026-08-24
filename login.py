import base64
from pathlib import Path
import streamlit as st

# ============================================================
# IDENTIFIANTS UTILISATEURS
# ============================================================
UTILISATEURS = {
    "admin": "12345",
    "transport": "tmf2026",
    "direction": "tmf@2026",
}

# CHEMINS DES IMAGES DE FOND ET LOGO
BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "logo.png"
BACKGROUND_PATH = BASE_DIR / "TMF.jpg"


def appliquer_style_connexion():
    """Style CSS spécifique à l'écran de connexion."""
    if BACKGROUND_PATH.exists():
        with open(BACKGROUND_PATH, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        background_css = f"""
        background-image: linear-gradient(rgba(0, 0, 0, 0.58), rgba(0, 0, 0, 0.58)), url("data:image/jpeg;base64,{encoded_image}");
        """
    else:
        background_css = "background: linear-gradient(135deg, #0f172a, #1e3a5f);"

    st.markdown(
        f"""
        <style>
        .stApp {{
            {background_css}
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        #MainMenu, header, footer {{ visibility: hidden; }}
        .login-box {{
            max-width: 450px;
            margin: 30px auto;
            padding: 40px 45px;
            background: rgba(255, 255, 255, 0.96);
            border-radius: 22px;
            box-shadow: 0px 15px 45px rgba(0, 0, 0, 0.40);
        }}
        .logo-container {{ text-align: center; margin-bottom: 18px; }}
        .logo-image {{ width: 135px; height: 135px; object-fit: contain; border-radius: 18px; }}
        .login-title {{ text-align: center; font-size: 34px; font-weight: 800; color: #172033; }}
        .login-subtitle {{ text-align: center; font-size: 16px; color: #64748b; margin-bottom: 28px; }}
        .security-text {{ text-align: center; color: #64748b; font-size: 13px; margin-top: 20px; }}
        .login-footer {{ text-align: center; color: white; font-size: 14px; margin-top: 20px; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def ecran_connexion():
    """Affiche le formulaire de connexion et gère la session utilisateur."""
    if st.session_state.get("connecte", False):
        # Affiche le bouton de déconnexion dans la sidebar quand connecté
        st.sidebar.divider()
        st.sidebar.markdown(f"### 👤 Utilisateur\n**{st.session_state.get('utilisateur', '')}**")
        if st.sidebar.button("🚪 Déconnexion", use_container_width=True):
            st.session_state.connecte = False
            st.session_state.pop("utilisateur", None)
            st.session_state.pop("login_error", None)
            st.rerun()
        return True

    appliquer_style_connexion()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="login-box">', unsafe_allow_html=True)

    if LOGO_PATH.exists():
        with open(LOGO_PATH, "rb") as image_file:
            logo_base64 = base64.b64encode(image_file.read()).decode("utf-8")
        st.markdown(
            f'<div class="logo-container"><img src="data:image/png;base64,{logo_base64}" class="logo-image"></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div style="font-size:75px; text-align:center;">🚛</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="login-title">TMF LOGISTICS</div><div class="login-subtitle">Système de Gestion du Transport</div>',
        unsafe_allow_html=True,
    )

    with st.form("login_form"):
        utilisateur = st.text_input(
            "👤 Nom d'utilisateur", placeholder="Entrez votre nom d'utilisateur"
        )
        mot_de_passe = st.text_input(
            "🔑 Mot de passe",
            type="password",
            placeholder="Entrez votre mot de passe",
        )
        bouton = st.form_submit_button(
            "🔐 SE CONNECTER", use_container_width=True
        )

        if bouton:
            utilisateur = utilisateur.strip()
            if (
                utilisateur in UTILISATEURS
                and UTILISATEURS[utilisateur] == mot_de_passe
            ):
                st.session_state.connecte = True
                st.session_state.utilisateur = utilisateur
                if "login_error" in st.session_state:
                    del st.session_state["login_error"]
                st.rerun()
            else:
                st.session_state.login_error = True

    if st.session_state.get("login_error", False):
        st.error("❌ Nom d'utilisateur ou mot de passe incorrect.")

    st.markdown(
        '<div class="security-text">🔒 Accès réservé aux utilisateurs autorisés</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="login-footer"><b>TMF LOGISTICS</b><br>© 2026</div>',
        unsafe_allow_html=True,
    )

    return False
