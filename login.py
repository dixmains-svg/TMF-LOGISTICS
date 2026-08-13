DECOUCHE V1.4.xlsx
Feuille de calcul
merci de utiliser ce fichier

il m'affiche ça comment le rendre professionnel

pas de liens lorsque on selection l'un des ces page

lundi 09:52
881e2176-51c1-482a-aa2a-1a520c797283.py
Python
code de ce fichier


Texte collé.txt
Document
un ficier de navision:

7d420948-9d75-4de9-b6d9-f7510facf6c7.xlsx
Feuille de calcul

Texte collé(2).txt
Document

Texte collé(3).txt
Document
QUEL EST LE PROBLEME DANS CE CODE

Camions.xlsx
Feuille de calcul
voila le fichier camions

Chauffeurs.xlsx
Feuille de calcul
le fichier chauffeurs

e4d8a352-7077-4ed9-b1a2-74ede2eb5191.xlsx
Feuille de calcul
voici le fichier clients:

886fdeb4-4ce4-4419-aa09-25467902056e.xlsx
Feuille de calcul
voici le fichier ordres de missions:

Texte collé(4).txt
Document

Texte collé(5).txt
Document

Texte collé(6).txt
Document
dans la pages rapport je veux une analyse des données  fichier chauffeur, fichier client fichier chauffeurs en basant sur les donnés fichier om 

Oui. Dans ce cas, le problème n'est probablement plus le code de lecture Excel.

Si OM.xlsx est modifié sur votre PC mais que l'application Streamlit Cloud continue d'afficher les anciennes données, c'est parce que Streamlit Cloud ne peut pas voir automatiquement votre fichier local :

C:\Users\h.redjedal\OneDrive\Desktop\TMF-LOGISTICS\Data\OM.xlsx

Il lit son propre fichier :

/mount/src/tmf-logistics/Data/OM.xlsx

Donc même avec st.cache_data.clear(), il relit l'ancien OM.xlsx présent sur le serveur.
Faisons un test simple

Ajoutez temporairement ceci dans votre page OM :

st.write("📁 Fichier utilisé par l'application :", FICHIER_OM)

if FICHIER_OM.exists():

    st.write(
        "📅 Dernière modification :",
        pd.to_datetime(
            FICHIER_OM.stat().st_mtime,
            unit="s"
        )
    )

    st.write(
        "📦 Taille du fichier :",
        FICHIER_OM.stat().st_size,
        "octets"
    )

Puis comparez avec votre fichier sur le PC.
Si vous voulez que ça fonctionne automatiquement

Votre architecture actuelle est :

Votre PC
   ↓
OM.xlsx
   ↓
GitHub
   ↓
Streamlit Cloud

OM.xlsx ne remonte pas automatiquement de votre PC vers GitHub.

Il faut donc soit :

    Remplacer OM.xlsx sur GitHub après chaque modification ;

    Mettre les fichiers Excel sur un emplacement cloud accessible par l'application ;

    Mettre en place une synchronisation automatique PC → serveur.

Pour votre projet, je vous conseille la 3ᵉ solution, tout en conservant vos fichiers Excel :

TMF-LOGISTICS
│
├── Data
│   ├── OM.xlsx
│   ├── Camions.xlsx
│   ├── Chauffeurs.xlsx
│   └── Clients.xlsx
│
├── Pages
│   ├── 1_Ordres_de_Mission.py
│   ├── 2_Camions.py
│   ├── 3_Chauffeurs.py
│   ├── 4_Clients.py
│   └── 5_Rapports.py
│
└── app.py

Mais avant de modifier encore le code, je veux vérifier une chose : est-ce que votre OM.xlsx que vous modifiez actuellement est bien celui situé dans :

C:\Users\h.redjedal\OneDrive\Desktop\TMF-LOGISTICS\Data\OM.xlsx

et votre application est toujours déployée sur Streamlit Cloud ?

Si oui, je vous donnerai la méthode pour que les modifications de vos 4 fichiers Excel soient récupérées automatiquement par l'application, sans avoir à redéployer à chaque changement.

donne moi la méthode pour que les modifications de vos 4 fichiers Excel soient récupérées automatiquement par l'application

Oui. Pour votre cas, je vous recommande OneDrive/SharePoint comme source des 4 fichiers Excel, avec une synchronisation automatique vers votre application Streamlit.
Architecture recommandée

PC / OneDrive
│
└── TMF-LOGISTICS
    │
    └── Data
        ├── OM.xlsx
        ├── Camions.xlsx
        ├── Chauffeurs.xlsx
        └── Clients.xlsx
              │
              ▼
       Synchronisation automatique
              │
              ▼
       Application Streamlit Cloud
              │
              ▼
        Tableau de bord
        Ordres de Mission
        Camions
        Chauffeurs
        Clients
        Rapports

Ainsi, lorsque vous modifiez OM.xlsx, l'application peut récupérer la nouvelle version sans modifier le code.
⚠️ Point important

Il ne faut plus faire ceci :

FICHIER_OM = BASE_DIR / "Data" / "OM.xlsx"

pour espérer que Streamlit Cloud voie automatiquement votre fichier OneDrive local.

Cette ligne signifie :

    « Lis le fichier qui se trouve dans le serveur Streamlit. »

Elle ne signifie pas :

    « Lis mon fichier OneDrive sur mon PC. »

