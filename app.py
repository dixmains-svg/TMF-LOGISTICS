import streamlit as st
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="HAMIDOUCHE REDJDAL | CV",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PHOTO
# ============================================================

PHOTO = Path("photo.jpg")

# ============================================================
# SELECTION DE LA LANGUE
# ============================================================

langue_choisie = st.sidebar.selectbox(
    "🌐 Langue / Language",
    ["Français", "English"]
)

# ============================================================
# BASE DE DONNÉES MULTILINGUE
# ============================================================

TEXTES = {
    "Français": {
        "fonction": "Planificateur et Superviseur Logistique",
        "nationalite": "Algérienne",
        "situation": "Marié",
        "service_national": "Dégagé",
        "nav_title": "NAVIGATION",
        "nav": [
            "🏠 Accueil",
            "👤 Profil",
            "💼 Expériences",
            "🎓 Diplômes & Formations",
            "🛠️ Compétences",
            "🌐 Langues",
            "⭐ Centres d'intérêt",
            "📞 Contact",
        ],
        "sidebar_domains": """
**DOMAINES PROFESSIONNELS**

🚚 Transport
📦 Logistique
📊 Planification
👥 Supervision
📈 Optimisation
""",
        "profil": (
            "Dynamique, sérieux et ayant de bonnes compétences relationnelles, "
            "avec 9 ans d'expérience dans le domaine de la logistique. "
            "Très à l'aise avec les outils informatiques, je souhaite mettre "
            "mes compétences et ma motivation au service d'une entreprise "
            "et relever de nouveaux défis professionnels."
        ),
        "sections": {
            "profil": "Profil professionnel",
            "expertise": "Domaines d'expertise",
            "actuel": "Expérience actuelle",
            "identite": "👤 Identité",
            "infos_pro": "📋 Informations professionnelles",
            "exp": "Expériences professionnelles",
            "form": "Diplômes & Formations",
            "comp": "Compétences professionnelles",
            "langues": "Langues",
            "interets": "Centres d'intérêt",
            "contact": "Contact"
        },
        "labels": {
            "nom": "Nom",
            "nationalite": "Nationalité",
            "situation": "Situation familiale",
            "fonction": "Fonction",
            "adresse": "Adresse",
            "service": "Service national",
            "stat_exp": "Expérience",
            "stat_postes": "Postes",
            "stat_form": "Formations",
            "stat_langues": "Langues",
            "missions": "Principales missions",
            "tel": "Téléphone",
            "email": "Email",
            "adresse_title": "Adresse",
            "degree_subtitle": "Master 2 en Recherche Opérationnelle",
            "sub_keywords": "Logistique &nbsp; • &nbsp; Transport &nbsp; • &nbsp; Planification &nbsp; • &nbsp; Supervision &nbsp; • &nbsp; Optimisation",
            "photo_missing": "Photo non trouvée"
        },
        "domaines": [
            ("🚚", "Transport", "Organisation, suivi et supervision des opérations de transport."),
            ("📦", "Logistique", "Gestion des flux, des opérations logistiques et des ressources."),
            ("📅", "Planification", "Élaboration des programmes et planification des ressources humaines et matérielles."),
            ("👥", "Supervision", "Suivi des équipes et contrôle du bon déroulement des opérations."),
            ("📈", "Optimisation", "Recherche de solutions permettant d'améliorer les coûts, les délais et l'utilisation des ressources."),
            ("📊", "Reporting", "Élaboration et suivi des reportings d'activité pour faciliter le pilotage."),
            ("🎯", "KPI", "Mise en place et suivi des indicateurs de performance liés à l'activité."),
            ("🤝", "Coordination", "Coordination entre les différents services et intervenants afin d'assurer la continuité des opérations."),
            ("⚙️", "Gestion des ressources", "Préparation, affectation et utilisation optimale des ressources disponibles."),
        ],
        "experiences": [
            {
                "poste": "Superviseur techno-commercial",
                "periode": "01/2024 - À ce jour",
                "entreprise": "SPA TMF Logistics",
                "missions": [
                    "Analyser les besoins des clients.",
                    "Établir des reportings d'activité quotidiens, mensuels et annuels.",
                    "Apporter des solutions pertinentes et adaptées.",
                    "Suivre le bon déroulement de l'activité.",
                    "Contrôler les flux entrants et sortants de la zone d'entreposage.",
                ],
            },
            {
                "poste": "Superviseur exploitation",
                "periode": "06/2022 - 01/2024",
                "entreprise": "SPA TMF Logistics",
                "missions": [
                    "Piloter et superviser les opérations de transport.",
                    "Suivre le bon déroulement de l'activité.",
                    "Contrôler les flux entrants et sortants de la zone d'entreposage.",
                    "Planifier, organiser et contrôler l'activité d'une équipe.",
                    "Réceptionner les commandes des clients et veiller à leur satisfaction.",
                    "Assurer la bonne réalisation du programme et le réadapter en fonction des imprévus.",
                ],
            },
            {
                "poste": "Chargé de la planification",
                "periode": "02/2020 - 06/2022",
                "entreprise": "SPA TMF Logistics",
                "missions": [
                    "Préparer la disponibilité des ressources humaines et matérielles.",
                    "Planifier les commandes de chaque client.",
                    "Élaborer les reportings et les KPI liés à l'activité.",
                    "Réceptionner et traiter les demandes du service commercial.",
                    "Optimiser les ressources logistiques en termes de coûts et de délais.",
                    "Administrer et générer les ordres de mission.",
                    "Assurer la bonne réalisation du programme et le réadapter en fonction des imprévus.",
                ],
            },
            {
                "poste": "Coordinateur logistique",
                "periode": "02/2019 - 02/2020",
                "entreprise": "SPA TMF Logistics",
                "missions": [
                    "Élaborer et maintenir une parfaite coordination avec les autres services.",
                    "Élaborer et mettre en place des indicateurs de suivi de transport.",
                    "Gérer les partenariats avec les prestataires de transport.",
                    "Piloter et contrôler les performances des activités à court, moyen et long terme.",
                    "Veiller au respect des procédures de travail et de la réglementation.",
                ],
            },
            {
                "poste": "Chargé de la programmation",
                "periode": "04/2016 - 10/2018",
                "entreprise": "SPA TMF Logistics",
                "missions": [
                    "Exécuter et suivre régulièrement la programmation et l'utilisation des ressources.",
                    "Établir un planning optimal en optimisant les coûts et les délais.",
                    "Anticiper les situations imprévues et prendre rapidement les décisions correctives.",
                    "Étudier la faisabilité d'une mission avant d'affecter les ressources.",
                ],
            },
        ],
        "formations": [
            {
                "annee": "2021",
                "titre": "Formation en Transport international des marchandises",
                "organisme": "Chambre algérienne de commerce et d'industrie, Alger - Algérie",
            },
            {
                "annee": "2020",
                "titre": "Formation en Planification et optimisation logistique",
                "organisme": "Institut international de Management, Bejaia - Algérie",
            },
            {
                "annee": "2019",
                "titre": "Formation en Logistique et transport",
                "organisme": "Institut international de management, Bejaia - Algérie",
            },
            {
                "annee": "2019",
                "titre": "Formation en Gestion des temps et des priorités",
                "organisme": "Institut international de management, Bejaia - Algérie",
            },
            {
                "annee": "2018",
                "titre": "Formation en Gestion des opérations de transport",
                "organisme": "Institut international de management, Bejaia - Algérie",
            },
            {
                "annee": "2015",
                "titre": "Master 2 en Recherche opérationnelle",
                "organisme": "Option : Fiabilité et évaluation des performances des réseaux. Université Abderrahmane Mira, Bejaia - Algérie",
            },
            {
                "annee": "2012",
                "titre": "Licence en Recherche opérationnelle",
                "organisme": "Option : Aide à la décision. Université Abderrahmane Mira, Bejaia - Algérie",
            },
            {
                "annee": "2012",
                "titre": "Attestation de stage en gestion portuaire",
                "organisme": "Entreprise portuaire de Bejaia, Bejaia - Algérie",
            },
            {
                "annee": "2008",
                "titre": "Diplôme Baccalauréat",
                "organisme": "Option : Science de la nature et de la vie. Lycée Mohamed Boudiaf, Tazmalt - Algérie",
            },
        ],
        "competences": [
            "Maîtrise du Pack Office : Excel, Word, PowerPoint et Outlook.",
            "Maîtrise de Matlab, LaTeX, Photoshop, Illustrator et InDesign.",
            "Langages de programmation : HTML, Java, Delphi et C++.",
            "Planification et optimisation des ressources.",
            "Gestion des opérations de transport.",
            "Supervision des opérations de transport.",
            "Élaboration et mise en place des indicateurs de suivi de transport.",
            "Élaboration des reportings et KPI liés à l'activité.",
            "Gestion des partenariats avec les prestataires de transport.",
            "Coordination avec les autres services.",
            "Gestion des ressources humaines et matérielles.",
            "Gestion et génération des ordres de mission.",
        ],
        "langues": [
            ("Kabyle", "Maîtrise très bien"),
            ("Arabe", "Maîtrise très bien"),
            ("Français", "Maîtrise bien"),
            ("Anglais", "Maîtrise moyenne"),
        ],
        "interets": [
            ("✈️", "Voyage"),
            ("⚽", "Passion pour le sport"),
            ("🤝", "Activités associatives"),
            ("🎬", "Cinéma"),
            ("🎨", "Arts créatifs"),
            ("💻", "Informatique"),
        ]
    },
    "English": {
        "fonction": "Logistics Planner & Supervisor",
        "nationalite": "Algerian",
        "situation": "Married",
        "service_national": "Exempted",
        "nav_title": "NAVIGATION",
        "nav": [
            "🏠 Home",
            "👤 Profile",
            "💼 Experience",
            "🎓 Education & Training",
            "🛠️ Skills",
            "🌐 Languages",
            "⭐ Interests",
            "📞 Contact",
        ],
        "sidebar_domains": """
**PROFESSIONAL FIELDS**

🚚 Transport
📦 Logistics
📊 Planning
👥 Supervision
📈 Optimization
""",
        "profil": (
            "Dynamic, reliable, and possessing strong interpersonal skills, "
            "with 9 years of experience in the field of logistics. "
            "Highly proficient with IT tools, I aim to apply "
            "my skills and motivation to serve a growing company "
            "and take on new professional challenges."
        ),
        "sections": {
            "profil": "Professional Profile",
            "expertise": "Fields of Expertise",
            "actuel": "Current Position",
            "identite": "👤 Identity",
            "infos_pro": "📋 Professional Information",
            "exp": "Work Experience",
            "form": "Education & Training",
            "comp": "Professional Skills",
            "langues": "Languages",
            "interets": "Interests",
            "contact": "Contact"
        },
        "labels": {
            "nom": "Name",
            "nationalite": "Nationality",
            "situation": "Marital Status",
            "fonction": "Position",
            "adresse": "Address",
            "service": "Military Service",
            "stat_exp": "Experience",
            "stat_postes": "Positions",
            "stat_form": "Training",
            "stat_langues": "Languages",
            "missions": "Key Responsibilities",
            "tel": "Phone",
            "email": "Email",
            "adresse_title": "Address",
            "degree_subtitle": "Master 2 in Operational Research",
            "sub_keywords": "Logistics &nbsp; • &nbsp; Transport &nbsp; • &nbsp; Planning &nbsp; • &nbsp; Supervision &nbsp; • &nbsp; Optimization",
            "photo_missing": "Photo not found"
        },
        "domaines": [
            ("🚚", "Transport", "Organization, tracking, and supervision of transport operations."),
            ("📦", "Logistics", "Flow management, logistics operations, and resource allocation."),
            ("📅", "Planning", "Scheduling operations and planning human and material resources."),
            ("👥", "Supervision", "Team management and operational control."),
            ("📈", "Optimization", "Cost reduction, lead time improvement, and optimal resource usage."),
            ("📊", "Reporting", "Developing and tracking activity reports for management."),
            ("🎯", "KPI", "Implementation and monitoring of activity performance indicators."),
            ("🤝", "Coordination", "Inter-departmental coordination ensuring seamless operations."),
            ("⚙️", "Resource Management", "Preparation, assignment, and optimal allocation of resources."),
        ],
        "experiences": [
            {
                "poste": "Technical & Commercial Supervisor",
                "periode": "01/2024 - Present",
                "entreprise": "SPA TMF Logistics",
                "missions": [
                    "Analyze customer requirements and needs.",
                    "Establish daily, monthly, and annual activity reports.",
                    "Provide relevant and adapted logistics solutions.",
                    "Monitor ongoing operational activities.",
                    "Control inbound and outbound flows within storage areas.",
                ],
            },
            {
                "poste": "Operations Supervisor",
                "periode": "06/2022 - 01/2024",
                "entreprise": "SPA TMF Logistics",
                "missions": [
                    "Lead and supervise transport operations.",
                    "Monitor operational smooth execution.",
                    "Control inbound and outbound warehouse flows.",
                    "Plan, organize, and control team tasks.",
                    "Receive customer orders and ensure customer satisfaction.",
                    "Ensure program delivery and adapt to contingencies.",
                ],
            },
            {
                "poste": "Planning Officer",
                "periode": "02/2020 - 06/2022",
                "entreprise": "SPA TMF Logistics",
                "missions": [
                    "Prepare human and material resource availability.",
                    "Schedule order execution per customer.",
                    "Develop activity-related reporting and KPIs.",
                    "Receive and process commercial requests.",
                    "Optimize logistics resources regarding cost and lead times.",
                    "Issue and manage mission orders.",
                    "Adjust operational schedules in case of unforeseen events.",
                ],
            },
            {
                "poste": "Logistics Coordinator",
                "periode": "02/2019 - 02/2020",
                "entreprise": "SPA TMF Logistics",
                "missions": [
                    "Develop and maintain seamless coordination with other departments.",
                    "Design and deploy transport monitoring indicators.",
                    "Manage partnerships with transport service providers.",
                    "Monitor short, medium, and long-term activity performance.",
                    "Ensure compliance with work procedures and safety regulations.",
                ],
            },
            {
                "poste": "Scheduling Officer",
                "periode": "04/2016 - 10/2018",
                "entreprise": "SPA TMF Logistics",
                "missions": [
                    "Execute and regularly monitor resource scheduling and usage.",
                    "Establish optimal schedules balancing cost and delivery times.",
                    "Anticipate unexpected situations and take prompt corrective decisions.",
                    "Analyze mission feasibility prior to assigning resources.",
                ],
            },
        ],
        "formations": [
            {
                "annee": "2021",
                "titre": "Training in International Freight Transport",
                "organisme": "Algerian Chamber of Commerce and Industry, Algiers - Algeria",
            },
            {
                "annee": "2020",
                "titre": "Training in Logistics Planning & Optimization",
                "organisme": "International Management Institute, Bejaia - Algeria",
            },
            {
                "annee": "2019",
                "titre": "Training in Logistics & Transport",
                "organisme": "International Management Institute, Bejaia - Algeria",
            },
            {
                "annee": "2019",
                "titre": "Training in Time & Priority Management",
                "organisme": "International Management Institute, Bejaia - Algeria",
            },
            {
                "annee": "2018",
                "titre": "Training in Transport Operations Management",
                "organisme": "International Management Institute, Bejaia - Algeria",
            },
            {
                "annee": "2015",
                "titre": "Master's Degree (M2) in Operational Research",
                "organisme": "Option: Network Reliability and Performance Evaluation. Abderrahmane Mira University, Bejaia - Algeria",
            },
            {
                "annee": "2012",
                "titre": "Bachelor's Degree in Operational Research",
                "organisme": "Option: Decision Support Systems. Abderrahmane Mira University, Bejaia - Algeria",
            },
            {
                "annee": "2012",
                "titre": "Port Management Internship Certificate",
                "organisme": "Bejaia Port Authority, Bejaia - Algeria",
            },
            {
                "annee": "2008",
                "titre": "High School Diploma (Baccalaureate)",
                "organisme": "Option: Natural Sciences and Life. Mohamed Boudiaf High School, Tazmalt - Algeria",
            },
        ],
        "competences": [
            "Proficient in MS Office: Excel, Word, PowerPoint, and Outlook.",
            "Proficient in Matlab, LaTeX, Photoshop, Illustrator, and InDesign.",
            "Programming Languages: HTML, Java, Delphi, and C++.",
            "Resource planning and optimization.",
            "Management of transport operations.",
            "Supervision of transport operations.",
            "Development and implementation of transport tracking indicators.",
            "Development of activity-related reports and KPIs.",
            "Partnership management with transport providers.",
            "Inter-departmental coordination.",
            "Management of human and material resources.",
            "Administration and generation of mission orders.",
        ],
        "langues": [
            ("Kabyle", "Native / Excellent"),
            ("Arabic", "Native / Excellent"),
            ("French", "Fluent"),
            ("English", "Intermediate"),
        ],
        "interets": [
            ("✈️", "Travel"),
            ("⚽", "Sports Passion"),
            ("🤝", "Community Activities"),
            ("🎬", "Cinema"),
            ("🎨", "Creative Arts"),
            ("💻", "IT & Technology"),
        ]
    }
}

