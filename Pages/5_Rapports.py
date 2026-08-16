import streamlit as st
import pandas as pd
from pathlib import Path


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

FICHIER_OM = BASE_DIR / "Data" / "OM.xlsx"
FICHIER_CHAUFFEURS = BASE_DIR / "Data" / "Chauffeurs.xlsx"
FICHIER_CLIENTS = BASE_DIR / "Data" / "Clients.xlsx"
FICHIER_COMMANDES = BASE_DIR / "Data" / "Commande de vente.xlsx"

FEUILLE_OM = "Input OM fini"
FEUILLE_CHAUFFEURS = "Chauffeurs"
FEUILLE_COMMANDES = "Feuil1"


# ============================================================
# FONCTION DE NETTOYAGE
# ============================================================

def nettoyer_dataframe(df):

    df = df.copy()

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    for colonne in df.columns:

        if df[colonne].dtype == "object":

            df[colonne] = (
                df[colonne]
                .fillna("")
                .astype(str)
                .str.strip()
            )

    return df


# ============================================================
# LECTURE OM
# ============================================================

@st.cache_data(ttl=30)
def charger_om():

    if not FICHIER_OM.exists():
        return pd.DataFrame()

    try:

        df = pd.read_excel(
            FICHIER_OM,
            sheet_name=FEUILLE_OM,
            engine="openpyxl"
        )

        return nettoyer_dataframe(df)

    except Exception:

        try:

            df = pd.read_excel(
                FICHIER_OM,
                engine="openpyxl"
            )

            return nettoyer_dataframe(df)

        except Exception as e:

            st.error(
                f"❌ Erreur lors de la lecture de OM.xlsx : {e}"
            )

            return pd.DataFrame()


# ============================================================
# LECTURE CHAUFFEURS
# ============================================================

@st.cache_data(ttl=30)
def charger_chauffeurs():

    if not FICHIER_CHAUFFEURS.exists():
        return pd.DataFrame()

    try:

        df = pd.read_excel(
            FICHIER_CHAUFFEURS,
            sheet_name=FEUILLE_CHAUFFEURS,
            engine="openpyxl"
        )

        return nettoyer_dataframe(df)

    except Exception:

        try:

            df = pd.read_excel(
                FICHIER_CHAUFFEURS,
                engine="openpyxl"
            )

            return nettoyer_dataframe(df)

        except Exception as e:

            st.error(
                f"❌ Erreur lors de la lecture de Chauffeurs.xlsx : {e}"
            )

            return pd.DataFrame()


# ============================================================
# LECTURE CLIENTS
# ============================================================

@st.cache_data(ttl=30)
def charger_clients():

    if not FICHIER_CLIENTS.exists():
        return pd.DataFrame()

    try:

        df = pd.read_excel(
            FICHIER_CLIENTS,
            engine="openpyxl"
        )

        return nettoyer_dataframe(df)

    except Exception as e:

        st.error(
            f"❌ Erreur lors de la lecture de Clients.xlsx : {e}"
        )

        return pd.DataFrame()


# ============================================================
# LECTURE COMMANDES DE VENTE
# ============================================================

@st.cache_data(ttl=30)
def charger_commandes():

    if not FICHIER_COMMANDES.exists():
        return pd.DataFrame()

    try:

        df = pd.read_excel(
            FICHIER_COMMANDES,
            sheet_name=FEUILLE_COMMANDES,
            engine="openpyxl"
        )

        df = nettoyer_dataframe(df)

        # Dates
        for colonne in [
            "Date de Mission",
            "Date Heure Charg Planif"
        ]:
            if colonne in df.columns:
                df[colonne] = pd.to_datetime(
                    df[colonne],
                    errors="coerce"
                )

        # Colonnes numériques
        for colonne in [
            "Prix unitaire",
            "Quantité restante",
            "Tonnage",
            "Montant ligne HT",
            "Quantité",
            "Quantité réservée (base)"
        ]:
            if colonne in df.columns:
                df[colonne] = pd.to_numeric(
                    df[colonne],
                    errors="coerce"
                )

        return df

    except Exception:

        try:

            df = pd.read_excel(
                FICHIER_COMMANDES,
                engine="openpyxl"
            )

            df = nettoyer_dataframe(df)

            for colonne in [
                "Date de Mission",
                "Date Heure Charg Planif"
            ]:
                if colonne in df.columns:
                    df[colonne] = pd.to_datetime(
                        df[colonne],
                        errors="coerce"
                    )

            for colonne in [
                "Prix unitaire",
                "Quantité restante",
                "Tonnage",
                "Montant ligne HT",
                "Quantité",
                "Quantité réservée (base)"
            ]:
                if colonne in df.columns:
                    df[colonne] = pd.to_numeric(
                        df[colonne],
                        errors="coerce"
                    )

            return df

        except Exception as e:

            st.error(
                f"❌ Erreur lors de la lecture de Commande de vente.xlsx : {e}"
            )

            return pd.DataFrame()