Méthode que je vous conseille

Pour votre application TMF LOGISTICS, je vous propose :
1. Garder vos 4 fichiers dans OneDrive

Sur votre PC :

C:\Users\h.redjedal\OneDrive\Desktop\TMF-LOGISTICS\Data\

avec :

OM.xlsx
Camions.xlsx
Chauffeurs.xlsx
Clients.xlsx

2. Utiliser Microsoft Graph / SharePoint

L'application Streamlit récupérera les fichiers depuis OneDrive/SharePoint.

Par exemple :

Streamlit Cloud
       ↓
Microsoft Graph
       ↓
OneDrive
       ↓
OM.xlsx
Camions.xlsx
Chauffeurs.xlsx
Clients.xlsx

3. Ajouter un bouton

Dans l'application :

🔄 Actualiser les données

Quand vous cliquez dessus :

OneDrive
   ↓
Téléchargement des 4 fichiers
   ↓
Lecture Excel
   ↓
Actualisation du tableau de bord

On peut également faire une actualisation automatique toutes les X minutes.
Mais il existe une solution encore plus simple

Comme vous avez déjà OneDrive sur votre PC, je vous recommande plutôt :

OneDrive → SharePoint → Microsoft Graph → Streamlit

C'est beaucoup plus adapté à une utilisation professionnelle que de mettre les fichiers Excel directement dans GitHub.

Votre application pourra alors lire :

OM.xlsx
Camions.xlsx
Chauffeurs.xlsx
Clients.xlsx

directement depuis votre espace Microsoft.
Ce que nous allons modifier dans votre application

Au lieu de :

pd.read_excel(
    FICHIER_OM,
    engine="openpyxl"
)

nous aurons quelque chose du principe :

fichier = telecharger_excel_onedrive("OM.xlsx")

df_om = pd.read_excel(
    fichier,
    engine="openpyxl"
)

Et pareil pour :

Camions.xlsx
Chauffeurs.xlsx
Clients.xlsx

Résultat final

Vous modifiez par exemple :

OM.xlsx

à 10h00.

Vous ajoutez 5 nouveaux OM.

Vous enregistrez Excel.

Puis dans votre application :

🔄 Actualiser les données

L'application récupère :

652 OM

puis :

657 OM

sans modifier GitHub et sans redéployer Streamlit.
🔐 Sécurité

Je vous conseille de ne surtout pas mettre votre mot de passe OneDrive dans le code.

Nous utiliserons des secrets Streamlit, par exemple :

AZURE_CLIENT_ID
AZURE_CLIENT_SECRET
AZURE_TENANT_ID

dans les paramètres Secrets de Streamlit Cloud.
Ce que je vous propose pour votre projet

On peut faire cela progressivement, sans refaire toute votre application.

Je peux vous préparer les fichiers suivants :

TMF-LOGISTICS/
│
├── app.py
├── utils/
│   └── onedrive.py
│
├── Pages/
│   ├── 1_Ordres_de_Mission.py
│   ├── 2_Camions.py
│   ├── 3_Chauffeurs.py
│   ├── 4_Clients.py
│   └── 5_Rapports.py
│
├── Data/
│   └── (plus besoin d'y mettre les fichiers sur Streamlit)
│
└── requirements.txt

avec un système centralisé :

get_excel("OM.xlsx")
get_excel("Camions.xlsx")
get_excel("Chauffeurs.xlsx")
get_excel("Clients.xlsx")

Ainsi, toutes vos pages utiliseront automatiquement les données les plus récentes.
Avant de commencer

Il me faut simplement savoir si vos fichiers sont actuellement dans votre OneDrive personnel ou dans OneDrive professionnel / SharePoint de votre entreprise. Les deux sont possibles, mais la configuration Microsoft n'est pas exactement la même.

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
        st.rerun() je veux que ça soit professionnel avec une photo en arriere plan 

Oui. Pour obtenir une page de connexion plus professionnelle, je vous conseille de mettre une image de fond, un panneau de connexion semi-transparent au centre, le logo/titre TMF LOGISTICS et les champs utilisateur/mot de passe.

Placez par exemple votre image ici :

TMF-LOGISTICS/
│
├── app.py
├── login.py
├── TMF.jpg
├── Data/
└── Pages/

Puis remplacez votre code de connexion par celui-ci :

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

Dans app.py

Votre app.py doit ensuite appeler la connexion avant d'afficher l'application :

import streamlit as st

from login import connexion, deconnexion


# ============================================================
# CONNEXION
# ============================================================

if not connexion():

    st.stop()


# ============================================================
# UTILISATEUR CONNECTÉ
# ============================================================

deconnexion()


# ============================================================
# VOTRE APPLICATION
# ============================================================

st.title("🚛 TMF LOGISTICS")

st.write(
    "Bienvenue dans le système de gestion du transport."
)

Vos identifiants actuels
Utilisateur	Mot de passe
admin	1234
transport	tmf2026
direction	tmf@2026

Important : pour une vraie application professionnelle, évitez de conserver les mots de passe directement dans le code. Une fois la page de connexion terminée, je vous conseille de passer ces identifiants dans les Secrets Streamlit, avec éventuellement des droits différents pour admin, transport et direction.

Si votre TMF.jpg est déjà dans le dossier Pages plutôt qu'à la racine du projet, dites-moi son emplacement exact et je vous adapte le chemin.