# Variable active selon la langue choisie
t = TEXTES[langue_choisie]

# Informations fixes
nom = "HAMIDOUCHE REDJDAL"
telephone = "00213775 73 79 30"
email = "hamidoucheredjdal@yahoo.fr"
adresse = "Tazmalt 06039, wilaya de Bejaia"

# ============================================================
# STYLE CSS
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background-color: #f4f7fb;
}

.block-container {
    max-width: 1200px;
    padding-top: 25px;
    padding-bottom: 50px;
}

/* HEADER */
.cv-header {
    background: linear-gradient(135deg, #102a43, #1f5f8b);
    color: white;
    padding: 40px 45px;
    border-radius: 22px;
    margin-bottom: 30px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.15);
    min-height: 260px;
}

.cv-name {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 12px;
}

.cv-title {
    font-size: 23px;
    font-weight: 600;
    margin-bottom: 18px;
}

.cv-subtitle {
    font-size: 16px;
    line-height: 1.8;
}

/* TITRES */
.section-title {
    color: #102a43;
    font-size: 27px;
    font-weight: 800;
    margin-top: 30px;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 3px solid #1f5f8b;
}

/* CARTES */
.card {
    background-color: white;
    border-radius: 17px;
    padding: 25px;
    margin-bottom: 18px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.06);
}