# ============================================================
# CHARGEMENT
# ============================================================

df_om = charger_om()
df_chauffeurs = charger_chauffeurs()
df_clients = charger_clients()
df_commandes = charger_commandes()


# ============================================================
# TITRE
# ============================================================

st.title("📊 Rapports & Analyse")

st.subheader(
    "Analyse des données de TMF LOGISTICS"
)

st.caption(
    "Analyse croisée des Ordres de Mission, Commandes de vente, "
    "Chauffeurs et Clients."
)


# ============================================================
# VÉRIFICATION OM
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
# SIDEBAR
# ============================================================

st.sidebar.header("🔎 Filtres du rapport")


# ============================================================
# PRÉPARATION DES DATES OM
# ============================================================

if "Date Depart" in df_om.columns:

    df_om["Date Depart"] = pd.to_datetime(
        df_om["Date Depart"],
        errors="coerce"
    )

    dates_valides = (
        df_om["Date Depart"]
        .dropna()
    )

else:

    dates_valides = pd.Series(dtype="datetime64[ns]")


# ============================================================
# FILTRE PÉRIODE
# ============================================================

if not dates_valides.empty:

    date_min = dates_valides.min().date()
    date_max = dates_valides.max().date()

    periode = st.sidebar.date_input(
        "📅 Période",
        value=(date_min, date_max),
        min_value=date_min,
        max_value=date_max,
        key="rapport_5_periode_principale"
    )

else:

    periode = None


# ============================================================
# FILTRE STATUT
# ============================================================

if "Status" in df_om.columns:

    statuts = sorted(
        [
            str(x)
            for x in df_om["Status"].dropna().unique()
            if str(x).strip()
        ]
    )

else:

    statuts = []


filtre_statut = st.sidebar.multiselect(
    "📊 Statut",
    statuts,
    key="rapport_filtre_statut"
)


# ============================================================
# FILTRE CLIENT
# ============================================================

if "Client" in df_om.columns:

    clients = sorted(
        [
            str(x)
            for x in df_om["Client"].dropna().unique()
            if str(x).strip()
        ]
    )

else:

    clients = []


filtre_client = st.sidebar.multiselect(
    "👥 Client",
    clients,
    key="rapport_filtre_client"
)


# ============================================================
# FILTRE CHAUFFEUR
# ============================================================

if "Chauffeur" in df_om.columns:

    chauffeurs = sorted(
        [
            str(x)
            for x in df_om["Chauffeur"].dropna().unique()
            if str(x).strip()
        ]
    )

else:

    chauffeurs = []


filtre_chauffeur = st.sidebar.multiselect(
    "👷 Chauffeur",
    chauffeurs,
    key="rapport_filtre_chauffeur"
)


# ============================================================
# FILTRE SECTION
# ============================================================

if "Section" in df_om.columns:

    sections = sorted(
        [
            str(x)
            for x in df_om["Section"].dropna().unique()
            if str(x).strip()
        ]
    )

else:

    sections = []


filtre_section = st.sidebar.multiselect(
    "🏢 Section",
    sections,
    key="rapport_filtre_section"
)


# ============================================================
# APPLICATION DES FILTRES OM
# ============================================================

df_analyse = df_om.copy()


# ------------------------------------------------------------
# PÉRIODE
# ------------------------------------------------------------

if periode is not None and len(periode) == 2:

    date_debut = pd.Timestamp(periode[0])
    date_fin = pd.Timestamp(periode[1]) + pd.Timedelta(days=1)

    if "Date Depart" in df_analyse.columns:

        df_analyse = df_analyse[
            (
                df_analyse["Date Depart"] >= date_debut
            )
            &
            (
                df_analyse["Date Depart"] < date_fin
            )
        ].copy()


# ------------------------------------------------------------
# STATUT
# ------------------------------------------------------------

if filtre_statut and "Status" in df_analyse.columns:

    df_analyse = df_analyse[
        df_analyse["Status"].isin(
            filtre_statut
        )
    ].copy()


# ------------------------------------------------------------
# CLIENT
# ------------------------------------------------------------

if filtre_client and "Client" in df_analyse.columns:

    df_analyse = df_analyse[
        df_analyse["Client"].isin(
            filtre_client
        )
    ].copy()


# ------------------------------------------------------------
# CHAUFFEUR
# ------------------------------------------------------------

if filtre_chauffeur and "Chauffeur" in df_analyse.columns:

    df_analyse = df_analyse[
        df_analyse["Chauffeur"].isin(
            filtre_chauffeur
        )
    ].copy()


# ------------------------------------------------------------
# SECTION
# ------------------------------------------------------------

if filtre_section and "Section" in df_analyse.columns:

    df_analyse = df_analyse[
        df_analyse["Section"].isin(
            filtre_section
        )
    ].copy()


# ============================================================
# PRÉPARATION COMMANDES DE VENTE POUR LA MÊME PÉRIODE
# ============================================================

