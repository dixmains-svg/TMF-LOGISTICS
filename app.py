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
# DOSSIER PRINCIPAL
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# FICHIERS
# ============================================================

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
# ARRIÈRE-PLAN
# ============================================================

def charger_arriere_plan():

    if not BACKGROUND_PATH.exists():
        return

    try:

        with open(
            BACKGROUND_PATH,
            "rb"
        ) as image_file:

            encoded_image = base64.b64encode(
                image_file.read()
            ).decode("utf-8")

        st.markdown(
            f"""
            <style>

            .stApp {{

                background-image:

                    linear-gradient(
                        rgba(0, 0, 0, 0.55),
                        rgba(0, 0, 0, 0.55)
                    ),

                    url(
                        "data:image/jpeg;base64,{encoded_image}"
                    );

                background-size: cover;

                background-position: center;

                background-repeat: no-repeat;

                background-attachment: fixed;
            }}

            </style>
            """,
            unsafe_allow_html=True
        )

    except Exception:
        pass


# ============================================================
# PAGE DE CONNEXION
# ============================================================

def page_connexion():

    charger_arriere_plan()

    st.markdown(
        """
        <style>

        .login-container {

            max-width: 500px;

            margin: 70px auto;

            padding: 40px;

            background: rgba(255,255,255,0.96);

            border-radius: 22px;

            box-shadow:
                0 10px 40px rgba(0,0,0,0.35);
        }

        .logo {

            text-align: center;

            margin-bottom: 15px;
        }

        .logo img {

            width: 180px;

            max-width: 80%;

            height: auto;
        }

        .login-title {

            text-align: center;

            font-size: 30px;

            font-weight: 800;

            color: #1f2937;

            margin-bottom: 5px;
        }

        .login-subtitle {

            text-align: center;

            font-size: 16px;

            color: #6b7280;

            margin-bottom: 30px;
        }

        .login-footer {

            text-align: center;

            color: #6b7280;

            font-size: 13px;

            margin-top: 25px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="login-container">',
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
            <div class="logo">

                <img
                    src="data:image/png;base64,{logo_base64}"
                    alt="TMF LOGISTICS"
                >

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="logo"
                 style="font-size:70px;">
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
            "🔐 Se connecter",
            use_container_width=True
        )


        if bouton:

            utilisateur = utilisateur.strip()

            if (
                utilisateur in UTILISATEURS
                and
                UTILISATEURS[utilisateur]
                == mot_de_passe
            ):

                st.session_state.connecte = True

                st.session_state.utilisateur = utilisateur

                st.rerun()

            else:

                st.error(
                    "❌ Nom d'utilisateur ou mot de passe incorrect."
                )


    st.markdown(
        """
        <div class="login-footer">

            🔒 Accès sécurisé<br><br>

            <b>TMF LOGISTICS</b><br>

            Système de Gestion du Transport

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# CONTRÔLE DE CONNEXION
# ============================================================

if not st.session_state.get(
    "connecte",
    False
):

    page_connexion()

    st.stop()


# ============================================================
# DÉCONNEXION
# ============================================================

st.sidebar.divider()

utilisateur_connecte = st.session_state.get(
    "utilisateur",
    ""
)

st.sidebar.markdown(
    f"""
    ### 👤 Utilisateur connecté

    **{utilisateur_connecte}**
    """
)


if st.sidebar.button(
    "🚪 Déconnexion",
    use_container_width=True
):

    st.session_state.clear()

    st.rerun()


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
# VÉRIFICATION DES FICHIERS
# ============================================================

fichiers_pages = {

    "Accueil": PAGE_HOME,

    "Ordres de Mission": PAGE_OM,

    "Camions": PAGE_CAMIONS,

    "Chauffeurs": PAGE_CHAUFFEURS,

    "Clients": PAGE_CLIENTS,

    "Rapports": PAGE_RAPPORTS
}


for nom_page, chemin_page in fichiers_pages.items():

    if not chemin_page.exists():

        st.error(
            f"""
            ❌ La page **{nom_page}** est introuvable.

            Fichier recherché :

            `{chemin_page}`
            """
        )

        st.stop()
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

navigation = st.navigation(pages)

navigation.run()