.card-title {
    color: #102a43;
    font-size: 19px;
    font-weight: 800;
    margin-bottom: 10px;
}

.card-text {
    color: #52606d;
    font-size: 16px;
    line-height: 1.9;
}

/* EXPERIENCES */
.experience-card {
    background-color: white;
    border-left: 5px solid #1f5f8b;
    border-radius: 17px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.06);
}

.experience-position {
    color: #102a43;
    font-size: 21px;
    font-weight: 800;
}

.experience-company {
    color: #1f5f8b;
    font-size: 16px;
    font-weight: 700;
    margin-top: 6px;
}

.experience-date {
    color: #829ab1;
    font-size: 14px;
    margin-top: 5px;
    margin-bottom: 18px;
}

.mission {
    color: #52606d;
    line-height: 1.7;
    margin-top: 9px;
}

/* FORMATIONS */
.education-card {
    background-color: white;
    border-radius: 17px;
    padding: 22px;
    margin-bottom: 15px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.06);
}

.year {
    display: inline-block;
    background-color: #102a43;
    color: white;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 10px;
}

.education-title {
    color: #102a43;
    font-size: 17px;
    font-weight: 800;
}

.education-school {
    color: #627d98;
    font-size: 14px;
    margin-top: 7px;
    line-height: 1.6;
}