df_commandes_analyse = df_commandes.copy()

if (
    periode is not None
    and len(periode) == 2
    and "Date de Mission" in df_commandes_analyse.columns
):

    date_debut_cmd = pd.Timestamp(periode[0])
    date_fin_cmd = pd.Timestamp(periode[1]) + pd.Timedelta(days=1)

    df_commandes_analyse = df_commandes_analyse[
        (
            df_commandes_analyse["Date de Mission"] >= date_debut_cmd
        )
        &
        (
            df_commandes_analyse["Date de Mission"] < date_fin_cmd
        )
    ].copy()


# ============================================================
# RÉSUMÉ
# ============================================================

st.divider()

st.header("📊 Synthèse générale")


nombre_om = len(df_analyse)


if "Numero Camion" in df_analyse.columns:

    nombre_camions = (
        df_analyse["Numero Camion"]
        .replace("", pd.NA)
        .nunique()
    )

else:

    nombre_camions = 0


if "Chauffeur" in df_analyse.columns:

    nombre_chauffeurs = (
        df_analyse["Chauffeur"]
        .replace("", pd.NA)
        .nunique()
    )

else:

    nombre_chauffeurs = 0


if "Client" in df_analyse.columns:

    nombre_clients = (
        df_analyse["Client"]
        .replace("", pd.NA)
        .nunique()
    )

else:

    nombre_clients = 0


# Commandes de vente
if not df_commandes_analyse.empty:

    if "N° document" in df_commandes_analyse.columns:
        nombre_commandes = (
            df_commandes_analyse["N° document"]
            .replace("", pd.NA)
            .nunique()
        )
    else:
        nombre_commandes = len(df_commandes_analyse)

    if "Montant ligne HT" in df_commandes_analyse.columns:
        montant_commandes = (
            pd.to_numeric(
                df_commandes_analyse["Montant ligne HT"],
                errors="coerce"
            )
            .fillna(0)
            .sum()
        )
    else:
        montant_commandes = 0

else:

    nombre_commandes = 0
    montant_commandes = 0


col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "📋 Ordres de Mission",
        nombre_om
    )


with col2:

    st.metric(
        "🚚 Camions",
        nombre_camions
    )


with col3:

    st.metric(
        "👷 Chauffeurs",
        nombre_chauffeurs
    )


with col4:

    st.metric(
        "👥 Clients",
        nombre_clients
    )


with col5:

    st.metric(
        "📦 Commandes de vente",
        nombre_commandes
    )


# ============================================================
# COMMANDES DE VENTE
# ============================================================

st.divider()

st.header("📦 Analyse des Commandes de vente")

if df_commandes.empty:

    st.warning(
        f"""
        ⚠️ Le fichier Commande de vente.xlsx n'a pas été trouvé.

        Emplacement attendu :
        `{FICHIER_COMMANDES}`
        """
    )

