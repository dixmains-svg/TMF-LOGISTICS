import pandas as pd
import streamlit as st
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

EXCEL_FILE = "DECOUCHE V1.4.xlsx"


# ============================================================
# CHARGER LE FICHIER EXCEL
# ============================================================

@st.cache_data(show_spinner=True)
def charger_excel():
    """
    Charge toutes les feuilles du fichier Excel.

    Retourne un dictionnaire contenant toutes les feuilles.
    Exemple :
        {
            "Input OM Fini": dataframe,
            "PASSAGE01": dataframe,
            "LISTE": dataframe,
            "Détails": dataframe
        }
    """

    fichier = Path(EXCEL_FILE)

    if not fichier.exists():
        raise FileNotFoundError(
            f"Le fichier '{EXCEL_FILE}' est introuvable."
        )

    feuilles = pd.read_excel(
        fichier,
        sheet_name=None,
        engine="openpyxl"
    )

    return feuilles


# ============================================================
# ORDRES DE MISSION
# ============================================================

@st.cache_data(show_spinner=False)
def get_om():

    feuilles = charger_excel()

    if "Input OM Fini" in feuilles:
        df = feuilles["Input OM Fini"].copy()
        df.columns = df.columns.astype(str).str.strip()
        return df

    # Si la feuille n'existe pas,
    # prendre la première feuille disponible
    if feuilles:
        df = list(feuilles.values())[0].copy()
        df.columns = df.columns.astype(str).str.strip()
        return df

    return pd.DataFrame()


# ============================================================
# PASSAGE
# ============================================================

@st.cache_data(show_spinner=False)
def get_passage():

    feuilles = charger_excel()

    if "PASSAGE01" in feuilles:
        df = feuilles["PASSAGE01"].copy()
        df.columns = df.columns.astype(str).str.strip()
        return df

    return pd.DataFrame()


# ============================================================
# LISTE
# ============================================================

@st.cache_data(show_spinner=False)
def get_liste():

    feuilles = charger_excel()

    if "LISTE" in feuilles:
        df = feuilles["LISTE"].copy()
        df.columns = df.columns.astype(str).str.strip()
        return df

    return pd.DataFrame()


# ============================================================
# DETAILS
# ============================================================

@st.cache_data(show_spinner=False)
def get_details():

    feuilles = charger_excel()

    if "Détails" in feuilles:
        df = feuilles["Détails"].copy()
        df.columns = df.columns.astype(str).str.strip()
        return df

    return pd.DataFrame()


# ============================================================
# RECHERCHE
# ============================================================

def recherche(df, texte):

    if df is None or df.empty:
        return df

    if not texte:
        return df

    masque = (
        df.astype(str)
        .apply(
            lambda col: col.str.contains(
                texte,
                case=False,
                na=False
            )
        )
        .any(axis=1)
    )

    return df[masque]


# ============================================================
# STATISTIQUES
# ============================================================

def statistiques(df):

    if df is None or df.empty:
        return {
            "lignes": 0,
            "colonnes": 0,
            "colonnes_noms": []
        }

    return {
        "lignes": len(df),
        "colonnes": len(df.columns),
        "colonnes_noms": list(df.columns)
    }