/* COMPETENCES */
.skill-card {
    background-color: white;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    color: #334e68;
    line-height: 1.6;
}

/* CONTACT */
.contact-card {
    background-color: white;
    border-radius: 17px;
    padding: 25px;
    text-align: center;
    min-height: 145px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.06);
}

.contact-icon {
    font-size: 32px;
    margin-bottom: 8px;
}

.contact-title {
    color: #102a43;
    font-weight: 800;
    margin-bottom: 8px;
}

.contact-value {
    color: #52606d;
    font-size: 14px;
    line-height: 1.6;
}

/* SIDEBAR ET FIX SELECTBOX */
[data-testid="stSidebar"] {
    background-color: #102a43;
}

[data-testid="stSidebar"] * {
    color: white;
}

/* Fix du texte pour le champ de selection de langue */
[data-testid="stSidebar"] div[data-baseweb="select"] div {
    color: #102a43 !important;
    font-weight: 600;
}

div[data-baseweb="popover"] ul li span {
    color: #102a43 !important;
}

[data-testid="stSidebar"] div[data-baseweb="select"] svg {
    fill: #102a43 !important;
}

.footer {
    text-align: center;
    color: #829ab1;
    font-size: 13px;
    margin-top: 50px;
    padding-top: 25px;
    border-top: 1px solid #d9e2ec;
}

