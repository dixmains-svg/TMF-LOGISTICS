import streamlit as st
import pandas as pd

# ==========================================
# 1. DÉFINITION DES FILTRES EN SIDEBAR
# ==========================================

st.sidebar.header("🔍 Filtres de recherche")

# --- A. FILTRE PAR MOIS ---
MOIS_LISTE = [
    "Tous les mois",
    "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
]

mois_selectionne = st.sidebar.selectbox("📅 Sélectionner un mois", MOIS_LISTE)

# Mapping des mois vers leurs numéros respectifs (1 à 12)
MOIS_MAP = {
    "Janvier": 1, "Février": 2, "Mars": 3, "Avril": 4, "Mai": 5, "Juin": 6,
    "Juillet": 7, "Août": 8, "Septembre": 9, "Octobre": 10, "Novembre": 11, "Décembre": 12
}

# --- B. FILTRE PAR AFFECTATION ---
AFFECTATIONS_LISTE = ["Toutes les affectations", "Akbou", "Setif", "Alger", "Oran"]
affectation_selectionnee = st.sidebar.selectbox("📍 Affectation / Agence", AFFECTATIONS_LISTE)

# --- C. FILTRE PAR NUMÉRO DE CAMION ---
# Exemple de recherche de la colonne des camions dans un dataframe (ex: df_flotte ou df_om)
def get_camions_list(df, keywords=["immatriculation", "camion", "vehicule", "code camion", "code"]):
    col = find_column_by_keywords(df, keywords)
    if col and not df.empty:
        camions = df[col].dropna().astype(str).unique().tolist()
        camions.sort()
        return camions
    return []

# Récupération de la liste dynamique des camions
liste_camions = ["Tous les camions"]
# Remplacez 'df_flotte' par votre DataFrame contenant la flotte ou les ordres de mission
if 'df_flotte' in locals() and not df_flotte.empty:
    liste_camions += get_camions_list(df_flotte)
elif 'df_om' in locals() and not df_om.empty:
    liste_camions += get_camions_list(df_om)

camion_selectionne = st.sidebar.selectbox("🚛 Numéro de Camion", liste_camions)


# ==========================================
# 2. FONCTIONS DE FILTRAGE DES DATAFRAMES
# ==========================================

def filter_by_month(df, keywords, month_name):
    """Filtre un DataFrame selon le mois sélectionné."""
    if df.empty or month_name == "Tous les mois":
        return df
    
    col = find_column_by_keywords(df, keywords)
    if col:
        try:
            dates = pd.to_datetime(df[col], errors='coerce')
            target_month = MOIS_MAP[month_name]
            return df[dates.dt.month == target_month]
        except Exception:
            return df
    return df

def filter_by_affectation(df, keywords, affectation):
    """Filtre un DataFrame selon l'affectation choisie."""
    if df.empty or affectation == "Toutes les affectations":
        return df
    
    col = find_column_by_keywords(df, keywords)
    if col:
        return df[df[col].astype(str).str.contains(affectation, case=False, na=False)]
    return df

def filter_by_camion(df, keywords, camion):
    """Filtre un DataFrame selon le numéro du camion."""
    if df.empty or camion == "Tous les camions":
        return df
    
    col = find_column_by_keywords(df, keywords)
    if col:
        return df[df[col].astype(str) == str(camion)]
    return df

# ==========================================
# 3. APPLICATION DES FILTRES AUX DATAFRAMES
# ==========================================

# Exemple d'application sur vos DataFrames principaux :
# (Ajustez les mots-clés selon les entêtes réels de vos fichiers Excel)

if 'df_om' in locals() and not df_om.empty:
    df_om_filtered = filter_by_month(df_om, ["date", "date om", "date_depart"], mois_selectionne)
    df_om_filtered = filter_by_affectation(df_om_filtered, ["agence", "affectation", "site", "depot"], affectation_selectionnee)
    df_om_filtered = filter_by_camion(df_om_filtered, ["camion", "immatriculation", "code camion"], camion_selectionne)

if 'df_flotte' in locals() and not df_flotte.empty:
    df_flotte_filtered = filter_by_affectation(df_flotte, ["agence", "affectation", "site"], affectation_selectionnee)
    df_flotte_filtered = filter_by_camion(df_flotte_filtered, ["camion", "immatriculation", "code camion"], camion_selectionne)
