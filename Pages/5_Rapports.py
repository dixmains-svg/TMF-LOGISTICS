import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO
import plotly.express as px


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="TMF LOGISTICS - Rapports",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# CHEMINS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "Data"

FICHIER_OM = DATA_DIR / "OM.xlsx"
FICHIER_CAMIONS = DATA_DIR / "Camions.xlsx"
FICHIER_CHAUFFEURS = DATA_DIR / "Chauffeurs.xlsx"


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>

    .report-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .report-subtitle {
        font-size: 17px;
        color: #666;
        margin-bottom: 20px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TITRE
# ============================================================

st.markdown(
    '<div class="report-title">📊 TMF LOGISTICS - RAPPORTS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="report-subtitle">'
    'Tableau de bord des indicateurs de gestion et de performance'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# LECTURE OM
# ============================================================

@st.cache_data
def charger_om():

    if not FICHIER_OM.exists():
        return pd.DataFrame()

    try:

        df = pd.read_excel(
            FICHIER_OM,
            sheet_name="Input OM fini",
            engine="openpyxl"
        )

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        return df

    except Exception as e:

        st.error(
            f"❌ Erreur lecture OM.xlsx : {e}"
        )

        return pd.DataFrame()


# ============================================================
# LECTURE CAMIONS
# ============================================================

@st.cache_data
def charger_camions():

    if not FICHIER_CAMIONS.exists():
        return pd.DataFrame()

    try:

        df = pd.read_excel(
            FICHIER_CAMIONS,
            engine="openpyxl"
        )

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        return df

    except Exception as e:

        st.error(
            f"❌ Erreur lecture Camions.xlsx : {e}"
        )

        return pd.DataFrame()


# ============================================================
# LECTURE CHAUFFEURS
# ============================================================

@st.cache_data
def charger_chauffeurs():

    if not FICHIER_CHAUFFEURS.exists():
        return pd.DataFrame()

    try:

        df = pd.read_excel(
            FICHIER_CHAUFFEURS,
            engine="openpyxl"
        )

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        return df

    except Exception as e:

        st.error(
            f"❌ Erreur lecture Chauffeurs.xlsx : {e}"
        )

        return pd.DataFrame()


# ============================================================
# CHARGEMENT
# ============================================================

df_om = charger_om()

df_camions = charger_camions()

df_chauffeurs = charger_chauffeurs()


# ============================================================
# VÉRIFICATION
# ============================================================

if df_om.empty:

    st.error(
        f"""
        ❌ Impossible de charger les Ordres de Mission.

        Fichier :
        `{FICHIER_OM}`
        """
    )

    st.stop()


# ============================================================
# NETTOYAGE
# ============================================================

df_om = df_om.copy()

df_om.columns = (
    df_om.columns
    .astype(str)
    .str.strip()
)


# ============================================================
# CONVERSION DATE
# ============================================================

if "Date Depart" in df_om.columns:

    df_om["Date Depart"] = pd.to_datetime(
        df_om["Date Depart"],
        errors="coerce"
    )


# ============================================================
# FILTRES
# ============================================================

st.markdown(
    '<div class="section-title">🔎 Filtres</div>',
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3)


# ------------------------------------------------------------
# DATE
# ------------------------------------------------------------

with col1:

    if "Date Depart" in df_om.columns:

        dates = df_om["Date Depart"].dropna()

        if not dates.empty:

            date_min = dates.min().date()
            date_max = dates.max().date()

            periode = st.date_input(
                "📅 Période",
                value=(date_min, date_max),
                min_value=date_min,
                max_value=date_max
            )

        else:

            periode = None

    else:

        periode = None


# ------------------------------------------------------------
# CLIENT
# ------------------------------------------------------------

with col2:

    if "Client" in df_om.columns:

        clients = sorted(
            df_om["Client"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        client_selection = st.multiselect(
            "👥 Client",
            clients
        )

    else:

        client_selection = []


# ------------------------------------------------------------
# CAMION
# ------------------------------------------------------------

with col3:

    if "Numero Camion" in df_om.columns:

        camions = sorted(
            df_om["Numero Camion"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        camion_selection = st.multiselect(
            "🚚 Camion",
            camions
        )

    else:

        camion_selection = []


# ============================================================
# FILTRE CHAUFFEUR
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    if "Chauffeur" in df_om.columns:

        chauffeurs = sorted(
            df_om["Chauffeur"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        chauffeur_selection = st.multiselect(
            "👷 Chauffeur",
            chauffeurs
        )

    else:

        chauffeur_selection = []


with col2:

    if "Status" in df_om.columns:

        statuts = sorted(
            df_om["Status"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        statut_selection = st.multiselect(
            "📊 Statut OM",
            statuts
        )

    else:

        statut_selection = []


with col3:

    if "Section" in df_om.columns:

        sections = sorted(
            df_om["Section"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        section_selection = st.multiselect(
            "🏢 Section",
            sections
        )

    else:

        section_selection = []


# ============================================================
# APPLICATION DES FILTRES
# ============================================================

df = df_om.copy()


if periode and len(periode) == 2:

    date_debut = pd.Timestamp(periode[0])

    date_fin = (
        pd.Timestamp(periode[1])
        + pd.Timedelta(days=1)
    )

    df = df[
        (df["Date Depart"] >= date_debut)
        &
        (df["Date Depart"] < date_fin)
    ]


if client_selection:

    df = df[
        df["Client"]
        .astype(str)
        .isin(client_selection)
    ]


if camion_selection:

    df = df[
        df["Numero Camion"]
        .astype(str)
        .isin(camion_selection)
    ]


if chauffeur_selection:

    df = df[
        df["Chauffeur"]
        .astype(str)
        .isin(chauffeur_selection)
    ]


if statut_selection:

    df = df[
        df["Status"]
        .astype(str)
        .isin(statut_selection)
    ]


if section_selection:

    df = df[
        df["Section"]
        .astype(str)
        .isin(section_selection)
    ]


# ============================================================
# FONCTION POUR POURCENTAGE
# ============================================================

def taux(numerateur, denominateur):

    try:

        if denominateur == 0:
            return 0.0

        return (numerateur / denominateur) * 100

    except:

        return 0.0


# ============================================================
# DONNÉES FLOTTES
# ============================================================

total_flottte = len(df_camions)

if total_flottte == 0:

    if "Numero Camion" in df_om.columns:

        total_flottte = (
            df_om["Numero Camion"]
            .replace("", pd.NA)
            .dropna()
            .nunique()
        )


# ============================================================
# IDENTIFICATION DES CAMIONS
# ============================================================

camions_exploites = 0

if "Numero Camion" in df.columns:

    camions_exploites = (
        df["Numero Camion"]
        .replace("", pd.NA)
        .dropna()
        .nunique()
    )


# ============================================================
# OPÉRATIONNEL
# ============================================================

if "Status" in df.columns:

    status_text = (
        df["Status"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    masque_terminee = status_text.str.contains(
        "termin",
        na=False
    )

    total_operationnel = (
        df.loc[masque_terminee, "Numero Camion"]
        .replace("", pd.NA)
        .dropna()
        .nunique()
        if "Numero Camion" in df.columns
        else 0
    )

else:

    total_operationnel = 0


# ============================================================
# TOTAL OM
# ============================================================

total_om = len(df)


# ============================================================
# OM TERMINÉES
# ============================================================

if "Status" in df.columns:

    total_om_terminees = (
        df["Status"]
        .astype(str)
        .str.lower()
        .str.contains(
            "termin",
            na=False
        )
        .sum()
    )

else:

    total_om_terminees = 0


# ============================================================
# CAMIONS SANS PLAN DE CHARGE
# ============================================================

camions_sans_plan = 0

if total_flottte > 0:

    if "Numero Camion" in df.columns:

        camions_avec_om = (
            df["Numero Camion"]
            .replace("", pd.NA)
            .dropna()
            .astype(str)
            .nunique()
        )

        camions_sans_plan = max(
            total_flottte - camions_avec_om,
            0
        )


# ============================================================
# DÉFAUTS TECHNIQUES / ORGANISATIONNELS
# ============================================================

total_defaut_technique = 0

total_defaut_org_interne = 0

total_defaut_org_externe = 0


# On cherche automatiquement les colonnes contenant
# les mots-clés correspondants.

colonnes_defaut = [
    c for c in df.columns
    if any(
        mot in c.lower()
        for mot in [
            "defaut",
            "défaut",
            "panne",
            "motif",
            "indispon"
        ]
    )
]


if colonnes_defaut:

    colonne_defaut = colonnes_defaut[0]

    valeurs_defaut = (
        df[colonne_defaut]
        .astype(str)
        .str.lower()
    )

    total_defaut_technique = valeurs_defaut.str.contains(
        "technique|panne|mecanique|mécanique",
        na=False
    ).sum()

    total_defaut_org_interne = valeurs_defaut.str.contains(
        "interne|organisationnel interne",
        na=False
    ).sum()

    total_defaut_org_externe = valeurs_defaut.str.contains(
        "externe|organisationnel externe",
        na=False
    ).sum()


# ============================================================
# INDICATEURS FLOTTES
# ============================================================

taux_exploitation_flotte = taux(
    camions_exploites,
    total_flottte
)


taux_exploitation_operationnelle = taux(
    total_om_terminees,
    total_om
)


taux_flotte_operationnelle = taux(
    total_operationnel,
    total_flottte
)


taux_flotte_non_operationnelle = (
    100 - taux_flotte_operationnelle
    if total_flottte > 0
    else 0
)


taux_defaut_technique = taux(
    total_defaut_technique,
    total_flottte
)


taux_flotte_sans_plan = taux(
    camions_sans_plan,
    total_flottte
)


taux_defaut_org_interne = taux(
    total_defaut_org_interne,
    total_flottte
)


taux_defaut_org_externe = taux(
    total_defaut_org_externe,
    total_flottte
)


# ============================================================
# TITRE FLOTTE
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">🚚 Indicateurs Flotte</div>',
    unsafe_allow_html=True
)


# ============================================================
# CARTES FLOTTES
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Capacité Logistique",
        total_flottte
    )


with col2:

    st.metric(
        "Total exploitation flotte",
        camions_exploites
    )


with col3:

    st.metric(
        "Total opérationnel",
        total_operationnel
    )


with col4:

    st.metric(
        "Total non opérationnel",
        max(
            total_flottte - total_operationnel,
            0
        )
    )


# ============================================================
# DEUXIÈME LIGNE
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Défaut technique",
        total_defaut_technique
    )


with col2:

    st.metric(
        "Camions sans plan de charge",
        camions_sans_plan
    )


with col3:

    st.metric(
        "Défaut organisationnel interne",
        total_defaut_org_interne
    )


with col4:

    st.metric(
        "Défaut organisationnel externe",
        total_defaut_org_externe
    )


# ============================================================
# TAUX FLOTTES
# ============================================================

st.markdown("### 📈 Taux Flotte")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Taux d'exploitation flotte",
        f"{taux_exploitation_flotte:.2f} %"
    )


with col2:

    st.metric(
        "Taux d'exploitation opérationnelle",
        f"{taux_exploitation_operationnelle:.2f} %"
    )


with col3:

    st.metric(
        "Taux flotte opérationnelle",
        f"{taux_flotte_operationnelle:.2f} %"
    )


with col4:

    st.metric(
        "Taux flotte non opérationnelle",
        f"{taux_flotte_non_operationnelle:.2f} %"
    )


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Défaut technique",
        f"{taux_defaut_technique:.2f} %"
    )


with col2:

    st.metric(
        "Flotte sans plan de charge",
        f"{taux_flotte_sans_plan:.2f} %"
    )


with col3:

    st.metric(
        "Défaut organisationnel interne",
        f"{taux_defaut_org_interne:.2f} %"
    )


with col4:

    st.metric(
        "Défaut organisationnel externe",
        f"{taux_defaut_org_externe:.2f} %"
    )


# ============================================================
# CHAUFFEURS
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">👷 Indicateurs Chauffeurs</div>',
    unsafe_allow_html=True
)


# ============================================================
# TOTAL CHAUFFEURS
# ============================================================

if not df_chauffeurs.empty:

    total_chauffeurs = len(df_chauffeurs)

else:

    if "Chauffeur" in df.columns:

        total_chauffeurs = (
            df["Chauffeur"]
            .replace("", pd.NA)
            .dropna()
            .nunique()
        )

    else:

        total_chauffeurs = 0


# ============================================================
# DÉTECTION DES COLONNES CHAUFFEURS
# ============================================================

colonne_statut_chauffeur = None


for colonne in df_chauffeurs.columns:

    nom = colonne.lower()

    if (
        "statut" in nom
        or "status" in nom
        or "situation" in nom
        or "disponibil" in nom
    ):

        colonne_statut_chauffeur = colonne
        break


# ============================================================
# COMPTEURS CHAUFFEURS
# ============================================================

chauffeurs_disponibles = 0

chauffeurs_service = 0

chauffeurs_chomage = 0

chauffeurs_absence_prevue = 0

chauffeurs_absence_non_prevue = 0


if (
    not df_chauffeurs.empty
    and colonne_statut_chauffeur
):

    statuts_ch = (
        df_chauffeurs[
            colonne_statut_chauffeur
        ]
        .astype(str)
        .str.lower()
        .str.strip()
    )


    chauffeurs_disponibles = (
        statuts_ch.str.contains(
            "disponible",
            na=False
        )
        .sum()
    )


    chauffeurs_service = (
        statuts_ch.str.contains(
            "service|en service",
            na=False
        )
        .sum()
    )


    chauffeurs_chomage = (
        statuts_ch.str.contains(
            "chomage|chômage",
            na=False
        )
        .sum()
    )


    chauffeurs_absence_prevue = (
        statuts_ch.str.contains(
            "absence prévue|absence prevue|congé|conge",
            na=False
        )
        .sum()
    )


    chauffeurs_absence_non_prevue = (
        statuts_ch.str.contains(
            "absence non prévue|absence non prevue",
            na=False
        )
        .sum()
    )


# ============================================================
# TAUX CHAUFFEURS
# ============================================================

taux_utilisation = taux(
    chauffeurs_service,
    total_chauffeurs
)


taux_chomage = taux(
    chauffeurs_chomage,
    total_chauffeurs
)


taux_chauffeur_disponible = taux(
    chauffeurs_disponibles,
    total_chauffeurs
)


taux_absence_prevue = taux(
    chauffeurs_absence_prevue,
    total_chauffeurs
)


taux_absence_non_prevue = taux(
    chauffeurs_absence_non_prevue,
    total_chauffeurs
)


# ============================================================
# CARTES CHAUFFEURS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "Total chauffeurs",
        total_chauffeurs
    )


with col2:

    st.metric(
        "Disponible",
        chauffeurs_disponibles
    )


with col3:

    st.metric(
        "En service",
        chauffeurs_service
    )


with col4:

    st.metric(
        "En chômage",
        chauffeurs_chomage
    )


with col5:

    st.metric(
        "Absence prévue",
        chauffeurs_absence_prevue
    )


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Absence non prévue",
        chauffeurs_absence_non_prevue
    )


with col2:

    st.metric(
        "Taux d'utilisation",
        f"{taux_utilisation:.2f} %"
    )


with col3:

    st.metric(
        "Taux de chômage",
        f"{taux_chomage:.2f} %"
    )


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Taux chauffeur disponible",
        f"{taux_chauffeur_disponible:.2f} %"
    )


with col2:

    st.metric(
        "Taux absence prévue",
        f"{taux_absence_prevue:.2f} %"
    )


with col3:

    st.metric(
        "Taux absence non prévue",
        f"{taux_absence_non_prevue:.2f} %"
    )


# ============================================================
# TAUX DE SERVICE CHAUFFEUR
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">🎯 Performance Chauffeurs</div>',
    unsafe_allow_html=True
)


# Nombre de chauffeurs ayant réalisé au moins une OM
if "Chauffeur" in df.columns:

    chauffeurs_ayant_om = (
        df["Chauffeur"]
        .replace("", pd.NA)
        .dropna()
        .nunique()
    )

else:

    chauffeurs_ayant_om = 0


taux_service_chauffeur = taux(
    chauffeurs_ayant_om,
    total_chauffeurs
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Chauffeurs ayant réalisé une OM",
        chauffeurs_ayant_om
    )


with col2:

    st.metric(
        "Total chauffeurs",
        total_chauffeurs
    )


with col3:

    st.metric(
        "🎯 Taux de service chauffeur",
        f"{taux_service_chauffeur:.2f} %"
    )


# ============================================================
# OPTIMISATION CAMIONS
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">🚚 Optimisation des Camions</div>',
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# KM
# ------------------------------------------------------------

km_depart = 0

km_retour = 0

km_parcourus = 0


if "Kilometrage au Depart" in df.columns:

    km_depart = pd.to_numeric(
        df["Kilometrage au Depart"],
        errors="coerce"
    ).fillna(0).sum()


if "Kilometrage au Retour" in df.columns:

    km_retour = pd.to_numeric(
        df["Kilometrage au Retour"],
        errors="coerce"
    ).fillna(0).sum()


if "Kilometrage Parcouru" in df.columns:

    km_parcourus = pd.to_numeric(
        df["Kilometrage Parcouru"],
        errors="coerce"
    ).fillna(0).sum()


# ------------------------------------------------------------
# RETOUR À VIDE
# ------------------------------------------------------------

retours_vides = 0


if "Tonnage" in df.columns:

    tonnage = pd.to_numeric(
        df["Tonnage"],
        errors="coerce"
    )

    retours_vides = (
        tonnage.fillna(0) <= 0
    ).sum()


elif "Nature du Chargement" in df.columns:

    nature = (
        df["Nature du Chargement"]
        .astype(str)
        .str.lower()
    )

    retours_vides = (
        nature.str.contains(
            "vide|retour vide",
            na=False
        )
    ).sum()


# ============================================================
# TAUX RETOUR À VIDE
# ============================================================

taux_retour_vide = taux(
    retours_vides,
    total_om
)


# ============================================================
# TAUX OPTIMISATION CAMION
# ============================================================

# Définition technique par défaut :
# kilomètres parcourus par les OM / kilomètres calculables.
#
# Cette définition pourra être remplacée par votre règle
# métier exacte.

if km_depart > 0 and km_retour >= km_depart:

    km_theoriques = km_retour - km_depart

    taux_optimisation_camion = taux(
        km_parcourus,
        km_theoriques
    )

else:

    taux_optimisation_camion = 0


# On limite l'indicateur à 100 % dans le tableau
# pour éviter les valeurs aberrantes dues aux données.

taux_optimisation_affiche = min(
    max(taux_optimisation_camion, 0),
    100
)


# ============================================================
# CARTES
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "OM analysées",
        total_om
    )


with col2:

    st.metric(
        "Retour à vide",
        retours_vides
    )


with col3:

    st.metric(
        "📦 Taux retour à vide",
        f"{taux_retour_vide:.2f} %"
    )


with col4:

    st.metric(
        "🚚 Taux optimisation camion",
        f"{taux_optimisation_affiche:.2f} %"
    )


# ============================================================
# GRAPHIQUES
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📊 Analyse graphique</div>',
    unsafe_allow_html=True
)


# ============================================================
# GRAPHIQUE FLOTTE
# ============================================================

df_graph_flotte = pd.DataFrame(
    {
        "Indicateur": [
            "Opérationnelle",
            "Non opérationnelle",
            "Sans plan de charge",
            "Défaut technique"
        ],
        "Taux": [
            taux_flotte_operationnelle,
            taux_flotte_non_operationnelle,
            taux_flotte_sans_plan,
            taux_defaut_technique
        ]
    }
)


fig_flotte = px.bar(
    df_graph_flotte,
    x="Indicateur",
    y="Taux",
    text="Taux",
    title="Performance de la flotte"
)


fig_flotte.update_traces(
    texttemplate="%{text:.2f} %",
    textposition="outside"
)


fig_flotte.update_layout(
    yaxis_title="Pourcentage",
    xaxis_title=""
)


st.plotly_chart(
    fig_flotte,
    use_container_width=True
)


# ============================================================
# GRAPHIQUE CHAUFFEURS
# ============================================================

df_graph_chauffeurs = pd.DataFrame(
    {
        "Indicateur": [
            "Disponible",
            "En service",
            "Chômage",
            "Absence prévue",
            "Absence non prévue"
        ],
        "Taux": [
            taux_chauffeur_disponible,
            taux_utilisation,
            taux_chomage,
            taux_absence_prevue,
            taux_absence_non_prevue
        ]
    }
)


fig_chauffeurs = px.bar(
    df_graph_chauffeurs,
    x="Indicateur",
    y="Taux",
    text="Taux",
    title="Situation des chauffeurs"
)


fig_chauffeurs.update_traces(
    texttemplate="%{text:.2f} %",
    textposition="outside"
)


fig_chauffeurs.update_layout(
    yaxis_title="Pourcentage",
    xaxis_title=""
)


st.plotly_chart(
    fig_chauffeurs,
    use_container_width=True
)


# ============================================================
# PERFORMANCE TRANSPORT
# ============================================================

df_graph_transport = pd.DataFrame(
    {
        "Indicateur": [
            "Service chauffeur",
            "Optimisation camion",
            "Retour à vide"
        ],
        "Taux": [
            taux_service_chauffeur,
            taux_optimisation_affiche,
            taux_retour_vide
        ]
    }
)


fig_transport = px.bar(
    df_graph_transport,
    x="Indicateur",
    y="Taux",
    text="Taux",
    title="Performance transport"
)


fig_transport.update_traces(
    texttemplate="%{text:.2f} %",
    textposition="outside"
)


fig_transport.update_layout(
    yaxis_title="Pourcentage",
    xaxis_title=""
)


st.plotly_chart(
    fig_transport,
    use_container_width=True
)


# ============================================================
# GLOBAL FLOTTE
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">🏆 Global Flotte</div>',
    unsafe_allow_html=True
)


# Moyenne des trois indicateurs principaux
global_flotte = (
    taux_service_chauffeur
    + taux_optimisation_affiche
    + (100 - taux_retour_vide)
) / 3


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🎯 Service chauffeur",
        f"{taux_service_chauffeur:.2f} %"
    )


