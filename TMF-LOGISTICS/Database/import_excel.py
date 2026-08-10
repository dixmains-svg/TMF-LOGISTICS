import sqlite3
import pandas as pd
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

DATABASE_FILE = Path("database/tmf.db")


# ============================================================
# CONNEXION SQLITE
# ============================================================

def get_connection():
    DATABASE_FILE.parent.mkdir(exist_ok=True)

    return sqlite3.connect(
        DATABASE_FILE,
        check_same_thread=False
    )


# ============================================================
# IMPORTER UN EXCEL DANS SQLITE
# ============================================================

def importer_excel(fichier_excel, table):

    """
    Importe un fichier Excel dans une table SQLite.

    Paramètres :
        fichier_excel : fichier Excel
        table         : nom de la table SQLite
    """

    try:

        # Lire Excel
        df = pd.read_excel(
            fichier_excel,
            engine="openpyxl"
        )

        # Nettoyer les colonnes
        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        # Remplacer les valeurs NaN
        df = df.where(
            pd.notna(df),
            None
        )

        # Connexion SQLite
        conn = get_connection()

        # Importer dans SQLite
        df.to_sql(
            table,
            conn,
            if_exists="replace",
            index=False
        )

        conn.close()

        return True, len(df)

    except Exception as e:

        return False, str(e)


# ============================================================
# IMPORTER LES ORDRES DE MISSION
# ============================================================

def importer_ordres_mission(fichier):

    return importer_excel(
        fichier,
        "ordres_mission"
    )


# ============================================================
# IMPORTER LES CAMIONS
# ============================================================

def importer_camions(fichier):

    return importer_excel(
        fichier,
        "camions"
    )


# ============================================================
# IMPORTER LES CHAUFFEURS
# ============================================================

def importer_chauffeurs(fichier):

    return importer_excel(
        fichier,
        "chauffeurs"
    )


# ============================================================
# IMPORTER LES CLIENTS
# ============================================================

def importer_clients(fichier):

    return importer_excel(
        fichier,
        "clients"
    )


# ============================================================
# TEST DU PROGRAMME
# ============================================================

if __name__ == "__main__":

    print("===================================")
    print(" TMF LOGISTICS")
    print(" Import Excel → SQLite")
    print("===================================")

    fichier = input(
        "Nom du fichier Excel : "
    )

    table = input(
        "Nom de la table SQLite : "
    )

    succes, resultat = importer_excel(
        fichier,
        table
    )

    if succes:

        print(
            f"✅ Import terminé : {resultat} lignes."
        )

    else:

        print(
            f"❌ Erreur : {resultat}"
        )