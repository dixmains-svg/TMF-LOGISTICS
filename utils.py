import pandas as pd
import streamlit as st
from pathlib import Path

# Nom du fichier Excel
EXCEL_FILE = "DECOUCHE V1.4.xlsx"


@st.cache_data(show_spinner=True)
def charger_excel():
    """
    Charge toutes les feuilles du fichier Excel.
    Retourne un dictionnaire :
        {
            "Input OM Fini": dataframe,
            "PASSAGE01": dataframe,
            ...
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


@st.cache_data(show_spinner=False)
def get_om():
    feuilles = charger_excel()

    if "Input OM Fini" in feuilles:
        return feuilles["Input OM Fini"]

    return list(feuilles.values())[0]


@st.cache_data(show_spinner=False)
def get_passage():
    feuilles = charger_excel()

    if "PASSAGE01" in feuilles:
        return feuilles["PASSAGE01"]

    return pd.DataFrame()


@st.cache_data(show_spinner=False)
def get_liste():
    feuilles = charger_excel()

    if "LISTE" in feuilles:
        return feuilles["LISTE"]

    return pd.DataFrame()


@st.cache_data(show_spinner=False)
def get_details():
    feuilles = charger_excel()

    if "Détails" in feuilles:
        return feuilles["Détails"]

    return pd.DataFrame()


def recherche(df, texte):

    if texte == "":
        return df

    masque = (
        df.astype(str)
          .apply(lambda col: col.str.contains(
              texte,
              case=False,
              na=False))
          .any(axis=1)
    )

    return df[masque]


def statistiques(df):

    return {
        "lignes": len(df),
        "colonnes": len(df.columns),
        "colonnes_noms": list(df.columns)
    }