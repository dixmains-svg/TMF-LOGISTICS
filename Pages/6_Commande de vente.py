import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO

# ============================================================
# 6_Commande de vente.py
# Page Streamlit - Commandes de vente
# Fichier source : Commande de vente.xlsx
# ============================================================

st.set_page_config(
    page_title="Commandes de vente",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
FICHIER_EXCEL = BASE_DIR / "Commande de vente.xlsx"
FEUILLE = "Feuil1"


# ------------------------------------------------------------
# CHARGEMENT DES DONNÉES
# ------------------------------------------------------------

@st.cache_data(show_spinner=False)
def charger_commandes(fichier):
    """Charge le fichier Excel des commandes de vente."""
    df = pd.read_excel(fichier, sheet_name=FEUILLE)

    # Nettoyage des noms de colonnes
    df.columns = [str(col).strip() for col in df.columns]

    # Conversion des dates
    colonnes_dates = [
        "Date de Mission",
        "Date Heure Charg Planif"
    ]

    for col in colonnes_dates:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Conversion numérique
    colonnes_numeriques = [
        "Prix unitaire",
        "Quantité restante",
        "Tonnage",
        "Montant ligne HT",
        "Quantité",
        "Quantité réservée (base)"
    ]

    for col in colonnes_numeriques:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


# ------------------------------------------------------------
# VÉRIFICATION DU FICHIER
# ------------------------------------------------------------

if not FICHIER_EXCEL.exists():
    st.error(
        f"❌ Le fichier **{FICHIER_EXCEL.name}** est introuvable.\n\n"
        "Placez le fichier Excel dans le même dossier que "
        "`6_Commande de vente.py`."
    )
    st.stop()


try:
    df = charger_commandes(str(FICHIER_EXCEL))
except Exception as e:
    st.error(f"❌ Erreur lors de la lecture du fichier Excel : {e}")
    st.stop()


# ------------------------------------------------------------
# TITRE
# ------------------------------------------------------------

st.title("📦 Commandes de vente")
st.caption(
    f"Source : {FICHIER_EXCEL.name} | "
    f"Feuille : {FEUILLE} | "
    f"{len(df):,} lignes".replace(",", " ")
)


# ------------------------------------------------------------
# INDICATEURS
# ------------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

nb_lignes = len(df)

if "N° document" in df.columns:
    nb_commandes = df["N° document"].dropna().nunique()
else:
    nb_commandes = 0

if "Ordre de Mission" in df.columns:
    nb_om = df["Ordre de Mission"].dropna().nunique()
else:
    nb_om = 0

if "Montant ligne HT" in df.columns:
    montant_total = pd.to_numeric(
        df["Montant ligne HT"], errors="coerce"
    ).fillna(0).sum()
else:
    montant_total = 0

col1.metric("📋 Lignes", f"{nb_lignes:,}".replace(",", " "))
col2.metric("📄 Commandes", f"{nb_commandes:,}".replace(",", " "))
col3.metric("🚚 Ordres de mission", f"{nb_om:,}".replace(",", " "))
col4.metric("💰 Montant HT", f"{montant_total:,.2f} DA".replace(",", " "))


st.divider()


# ------------------------------------------------------------
# SIDEBAR - FILTRES
# ------------------------------------------------------------

st.sidebar.header("🔎 Filtres")

# Recherche générale
recherche = st.sidebar.text_input(
    "Recherche",
    placeholder="Commande, client, trajet, OM, BL..."
)

# Code convention
if "Code Convention" in df.columns:
    conventions = sorted(
        df["Code Convention"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )
    choix_convention = st.sidebar.multiselect(
        "Code Convention",
        conventions
    )
else:
    choix_convention = []

# Type document
if "Type document" in df.columns:
    types_document = sorted(
        df["Type document"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )
    choix_type_document = st.sidebar.multiselect(
        "Type document",
        types_document
    )
else:
    choix_type_document = []

# Donneur d'ordre
if "N° donneur d'ordre" in df.columns:
    donneurs = sorted(
        df["N° donneur d'ordre"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )
    choix_donneur = st.sidebar.multiselect(
        "N° donneur d'ordre",
        donneurs
    )
else:
    choix_donneur = []

# OM généré
if "OM Generé" in df.columns:
    choix_om = st.sidebar.selectbox(
        "OM généré",
        ["Tous", "Oui", "Non"]
    )
else:
    choix_om = "Tous"

# Date de mission
if "Date de Mission" in df.columns:
    dates_valides = df["Date de Mission"].dropna()

    if not dates_valides.empty:
        date_min = dates_valides.min().date()
        date_max = dates_valides.max().date()

        plage_dates = st.sidebar.date_input(
            "Date de mission",
            value=(date_min, date_max),
            min_value=date_min,
            max_value=date_max
        )
    else:
        plage_dates = None
else:
    plage_dates = None


# ------------------------------------------------------------
# APPLICATION DES FILTRES
# ------------------------------------------------------------

df_filtre = df.copy()

# Recherche
if recherche.strip():
    terme = recherche.strip().lower()

    masque = pd.Series(False, index=df_filtre.index)

    colonnes_recherche = [
        "N° document",
        "N° donneur d'ordre",
        "N°",
        "Désignation",
        "Trajet",
        "Lieu de Chargement",
        "Lieu Déchargement",
        "Produit Transporté",
        "BL Client M1",
        "Ordre de Mission",
        "Code Vehicule",
        "Code Rotation"
    ]

    for col in colonnes_recherche:
        if col in df_filtre.columns:
            masque = masque | (
                df_filtre[col]
                .fillna("")
                .astype(str)
                .str.lower()
                .str.contains(terme, regex=False)
            )

    df_filtre = df_filtre[masque]


# Convention
if choix_convention and "Code Convention" in df_filtre.columns:
    df_filtre = df_filtre[
        df_filtre["Code Convention"]
        .astype(str)
        .isin(choix_convention)
    ]


# Type document
if choix_type_document and "Type document" in df_filtre.columns:
    df_filtre = df_filtre[
        df_filtre["Type document"]
        .astype(str)
        .isin(choix_type_document)
    ]


# Donneur d'ordre
if choix_donneur and "N° donneur d'ordre" in df_filtre.columns:
    df_filtre = df_filtre[
        df_filtre["N° donneur d'ordre"]
        .astype(str)
        .isin(choix_donneur)
    ]


# OM généré
if choix_om != "Tous" and "OM Generé" in df_filtre.columns:
    if choix_om == "Oui":
        df_filtre = df_filtre[
            df_filtre["OM Generé"].astype(str).str.lower().isin(
                ["true", "1", "oui"]
            )
        ]
    else:
        df_filtre = df_filtre[
            ~df_filtre["OM Generé"].astype(str).str.lower().isin(
                ["true", "1", "oui"]
            )
        ]


# Date
if (
    plage_dates
    and isinstance(plage_dates, tuple)
    and len(plage_dates) == 2
    and "Date de Mission" in df_filtre.columns
):
    date_debut, date_fin = plage_dates

    df_filtre = df_filtre[
        df_filtre["Date de Mission"].dt.date.between(
            date_debut,
            date_fin
        )
    ]


# ------------------------------------------------------------
# RÉSUMÉ APRÈS FILTRES
# ------------------------------------------------------------

st.subheader("📊 Résultat de la recherche")

r1, r2, r3 = st.columns(3)

r1.metric(
    "Lignes affichées",
    f"{len(df_filtre):,}".replace(",", " ")
)

if "N° document" in df_filtre.columns:
    r2.metric(
        "Commandes",
        f"{df_filtre['N° document'].dropna().nunique():,}".replace(",", " ")
    )
else:
    r2.metric("Commandes", "0")

if "Montant ligne HT" in df_filtre.columns:
    montant_filtre = pd.to_numeric(
        df_filtre["Montant ligne HT"],
        errors="coerce"
    ).fillna(0).sum()
else:
    montant_filtre = 0

r3.metric(
    "Montant HT filtré",
    f"{montant_filtre:,.2f} DA".replace(",", " ")
)


# ------------------------------------------------------------
# COLONNES PRINCIPALES À AFFICHER
# ------------------------------------------------------------

colonnes_affichage = [
    "Code Convention",
    "Code Vehicule",
    "Date de Mission",
    "N° document",
    "N° ligne",
    "Code Rotation",
    "Type document",
    "N° donneur d'ordre",
    "Type",
    "N°",
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
    "Retour A Charge",
    "Jumelée",
    "Tonnage",
    "Ordre de Mission",
    "Code Activité",
    "Code magasin",
    "Code unité",
    "Code variante",
    "Montant ligne HT",
    "Quantité",
    "Quantité réservée (base)",
    "Réserver"
]

colonnes_affichage = [
    col for col in colonnes_affichage
    if col in df_filtre.columns
]

tableau = df_filtre[colonnes_affichage].copy()


# ------------------------------------------------------------
# FORMAT DES DATES
# ------------------------------------------------------------

for col in ["Date de Mission", "Date Heure Charg Planif"]:
    if col in tableau.columns:
        tableau[col] = tableau[col].dt.strftime(
            "%d/%m/%Y %H:%M" if col == "Date Heure Charg Planif"
            else "%d/%m/%Y"
        )


# ------------------------------------------------------------
# FORMAT DES MONTANTS
# ------------------------------------------------------------

for col in ["Prix unitaire", "Montant ligne HT"]:
    if col in tableau.columns:
        tableau[col] = pd.to_numeric(
            tableau[col], errors="coerce"
        ).round(2)


# ------------------------------------------------------------
# AFFICHAGE
# ------------------------------------------------------------

st.dataframe(
    tableau,
    use_container_width=True,
    hide_index=True,
    height=620
)


# ------------------------------------------------------------
# EXPORT EXCEL DES DONNÉES FILTRÉES
# ------------------------------------------------------------

st.divider()

st.subheader("📥 Export")

buffer = BytesIO()

with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    df_filtre.to_excel(
        writer,
        index=False,
        sheet_name="Commandes filtrées"
    )

st.download_button(
    label="📥 Télécharger les commandes filtrées",
    data=buffer.getvalue(),
    file_name="Commandes_de_vente_filtrees.xlsx",
    mime=(
        "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet"
    )
)


# ------------------------------------------------------------
# INFORMATIONS
# ------------------------------------------------------------

with st.expander("ℹ️ Informations sur les données"):
    st.write(f"**Fichier :** {FICHIER_EXCEL.name}")
    st.write(f"**Feuille :** {FEUILLE}")
    st.write(f"**Nombre total de lignes :** {len(df):,}".replace(",", " "))
    st.write(
        f"**Nombre de lignes après filtrage :** "
        f"{len(df_filtre):,}".replace(",", " ")
    )
    st.write(f"**Nombre de colonnes :** {len(df.columns)}")