else:

    # --------------------------------------------------------
    # INDICATEURS COMMANDES
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    # Nombre de commandes
    if "N° document" in df_commandes_analyse.columns:

        nombre_commandes = (
            df_commandes_analyse["N° document"]
            .replace("", pd.NA)
            .nunique()
        )

    else:

        nombre_commandes = len(df_commandes_analyse)

    # Nombre de lignes
    nombre_lignes_commandes = len(df_commandes_analyse)

    # Tonnage
    if "Tonnage" in df_commandes_analyse.columns:

        tonnage_commandes = (
            pd.to_numeric(
                df_commandes_analyse["Tonnage"],
                errors="coerce"
            )
            .fillna(0)
            .sum()
        )

    else:

        tonnage_commandes = 0

    # Montant HT
    if "Montant ligne HT" in df_commandes_analyse.columns:

        montant_commandes = (
            pd.to_numeric(
                df_commandes_analyse["Montant ligne HT"],
                errors="coerce"
            )
            .fillna(0)
            .sum()
        )

    else:

        montant_commandes = 0

    with col1:

        st.metric(
            "📄 Commandes",
            nombre_commandes
        )

    with col2:

        st.metric(
            "📝 Lignes de commande",
            nombre_lignes_commandes
        )

    with col3:

        st.metric(
            "⚖️ Tonnage",
            f"{tonnage_commandes:,.2f}"
        )

    with col4:

        st.metric(
            "💰 Montant HT",
            f"{montant_commandes:,.2f} DA"
        )

    # --------------------------------------------------------
    # TOP CLIENTS / DONNEURS D'ORDRE
    # --------------------------------------------------------

    if "N° donneur d'ordre" in df_commandes_analyse.columns:

        st.subheader(
            "🏆 Commandes par donneur d'ordre"
        )

        analyse_donneurs = (
            df_commandes_analyse["N° donneur d'ordre"]
            .replace("", "Non renseigné")
            .value_counts()
            .rename_axis("Donneur d'ordre")
            .reset_index(name="Nombre de lignes")
        )

        analyse_donneurs = analyse_donneurs.head(20)

        if not analyse_donneurs.empty:

            st.dataframe(
                analyse_donneurs,
                use_container_width=True,
                hide_index=True
            )

            st.bar_chart(
                analyse_donneurs.set_index(
                    "Donneur d'ordre"
                )
            )

    # --------------------------------------------------------
    # ANALYSE PAR PRODUIT
    # --------------------------------------------------------

    if "Produit Transporté" in df_commandes_analyse.columns:

        st.subheader(
            "📦 Produits transportés"
        )

        analyse_produits = (
            df_commandes_analyse[
                "Produit Transporté"
            ]
            .replace("", "Non renseigné")
            .value_counts()
            .rename_axis("Produit Transporté")
            .reset_index(name="Nombre de lignes")
        )

        analyse_produits = analyse_produits.head(20)

        if not analyse_produits.empty:

            st.dataframe(
                analyse_produits,
                use_container_width=True,
                hide_index=True
            )

            st.bar_chart(
                analyse_produits.set_index(
                    "Produit Transporté"
                )
            )

    # --------------------------------------------------------
    # ANALYSE DES TRAJETS
    # --------------------------------------------------------

    if "Trajet" in df_commandes_analyse.columns:

        st.subheader(
            "🛣️ Principaux trajets"
        )

        analyse_trajets = (
            df_commandes_analyse["Trajet"]
            .replace("", "Non renseigné")
            .value_counts()
            .rename_axis("Trajet")
            .reset_index(name="Nombre de lignes")
        )

        analyse_trajets = analyse_trajets.head(20)

        if not analyse_trajets.empty:

            st.dataframe(
                analyse_trajets,
                use_container_width=True,
                hide_index=True
            )

            st.bar_chart(
                analyse_trajets.set_index(
                    "Trajet"
                )
            )

    # --------------------------------------------------------
    # COMMANDES AVEC OM
    # --------------------------------------------------------

    if "OM Generé" in df_commandes_analyse.columns:

        st.subheader(
            "🚚 Commandes avec Ordre de Mission"
        )

        serie_om = (
            df_commandes_analyse["OM Generé"]
            .astype(str)
            .str.strip()
            .str.lower()
        )

        nombre_avec_om = serie_om.isin(
            ["true", "1", "oui", "yes"]
        ).sum()

        nombre_sans_om = len(
            df_commandes_analyse
        ) - nombre_avec_om

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "✅ Avec OM",
                int(nombre_avec_om)
            )

        with col2:

            st.metric(
                "⏳ Sans OM",
                int(nombre_sans_om)
            )

    # --------------------------------------------------------
    # TABLEAU DES COMMANDES
    # --------------------------------------------------------

    st.subheader(
        "📋 Détail des commandes de vente"
    )

    colonnes_commandes = [
        "Code Convention",
        "Code Vehicule",
        "Date de Mission",
        "N° document",
        "N° ligne",
        "Code Rotation",
        "Type document",
        "N° donneur d'ordre",
        "Désignation",
        "Trajet",
        "Prix unitaire",
        "Date Heure Charg Planif",
        "OM Generé",
        "Quantité restante",
        "Lieu de Chargement",
        "Lieu Déchargement",
        "Produit Transporté",
        "BL Client M1",
        "Tonnage",
        "Ordre de Mission",
        "Montant ligne HT",
        "Quantité",
        "Quantité réservée (base)",
        "Réserver"
    ]

    colonnes_commandes = [
        col
        for col in colonnes_commandes
        if col in df_commandes_analyse.columns
    ]

    tableau_commandes = (
        df_commandes_analyse[
            colonnes_commandes
        ]
        .copy()
    )

    for colonne in [
        "Date de Mission",
        "Date Heure Charg Planif"
    ]:

        if colonne in tableau_commandes.columns:

            if colonne == "Date Heure Charg Planif":

                tableau_commandes[colonne] = (
                    tableau_commandes[colonne]
                    .dt.strftime("%d/%m/%Y %H:%M")
                )

            else:

                tableau_commandes[colonne] = (
                    tableau_commandes[colonne]
                    .dt.strftime("%d/%m/%Y")
                )

    st.dataframe(
        tableau_commandes,
        use_container_width=True,
        hide_index=True,
        height=500
    )


# ============================================================
# KILOMÉTRAGE
# ============================================================

st.divider()

st.header("🛣️ Analyse du kilométrage")


if "Kilometrage Parcouru" in df_analyse.columns:

    df_analyse["Kilometrage Parcouru"] = pd.to_numeric(
        df_analyse["Kilometrage Parcouru"],
        errors="coerce"
    )

    km_total = (
        df_analyse["Kilometrage Parcouru"]
        .fillna(0)
        .sum()
    )

    km_moyen = (
        df_analyse["Kilometrage Parcouru"]
        .dropna()
        .mean()
    )