with col2:

    st.metric(
        "🚚 Optimisation camion",
        f"{taux_optimisation_affiche:.2f} %"
    )


with col3:

    st.metric(
        "↩️ Retour à vide",
        f"{taux_retour_vide:.2f} %"
    )


with col4:

    st.metric(
        "🏆 Global flotte",
        f"{global_flotte:.2f} %"
    )


# ============================================================
# TABLEAU RÉCAPITULATIF
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📋 Tableau récapitulatif</div>',
    unsafe_allow_html=True
)


rapport = pd.DataFrame(
    {
        "Indicateur": [
            "Total Capacité Logistique",
            "Total exploitation flotte",
            "Total opérationnel",
            "Total non opérationnel",
            "Total défaut technique",
            "Total camion sans plan de charge",
            "Total défaut organisationnel interne",
            "Total défaut organisationnel externe",
            "Taux d'exploitation flotte",
            "Taux d'exploitation opérationnelle",
            "Taux de flotte opérationnelle",
            "Taux de flotte non opérationnelle",
            "Défaut technique",
            "Taux flotte sans plan de charge",
            "Défaut organisationnel interne",
            "Défaut organisationnel externe",
            "Taux d'utilisation",
            "Taux de chômage",
            "Taux chauffeur disponible",
            "Taux chauffeur absence prévue",
            "Taux chauffeur absence non prévue",
            "Total chauffeur disponible",
            "Total chauffeur en service",
            "Total chauffeur en chômage",
            "Total chauffeur absence prévue",
            "Total chauffeur absence non prévue",
            "Taux de service chauffeur",
            "Taux d'optimisation camion",
            "Taux de retour à vide",
            "Global flotte"
        ],
        "Valeur": [
            total_flottte,
            camions_exploites,
            total_operationnel,
            max(total_flottte - total_operationnel, 0),
            total_defaut_technique,
            camions_sans_plan,
            total_defaut_org_interne,
            total_defaut_org_externe,
            f"{taux_exploitation_flotte:.2f} %",
            f"{taux_exploitation_operationnelle:.2f} %",
            f"{taux_flotte_operationnelle:.2f} %",
            f"{taux_flotte_non_operationnelle:.2f} %",
            f"{taux_defaut_technique:.2f} %",
            f"{taux_flotte_sans_plan:.2f} %",
            f"{taux_defaut_org_interne:.2f} %",
            f"{taux_defaut_org_externe:.2f} %",
            f"{taux_utilisation:.2f} %",
            f"{taux_chomage:.2f} %",
            f"{taux_chauffeur_disponible:.2f} %",
            f"{taux_absence_prevue:.2f} %",
            f"{taux_absence_non_prevue:.2f} %",
            chauffeurs_disponibles,
            chauffeurs_service,
            chauffeurs_chomage,
            chauffeurs_absence_prevue,
            chauffeurs_absence_non_prevue,
            f"{taux_service_chauffeur:.2f} %",
            f"{taux_optimisation_affiche:.2f} %",
            f"{taux_retour_vide:.2f} %",
            f"{global_flotte:.2f} %"
        ]
    }
)


st.dataframe(
    rapport,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# EXPORT EXCEL
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">📥 Export du rapport</div>',
    unsafe_allow_html=True
)


def exporter_excel():

    buffer = BytesIO()

    with pd.ExcelWriter(
        buffer,
        engine="openpyxl"
    ) as writer:

        rapport.to_excel(
            writer,
            index=False,
            sheet_name="Indicateurs"
        )

        df.to_excel(
            writer,
            index=False,
            sheet_name="OM filtrées"
        )

    return buffer.getvalue()


excel_data = exporter_excel()


st.download_button(
    label="📥 Télécharger le rapport Excel",
    data=excel_data,
    file_name="Rapport_TMF_LOGISTICS.xlsx",
    mime=(
        "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet"
    )
)


# ============================================================
# ACTUALISATION
# ============================================================

st.divider()

if st.button("🔄 Actualiser les données"):

    st.cache_data.clear()

    st.rerun()