@media (max-width: 768px) {
    .cv-header { padding: 30px 25px; }
    .cv-name { font-size: 30px; }
    .cv-title { font-size: 18px; }
    .cv-subtitle { font-size: 14px; }
    .section-title { font-size: 23px; }
}

</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# HEADER AVEC PHOTO
# ============================================================

col_photo, col_header = st.columns([1, 4])

with col_photo:
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #102a43, #1f5f8b); padding: 25px; border-radius: 22px; height: 100%; text-align: center;">
        """,
        unsafe_allow_html=True,
    )

    if PHOTO.exists():
        st.image(str(PHOTO), width=180)
    else:
        st.markdown(
            """
            <div style="font-size:100px; padding:30px;">👤</div>
            """,
            unsafe_allow_html=True,
        )
        st.warning(t["labels"]["photo_missing"])

    st.markdown("</div>", unsafe_allow_html=True)


with col_header:
    st.markdown(
        f"""
        <div class="cv-header">
            <div class="cv-name">{nom}</div>
            <div class="cv-title">🚚 {t['fonction']}</div>
            <div class="cv-subtitle">
                {t['labels']['degree_subtitle']}
                <br><br>
                {t['labels']['sub_keywords']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    f"""
    <div style="text-align:center; padding:15px 5px 20px 5px;">
        <div style="font-size:45px;">🚚</div>
        <div style="font-size:20px; font-weight:800;">{nom}</div>
        <div style="font-size:13px; margin-top:6px;">CURRICULUM VITAE</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("---")

page = st.sidebar.radio(t["nav_title"], t["nav"])

st.sidebar.markdown("---")
st.sidebar.markdown(t["sidebar_domains"])

# ============================================================
# PAGES DE L'APPLICATION
# ============================================================

# --- ACCUEIL ---
if page in ["🏠 Accueil", "🏠 Home"]:

    st.markdown(
        f"<div class='section-title'>{t['sections']['profil']}</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="card">
            <p class="card-text">{t['profil']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Indicateurs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(t["labels"]["stat_exp"], "9 ans / yrs")
    with col2:
        st.metric(t["labels"]["stat_postes"], len(t["experiences"]))
    with col3:
        st.metric(t["labels"]["stat_form"], len(t["formations"]))
    with col4:
        st.metric(t["labels"]["stat_langues"], len(t["langues"]))

    # Domaines d'expertise
    st.markdown(
        f"<div class='section-title'>{t['sections']['expertise']}</div>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    for index, (icone, titre, definition) in enumerate(t["domaines"]):
        if index % 3 == 0:
            colonne = col1
        elif index % 3 == 1:
            colonne = col2
        else:
            colonne = col3

        with colonne:
            st.markdown(
                f"""
                <div class="card" style="min-height: 190px;">
                    <div style="font-size: 34px; margin-bottom: 10px;">{icone}</div>
                    <div class="card-title">{titre}</div>
                    <div style="color:#52606d; font-size:14px; line-height:1.7; margin-top:10px;">
                        {definition}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Expérience actuelle
    st.markdown(
        f"<div class='section-title'>{t['sections']['actuel']}</div>",
        unsafe_allow_html=True,
    )

    current = t["experiences"][0]
    st.markdown(
        f"""
        <div class="experience-card">
            <div class="experience-position">{current["poste"]}</div>
            <div class="experience-company">🏢 {current["entreprise"]}</div>
            <div class="experience-date">📅 {current["periode"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- PROFIL ---
elif page in ["👤 Profil", "👤 Profile"]:
    st.markdown(
        f"<div class='section-title'>{t['sections']['profil']}</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="card">
            <p class="card-text">{t['profil']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"<div class='section-title'>{t['sections']['identite']}</div>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">{t['sections']['identite']}</div>
                <p><strong>{t['labels']['nom']} :</strong><br>{nom}</p>
                <p><strong>{t['labels']['nationalite']} :</strong><br>{t['nationalite']}</p>
                <p><strong>{t['labels']['situation']} :</strong><br>{t['situation']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">{t['sections']['infos_pro']}</div>
                <p><strong>{t['labels']['fonction']} :</strong><br>{t['fonction']}</p>
                <p><strong>{t['labels']['adresse']} :</strong><br>{adresse}</p>
                <p><strong>{t['labels']['service']} :</strong><br>{t['service_national']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# --- EXPERIENCES ---
elif page in ["💼 Expériences", "💼 Experience"]:

    st.markdown(
        f"<div class='section-title'>{t['sections']['exp']}</div>",
        unsafe_allow_html=True,
    )

    for exp in t["experiences"]:
        st.markdown(
            f"""
            <div class="experience-card">
                <div class="experience-position">{exp["poste"]}</div>
                <div class="experience-company">🏢 {exp["entreprise"]}</div>
                <div class="experience-date">📅 {exp["periode"]}</div>
                <strong>{t['labels']['missions']}</strong>
            """,
            unsafe_allow_html=True,
        )

        for mission in exp["missions"]:
            st.markdown(
                f"""
                <div class="mission">✓ {mission}</div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

# --- DIPLOMES ET FORMATIONS ---
elif page in ["🎓 Diplômes & Formations", "🎓 Education & Training"]:

    st.markdown(
        f"<div class='section-title'>{t['sections']['form']}</div>",
        unsafe_allow_html=True,
    )

    for formation in t["formations"]:
        st.markdown(
            f"""
            <div class="education-card">
                <div class="year">{formation["annee"]}</div>
                <div class="education-title">{formation["titre"]}</div>
                <div class="education-school">🏫 {formation["organisme"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# --- COMPETENCES ---
elif page in ["🛠️ Compétences", "🛠️ Skills"]:

    st.markdown(
        f"<div class='section-title'>{t['sections']['comp']}</div>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    for index, competence in enumerate(t["competences"]):
        colonne = col1 if index % 2 == 0 else col2
        with colonne:
            st.markdown(
                f"""
                <div class="skill-card">✓ {competence}</div>
                """,
                unsafe_allow_html=True,
            )

# --- LANGUES ---
elif page in ["🌐 Langues", "🌐 Languages"]:

    st.markdown(
        f"<div class='section-title'>{t['sections']['langues']}</div>",
        unsafe_allow_html=True,
    )

    columns = st.columns(4)

    for index, langue in enumerate(t["langues"]):
        with columns[index]:
            st.markdown(
                f"""
                <div class="card" style="text-align:center;">
                    <div style="font-size:38px;">🌐</div>
                    <div class="card-title">{langue[0]}</div>
                    <div style="color:#1f5f8b; font-weight:700; margin-top:10px;">
                        {langue[1]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# --- CENTRES D'INTERET ---
elif page in ["⭐ Centres d'intérêt", "⭐ Interests"]:

    st.markdown(
        f"<div class='section-title'>{t['sections']['interets']}</div>",
        unsafe_allow_html=True,
    )

    columns = st.columns(3)

    for index, item in enumerate(t["interets"]):
        icone, titre = item[0], item[1]

        with columns[index % 3]:
            st.markdown(
                f"""
                <div class="card" style="text-align:center;">
                    <div style="font-size:40px;">{icone}</div>
                    <div class="card-title">{titre}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# --- CONTACT ---
elif page in ["📞 Contact"]:

    st.markdown(
        f"<div class='section-title'>{t['sections']['contact']}</div>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="contact-card">
                <div class="contact-icon">📱</div>
                <div class="contact-title">{t['labels']['tel']}</div>
                <div class="contact-value">{telephone}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="contact-card">
                <div class="contact-icon">📧</div>
                <div class="contact-title">{t['labels']['email']}</div>
                <div class="contact-value">{email}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="contact-card">
                <div class="contact-icon">📍</div>
                <div class="contact-title">{t['labels']['adresse_title']}</div>
                <div class="contact-value">{adresse}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    f"""
    <div class="footer">
        <strong>{nom}</strong>
        <br><br>
        {t['fonction']}
        <br>
        {t['labels']['sub_keywords']}
    </div>
    """,
    unsafe_allow_html=True,
)