else:

    km_total = 0
    km_moyen = 0


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "🛣️ KM parcourus",
        f"{km_total:,.0f}"
    )


with col2:

    st.metric(
        "📏 KM moyen / OM",
        f"{km_moyen:,.0f}"
        if pd.notna(km_moyen)
        else "0"
    )


# ============================================================
# ANALYSE PAR STATUT
# ============================================================

st.divider()

st.header("📊 Répartition des Ordres de Mission par statut")


if "Status" in df_analyse.columns:

    analyse_statut = (
        df_analyse["Status"]
        .replace("", "Non renseigné")
        .value_counts()
        .rename_axis("Statut")
        .reset_index(name="Nombre")
    )

    if not analyse_statut.empty:

        st.dataframe(
            analyse_statut,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            analyse_statut.set_index("Statut")
        )


# ============================================================
# ANALYSE CLIENTS
# ============================================================

st.divider()

st.header("👥 Analyse des Clients")


if "Client" in df_analyse.columns:

    analyse_clients = (
        df_analyse["Client"]
        .replace("", "Non renseigné")
        .value_counts()
        .rename_axis("Client")
        .reset_index(name="Nombre OM")
    )

    analyse_clients = analyse_clients.head(20)

    if not analyse_clients.empty:

        st.subheader(
            "🏆 Top 20 des clients par nombre d'OM"
        )

        st.dataframe(
            analyse_clients,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            analyse_clients.set_index("Client")
        )


# ============================================================
# ANALYSE CHAUFFEURS
# ============================================================

st.divider()

st.header("👷 Analyse des Chauffeurs")


if "Chauffeur" in df_analyse.columns:

    analyse_chauffeurs = (
        df_analyse["Chauffeur"]
        .replace("", "Non renseigné")
        .value_counts()
        .rename_axis("Chauffeur")
        .reset_index(name="Nombre OM")
    )

    analyse_chauffeurs = analyse_chauffeurs.head(20)

    if not analyse_chauffeurs.empty:

        st.subheader(
            "🏆 Top 20 des chauffeurs par nombre d'OM"
        )

        st.dataframe(
            analyse_chauffeurs,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            analyse_chauffeurs.set_index("Chauffeur")
        )


# ============================================================
# ANALYSE CAMIONS
# ============================================================

st.divider()

st.header("🚚 Analyse des Camions")


if "Numero Camion" in df_analyse.columns:

    analyse_camions = (
        df_analyse["Numero Camion"]
        .replace("", "Non renseigné")
        .value_counts()
        .rename_axis("Camion")
        .reset_index(name="Nombre OM")
    )

    analyse_camions = analyse_camions.head(20)

    if not analyse_camions.empty:

        st.subheader(
            "🏆 Top 20 des camions par nombre d'OM"
        )

        st.dataframe(
            analyse_camions,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            analyse_camions.set_index("Camion")
        )


# ============================================================
# ANALYSE TONNAGE
# ============================================================

st.divider()

st.header("📦 Analyse du chargement")


if "Tonnage" in df_analyse.columns:

    df_analyse["Tonnage"] = pd.to_numeric(
        df_analyse["Tonnage"],
        errors="coerce"
    )

    tonnage_total = (
        df_analyse["Tonnage"]
        .fillna(0)
        .sum()
    )

    tonnage_moyen = (
        df_analyse["Tonnage"]
        .dropna()
        .mean()
    )

else:

    tonnage_total = 0
    tonnage_moyen = 0


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "⚖️ Tonnage total",
        f"{tonnage_total:,.2f}"
    )


with col2:

    st.metric(
        "⚖️ Tonnage moyen / OM",
        f"{tonnage_moyen:,.2f}"
        if pd.notna(tonnage_moyen)
        else "0"
    )


# ============================================================
# ANALYSE DES LIEUX DE CHARGEMENT
# ============================================================

if "Lieu de Chargement" in df_analyse.columns:

    st.divider()

    st.header("📍 Lieux de chargement")

    analyse_chargement = (
        df_analyse["Lieu de Chargement"]
        .replace("", "Non renseigné")
        .value_counts()
        .rename_axis("Lieu de Chargement")
        .reset_index(name="Nombre OM")
    )

    analyse_chargement = analyse_chargement.head(20)

    if not analyse_chargement.empty:

        st.dataframe(
            analyse_chargement,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            analyse_chargement.set_index(
                "Lieu de Chargement"
            )
        )


# ============================================================
# ANALYSE DES LIEUX DE DÉCHARGEMENT
# ============================================================

if "Lieu de DéChargement" in df_analyse.columns:

    st.divider()

    st.header("📍 Lieux de déchargement")

    analyse_dechargement = (
        df_analyse["Lieu de DéChargement"]
        .replace("", "Non renseigné")
        .value_counts()
        .rename_axis("Lieu de Déchargement")
        .reset_index(name="Nombre OM")
    )

    analyse_dechargement = analyse_dechargement.head(20)

    if not analyse_dechargement.empty:

        st.dataframe(
            analyse_dechargement,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            analyse_dechargement.set_index(
                "Lieu de Déchargement"
            )
        )


