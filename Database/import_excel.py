import sqlite3
import pandas as pd
from pathlib import Path


# ============================================================
# CHEMINS DU PROJET
# ============================================================

# import_excel.py se trouve dans :
# TMF-LOGISTICS/database/import_excel.py

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "Data"

DATABASE_DIR = BASE_DIR / "database"

DATABASE_FILE = DATABASE_DIR / "tmf.db"


# ============================================================
# CONNEXION SQLITE
# ============================================================

def get_connection():

    DATABASE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    return sqlite3.connect(
        DATABASE_FILE,
        check_same_thread=False
    )


# ============================================================
# LECTURE EXCEL
# ============================================================

def lire_excel(fichier_excel):

    fichier_excel = Path(fichier_excel)

    if not fichier_excel.exists():

        raise FileNotFoundError(
            f"Fichier Excel introuvable : {fichier_excel}"
        )

    # Vérifier OpenPyXL
    try:

        import openpyxl

    except ImportError:

        raise ImportError(
            "OpenPyXL n'est pas installé. "
            "Ajoutez openpyxl dans requirements.txt."
        )

    # Lire Excel
    df = pd.read_excel(
        fichier_excel,
        engine="openpyxl"
    )

    # Nettoyer les noms de colonnes
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    # Supprimer les lignes complètement vides
    df = df.dropna(
        how="all"
    )

    # Remplacer NaN par None
    df = df.astype(object).where(
        pd.notna(df),
        None
    )

    return df


# ============================================================
# IMPORT EXCEL → SQLITE
# ============================================================

def importer_excel(
    fichier_excel,
    table
):

    try:

        print()
        print("=" * 60)
        print("IMPORT EXCEL → SQLITE")
        print("=" * 60)

        print(
            f"📄 Fichier : {fichier_excel}"
        )

        print(
            f"🗄️ Table : {table}"
        )

        # ----------------------------------------------------
        # LIRE EXCEL
        # ----------------------------------------------------

        df = lire_excel(
            fichier_excel
        )

        print(
            f"📊 Lignes trouvées : {len(df)}"
        )

        print(
            f"📋 Colonnes : {len(df.columns)}"
        )

        # ----------------------------------------------------
        # CONNEXION SQLITE
        # ----------------------------------------------------

        conn = get_connection()

        # ----------------------------------------------------
        # IMPORTER DANS SQLITE
        # ----------------------------------------------------

        df.to_sql(
            table,
            conn,
            if_exists="replace",
            index=False
        )

        conn.commit()

        conn.close()

        print(
            f"✅ Import terminé : {len(df)} lignes"
        )

        return True, len(df)

    except Exception as e:

        print(
            f"❌ Erreur : {e}"
        )

        return False, str(e)


# ============================================================
# IMPORT ORDRES DE MISSION
# ============================================================

def importer_ordres_mission():

    fichier = DATA_DIR / "OM.xlsx"

    return importer_excel(
        fichier,
        "ordres_mission"
    )


# ============================================================
# IMPORT CAMIONS
# ============================================================

def importer_camions():

    fichier = DATA_DIR / "Camions.xlsx"

    return importer_excel(
        fichier,
        "camions"
    )


# ============================================================
# IMPORT CHAUFFEURS
# ============================================================

def importer_chauffeurs():

    fichier = DATA_DIR / "Chauffeurs.xlsx"

    return importer_excel(
        fichier,
        "chauffeurs"
    )


# ============================================================
# IMPORT CLIENTS
# ============================================================

def importer_clients():

    fichier = DATA_DIR / "Clients.xlsx"

    return importer_excel(
        fichier,
        "clients"
    )


# ============================================================
# IMPORTER TOUS LES FICHIERS
# ============================================================

def importer_toutes_les_donnees():

    resultats = {}

    # --------------------------------------------------------
    # ORDRES DE MISSION
    # --------------------------------------------------------

    succes, resultat = importer_ordres_mission()

    resultats["ordres_mission"] = (
        succes,
        resultat
    )

    # --------------------------------------------------------
    # CAMIONS
    # --------------------------------------------------------

    succes, resultat = importer_camions()

    resultats["camions"] = (
        succes,
        resultat
    )

    # --------------------------------------------------------
    # CHAUFFEURS
    # --------------------------------------------------------

    succes, resultat = importer_chauffeurs()

    resultats["chauffeurs"] = (
        succes,
        resultat
    )

    # --------------------------------------------------------
    # CLIENTS
    # --------------------------------------------------------

    succes, resultat = importer_clients()

    resultats["clients"] = (
        succes,
        resultat
    )

    return resultats


# ============================================================
# TEST DU PROGRAMME
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print(" TMF LOGISTICS")
    print(" IMPORT EXCEL → SQLITE")
    print("=" * 60)

    print()
    print(
        f"📁 Dossier Data : {DATA_DIR}"
    )

    print(
        f"🗄️ Base SQLite : {DATABASE_FILE}"
    )

    print()

    resultats = importer_toutes_les_donnees()

    print()
    print("=" * 60)
    print(" RÉSULTAT FINAL")
    print("=" * 60)

    for table, resultat in resultats.items():

        succes, valeur = resultat

        if succes:

            print(
                f"✅ {table} : {valeur} lignes"
            )

        else:

            print(
                f"❌ {table} : {valeur}"
            )

    print()
    print("✅ Import terminé.")
