import base64
from pathlib import Path
import streamlit as st

# ============================================================
# CONFIGURATION DE LA PAGE
# ============================================================

st.set_page_config(
    page_title="TMF LOGISTICS - Connexion",
    page_icon="🚛",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ============================================================
# UTILISATEURS
# ============================================================

UTILISATEURS = {
    "admin": "1234",
    "transport": "tmf2026",
    "direction": "tmf@2026",
}

# ============================================================
# CHEMINS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "logo.png"
BACKGROUND_PATH = BASE_DIR / "TMF.jpg"

# ============================================================
# ARRIÈRE-PLAN + STYLE
# ============================================================


def appliquer_style():
    if BACKGROUND_PATH.exists():
        with open(BACKGROUND_PATH, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

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

        #MainMenu {{ visibility: hidden; }}
        header {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}

        .block-container {{
            padding-top: 3rem;
            padding-bottom: 2rem;
        }}

        .login-box {{
            max-width: 450px;
            margin: 30px auto;
            padding: 40px 45px;
            background: rgba(255, 255, 255, 0.96);
            border-radius: 22px;
            box-shadow: 0px 15px 45px rgba(0, 0, 0, 0.40);
            border: 1px solid rgba(255, 255, 255, 0.5);
        }}

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

        .logo-fallback {{
            font-size: 75px;
            text-align: center;
            margin-bottom: 15px;
        }}

        .login-title {{
            text-align: center;
            font-size: 34px;
            font-weight: 800;
            color: #172033;
            margin-bottom: 5px;
            letter-spacing: 1px;
        }}

        .login-subtitle {{
            text-align: center;
            font-size: 16px;
            color: #64748b;
            margin-bottom: 28px;
        }}

        .security-text {{
            text-align: center;
            color: #64748b;
            font-size: 13px;
            margin-top: 20px;
        }}

        .login-footer {{
            text-align: center;
            color: white;
            font-size: 14px;
            margin-top: 20px;
            text-shadow: 0px 2px 5px rgba(0, 0, 0, 0.8);
        }}

        div.stButton > button {{
            border-radius: 10px;
            font-weight: 600;
        }}

        @media (max-width: 600px) {{
            .login-box {{
                margin: 15px;
                padding: 30px 25px;
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
        unsafe_allow_html=True,
    )


# ============================================================
# FONCTION DE CONNEXION
# ============================================================


def connexion():
    # Si déjà connecté, on sort de la fonction
    if st.session_state.get("connecte", False):
        return True

    appliquer_style()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="login-box">', unsafe_allow_html=True)

    # LOGO
    if LOGO_PATH.exists():
        with open(LOGO_PATH, "rb") as image_file:
            logo_base64 = base64.b64encode(image_file.read()).decode("utf-8")

        st.markdown(
            f"""
            <div class="logo-container">
                <img src="data:image/png;base64,{logo_base64}" class="logo-image">
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="logo-fallback">
                🚛
            </div>
            """,
            unsafe_allow_html=True,
        )

    # TITRES
    st.markdown(
        """
        <div class="login-title">
            TMF LOGISTICS
        </div>
        <div class="login-subtitle">
            Système de Gestion du Transport
        </div>
        """,
        unsafe_allow_html=True,
    )

    # FORMULAIRE
    with st.form("login_form", clear_on_submit=False):
        utilisateur = st.text_input(
            "👤 Nom d'utilisateur",
            placeholder="Entrez votre nom d'utilisateur",
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

    # ERREUR
    if st.session_state.get("login_error", False):
        st.error("❌ Nom d'utilisateur ou mot de passe incorrect.")

    st.markdown(
        """
        <div class="security-text">
            🔒 Accès réservé aux utilisateurs autorisés
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="login-footer">
            <b>TMF LOGISTICS</b><br>
            Système de Gestion du Transport<br>
            © 2026
        </div>
        """,
        unsafe_allow_html=True,
    )

    return False


# ============================================================
# FONCTION DE DÉCONNEXION
# ============================================================


def deconnexion():
    if not st.session_state.get("connecte", False):
        return

    st.sidebar.divider()
    utilisateur = st.session_state.get("utilisateur", "")

    st.sidebar.markdown(
        f"""
        ### 👤 Utilisateur
        **{utilisateur}**
        """
    )

    if st.sidebar.button("🚪 Déconnexion", use_container_width=True):
        st.session_state.connecte = False
        if "utilisateur" in st.session_state:
            del st.session_state["utilisateur"]
        if "login_error" in st.session_state:
            del st.session_state["login_error"]

        st.rerun()


# ============================================================
# FLUX D'EXÉCUTION PRINCIPAL (CRUCIAL POUR QUE ÇA FONCTIONNE)
# ============================================================

# 1. Vérification de la connexion
if not connexion():
    # Bloque l'exécution de l'application si l'utilisateur n'est pas connecté
    st.stop()

# 2. Affichage du bouton de déconnexion dans la barre latérale une fois connecté
deconnexion()

# ============================================================
# CONTENU DE VOTRE APPLICATION (ACCÈS AUTORISÉ)
# ============================================================

st.title("Bienvenue sur l'application TMF LOGISTICS 🚛")
st.success(f"Vous êtes connecté en tant que **{st.session_state.utilisateur}**.")

# Mettez ici le reste du code de votre tableau de bord ou accueil