# ============================================================
# INFORMATIONS SUR LE FICHIER CHAUFFEURS
# ============================================================

st.divider()

st.header("👷 Données du fichier Chauffeurs")


if not df_chauffeurs.empty:

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "👷 Total chauffeurs",
            len(df_chauffeurs)
        )

    with col2:

        if "Fonction" in df_chauffeurs.columns:

            nombre_fonctions = (
                df_chauffeurs["Fonction"]
                .replace("", pd.NA)
                .nunique()
            )

        else:

            nombre_fonctions = 0

        st.metric(
            "🪪 Fonctions",
            nombre_fonctions
        )

    with col3:

        if "Section/Affectation" in df_chauffeurs.columns:

            nombre_affectations = (
                df_chauffeurs["Section/Affectation"]
                .replace("", pd.NA)
                .nunique()
            )

        else:

            nombre_affectations = 0

        st.metric(
            "📍 Affectations",
            nombre_affectations
        )


else:

    st.warning(
        "⚠️ Le fichier Chauffeurs.xlsx n'est pas disponible."
    )


# ============================================================
# INFORMATIONS SUR LE FICHIER CLIENTS
# ============================================================

st.divider()

st.header("👥 Données du fichier Clients")


if not df_clients.empty:

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "👥 Total clients",
            len(df_clients)
        )

    with col2:

        if "Lieu de chargement" in df_clients.columns:

            nombre_lieux = (
                df_clients["Lieu de chargement"]
                .replace("", pd.NA)
                .nunique()
            )

        else:

            nombre_lieux = 0

        st.metric(
            "📍 Lieux de chargement",
            nombre_lieux
        )

else:

    st.warning(
        "⚠️ Le fichier Clients.xlsx n'est pas disponible."
    )


# ============================================================
# CONCLUSION
# ============================================================

st.divider()

st.header("📌 Résumé de l'activité")


st.info(
    f"""
    **Période analysée :**
    {periode[0] if periode and len(periode) == 2 else "Toutes les dates"}
    → {periode[1] if periode and len(periode) == 2 else "Toutes les dates"}

    **Ordres de Mission analysés :** {nombre_om}

    **Camions utilisés :** {nombre_camions}

    **Chauffeurs concernés :** {nombre_chauffeurs}

    **Clients concernés :** {nombre_clients}

    **Commandes de vente :** {nombre_commandes}

    **Montant des commandes HT :** {montant_commandes:,.2f} DA

    **Kilométrage total :** {km_total:,.0f} km
    """
)



# ============================================================
# ANALYSE CROISÉE OM / COMMANDES / CAMIONS / CHAUFFEURS
# ============================================================

st.divider()

st.header("🔗 Analyse croisée : Commandes de vente → OM → Camions → Chauffeurs")

st.caption(
    "Cette analyse rapproche les commandes de vente des Ordres de Mission "
    "à partir du numéro d'OM. Elle permet de suivre la chaîne "
    "Commande → OM → Camion → Chauffeur."
)

if df_commandes.empty:

    st.warning(
        "⚠️ Impossible de réaliser l'analyse croisée : "
        "Commande de vente.xlsx n'est pas disponible."
    )

else:

    # --------------------------------------------------------
    # PRÉPARATION DES CLÉS
    # --------------------------------------------------------

    def normaliser_cle(valeur):
        if pd.isna(valeur):
            return ""
        return (
            str(valeur)
            .strip()
            .upper()
            .replace(".0", "")
        )

    commandes_croisees = df_commandes_analyse.copy()
    om_croise = df_analyse.copy()

    # La commande contient "Ordre de Mission".
    # L'OM contient généralement "N° OM" ou une colonne similaire.
    colonne_om_commande = None
    for col in [
        "Ordre de Mission",
        "N° OM",
        "Numero OM",
        "Numéro OM",
        "OM"
    ]:
        if col in commandes_croisees.columns:
            colonne_om_commande = col
            break

    colonne_om = None
    for col in [
        "N° OM",
        "N° OM ",
        "Numero OM",
        "Numéro OM",
        "OM",
        "N°"
    ]:
        if col in om_croise.columns:
            colonne_om = col
            break

    # --------------------------------------------------------
    # CAS STANDARD : RAPPROCHEMENT PAR NUMÉRO D'OM
    # --------------------------------------------------------

    if colonne_om_commande and colonne_om:

        commandes_croisees["_CLE_OM"] = (
            commandes_croisees[colonne_om_commande]
            .apply(normaliser_cle)
        )

        om_croise["_CLE_OM"] = (
            om_croise[colonne_om]
            .apply(normaliser_cle)
        )

        # On ne garde pas les lignes sans OM
        commandes_avec_om = commandes_croisees[
            commandes_croisees["_CLE_OM"] != ""
        ].copy()

        om_avec_cle = om_croise[
            om_croise["_CLE_OM"] != ""
        ].copy()

        # Pour éviter les doublons côté OM,
        # une ligne de synthèse par OM est construite.
        colonnes_om_disponibles = [
            col for col in [
                "_CLE_OM",
                colonne_om,
                "Numero Camion",
                "Chauffeur",
                "Client",
                "Status",
                "Section",
                "Date Depart",
                "Kilometrage Parcouru",
                "Tonnage",
                "Lieu de Chargement",
                "Lieu de DéChargement"
            ]
            if col in om_avec_cle.columns
        ]

        om_reference = om_avec_cle[
            colonnes_om_disponibles
        ].copy()

        om_reference = om_reference.drop_duplicates(
            subset=["_CLE_OM"]
        )

        # ----------------------------------------------------
        # JOINTURE
        # ----------------------------------------------------

        analyse_croisee = commandes_avec_om.merge(
            om_reference,
            on="_CLE_OM",
            how="left",
            suffixes=("_Commande", "_OM")
        )

        # ----------------------------------------------------
        # INDICATEURS
        # ----------------------------------------------------

        total_commandes = (
            commandes_croisees[
                "N° document"
            ].replace("", pd.NA).nunique()
            if "N° document" in commandes_croisees.columns
            else len(commandes_croisees)
        )

        commandes_avec_om_count = (
            commandes_avec_om[
                "N° document"
            ].replace("", pd.NA).nunique()
            if "N° document" in commandes_avec_om.columns
            else len(commandes_avec_om)
        )

        commandes_sans_om_count = max(
            total_commandes - commandes_avec_om_count,
            0
        )

        oms_issus_commandes = (
            analyse_croisee["_CLE_OM"]
            .replace("", pd.NA)
            .dropna()
            .nunique()
        )

        camions_commandes = (
            analyse_croisee["Numero Camion"]
            .replace("", pd.NA)
            .dropna()
            .nunique()
            if "Numero Camion" in analyse_croisee.columns
            else 0
        )

        chauffeurs_commandes = (
            analyse_croisee["Chauffeur"]
            .replace("", pd.NA)
            .dropna()
            .nunique()
            if "Chauffeur" in analyse_croisee.columns
            else 0
        )

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric(
                "📦 Commandes",
                total_commandes
            )

        with col2:
            st.metric(
                "🔗 Commandes avec OM",
                commandes_avec_om_count
            )

        with col3:
            st.metric(
                "⏳ Commandes sans OM",
                commandes_sans_om_count
            )

        with col4:
            st.metric(
                "🚚 Camions liés",
                camions_commandes
            )

        with col5:
            st.metric(
                "👷 Chauffeurs liés",
                chauffeurs_commandes
            )

        # ----------------------------------------------------
        # TAUX DE TRANSFORMATION COMMANDE → OM
        # ----------------------------------------------------

        if total_commandes > 0:
            taux_om = (
                commandes_avec_om_count
                / total_commandes
                * 100
            )
        else:
            taux_om = 0

        st.subheader(
            "🎯 Taux de transformation Commande → OM"
        )

        st.metric(
            "Commandes transformées en OM",
            f"{taux_om:.1f} %"
        )

        # ----------------------------------------------------
        # CHARGE PAR CAMION
        # ----------------------------------------------------

        if "Numero Camion" in analyse_croisee.columns:

            st.subheader(
                "🚚 Activité des camions liée aux commandes"
            )

            analyse_camions_commandes = (
                analyse_croisee[
                    analyse_croisee["Numero Camion"]
                    .fillna("")
                    .astype(str)
                    .str.strip() != ""
                ]
                .groupby("Numero Camion")
                .agg(
                    Commandes=(
                        "N° document",
                        "nunique"
                    ) if "N° document" in analyse_croisee.columns
                    else ("_CLE_OM", "nunique"),
                    OM=(
                        "_CLE_OM",
                        "nunique"
                    ),
                    Tonnage=(
                        "Tonnage_Commande",
                        "sum"
                    ) if "Tonnage_Commande" in analyse_croisee.columns
                    else ("_CLE_OM", "size")
                )
                .reset_index()
                .sort_values(
                    "Commandes",
                    ascending=False
                )
                .head(20)
            )

            # Si la colonne Tonnage n'a pas été suffixée,
            # rechercher la colonne disponible.
            if "Tonnage" in analyse_croisee.columns:
                analyse_camions_commandes = (
                    analyse_croisee
                    .groupby("Numero Camion")
                    .agg(
                        Commandes=(
                            "N° document",
                            "nunique"
                        ) if "N° document" in analyse_croisee.columns
                        else ("_CLE_OM", "nunique"),
                        OM=("_CLE_OM", "nunique"),
                        Tonnage=("Tonnage", "sum")
                    )
                    .reset_index()
                    .sort_values(
                        "Commandes",
                        ascending=False
                    )
                    .head(20)
                )

            st.dataframe(
                analyse_camions_commandes,
                use_container_width=True,
                hide_index=True
            )

        # ----------------------------------------------------
        # CHARGE PAR CHAUFFEUR
        # ----------------------------------------------------

        if "Chauffeur" in analyse_croisee.columns:

            st.subheader(
                "👷 Activité des chauffeurs liée aux commandes"
            )

            analyse_chauffeurs_commandes = (
                analyse_croisee
                .groupby("Chauffeur")
                .agg(
                    Commandes=(
                        "N° document",
                        "nunique"
                    ) if "N° document" in analyse_croisee.columns
                    else ("_CLE_OM", "nunique"),
                    OM=(
                        "_CLE_OM",
                        "nunique"
                    )
                )
                .reset_index()
            )

            analyse_chauffeurs_commandes = (
                analyse_chauffeurs_commandes[
                    analyse_chauffeurs_commandes["Chauffeur"]
                    .fillna("")
                    .astype(str)
                    .str.strip() != ""
                ]
                .sort_values(
                    "Commandes",
                    ascending=False
                )
                .head(20)
            )

            st.dataframe(
                analyse_chauffeurs_commandes,
                use_container_width=True,
                hide_index=True
            )

        # ----------------------------------------------------
        # ANALYSE CLIENT / COMMANDE / OM
        # ----------------------------------------------------

        if "N° donneur d'ordre" in analyse_croisee.columns:

            st.subheader(
                "👥 Chaîne Client → Commande → OM → Ressources"
            )

            agregations = {
                "Commandes": (
                    "N° document",
                    "nunique"
                ) if "N° document" in analyse_croisee.columns
                else ("_CLE_OM", "nunique"),

                "OM": (
                    "_CLE_OM",
                    "nunique"
                )
            }

            if "Numero Camion" in analyse_croisee.columns:
                agregations["Camions"] = (
                    "Numero Camion",
                    "nunique"
                )

            if "Chauffeur" in analyse_croisee.columns:
                agregations["Chauffeurs"] = (
                    "Chauffeur",
                    "nunique"
                )

            if "Tonnage" in analyse_croisee.columns:
                agregations["Tonnage"] = (
                    "Tonnage",
                    "sum"
                )

            if "Montant ligne HT" in analyse_croisee.columns:
                agregations["Montant HT"] = (
                    "Montant ligne HT",
                    "sum"
                )

            analyse_clients_commandes = (
                analyse_croisee
                .groupby("N° donneur d'ordre")
                .agg(**{
                    nom: pd.NamedAgg(
                        column=col,
                        aggfunc=func
                    )
                    for nom, (col, func)
                    in agregations.items()
                })
                .reset_index()
            )

            analyse_clients_commandes = (
                analyse_clients_commandes
                .sort_values(
                    "Commandes",
                    ascending=False
                )
                .head(20)
            )

            st.dataframe(
                analyse_clients_commandes,
                use_container_width=True,
                hide_index=True
            )

        # ----------------------------------------------------
        # TABLEAU DE TRAÇABILITÉ
        # ----------------------------------------------------

        st.subheader(
            "🔎 Traçabilité complète Commande → OM → Camion → Chauffeur"
        )

        colonnes_trace = [
            "N° document",
            "N° ligne",
            "N° donneur d'ordre",
            "Désignation",
            "Trajet",
            "Produit Transporté",
            "Tonnage",
            "Montant ligne HT",
            colonne_om_commande,
            "Numero Camion",
            "Chauffeur",
            "Status",
            "Section",
            "Date Depart",
            "Kilometrage Parcouru"
        ]

        colonnes_trace = [
            col
            for col in colonnes_trace
            if col in analyse_croisee.columns
        ]

        tableau_trace = analyse_croisee[
            colonnes_trace
        ].copy()

        st.dataframe(
            tableau_trace,
            use_container_width=True,
            hide_index=True,
            height=550
        )

    else:

        # ----------------------------------------------------
        # CAS OÙ LE NOM DES COLONNES D'OM N'EST PAS IDENTIFIÉ
        # ----------------------------------------------------

        st.warning(
            "⚠️ Le rapprochement automatique Commande → OM "
            "n'a pas pu être effectué."
        )

        st.write(
            "Colonne OM trouvée dans Commande de vente :",
            colonne_om_commande or "Aucune"
        )

        st.write(
            "Colonne OM trouvée dans OM.xlsx :",
            colonne_om or "Aucune"
        )

        st.info(
            "Vérifiez que le numéro d'Ordre de Mission existe "
            "dans les deux fichiers avec une valeur commune."
        )

# ============================================================
# ACTUALISATION
# ============================================================
# ============================================================
# ACTUALISATION
# ============================================================

st.divider()

if st.button(
    "🔄 Actualiser les données",
    key="rapport_actualiser"
):

    st.cache_data.clear()
    st.rerun()
