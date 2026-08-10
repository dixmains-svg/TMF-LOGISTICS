import sqlite3
import pandas as pd
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

DATABASE_DIR = Path("database")
DATABASE_FILE = DATABASE_DIR / "tmf.db"


# ============================================================
# CONNEXION À LA BASE
# ============================================================

def get_connection():
    """
    Retourne une connexion à la base SQLite.
    """

    DATABASE_DIR.mkdir(exist_ok=True)

    conn = sqlite3.connect(
        DATABASE_FILE,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    return conn


# ============================================================
# INITIALISATION DE LA BASE
# ============================================================

def init_database():

    conn = get_connection()
    cursor = conn.cursor()

    # --------------------------------------------------------
    # TABLE ORDRES DE MISSION
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ordres_mission (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            numero_om TEXT,
            commande TEXT,
            camion TEXT,
            remorque TEXT,
            chauffeur TEXT,
            client TEXT,
            mission TEXT,

            date_depart TEXT,
            heure_depart TEXT,

            date_retour TEXT,
            heure_retour TEXT,

            km_depart REAL,
            km_retour REAL,
            km_parcourus REAL,

            statut TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # --------------------------------------------------------
    # TABLE CAMIONS
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS camions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            camion TEXT UNIQUE,
            remorque TEXT,
            chauffeur TEXT,
            statut TEXT,
            client TEXT,
            mission TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # --------------------------------------------------------
    # TABLE CHAUFFEURS
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chauffeurs (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            badge TEXT,
            chauffeur TEXT,
            fonction TEXT,
            section_affectation TEXT,
            superviseur TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # --------------------------------------------------------
    # TABLE CLIENTS
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            code_client TEXT UNIQUE,
            client TEXT,
            ville TEXT,
            adresse TEXT,
            telephone TEXT,
            email TEXT,
            contact TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# ============================================================
# ORDRES DE MISSION
# ============================================================

def get_ordres_mission():

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM ordres_mission ORDER BY id DESC",
        conn
    )

    conn.close()

    return df


def ajouter_ordre_mission(data):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ordres_mission (
            numero_om,
            commande,
            camion,
            remorque,
            chauffeur,
            client,
            mission,
            date_depart,
            heure_depart,
            date_retour,
            heure_retour,
            km_depart,
            km_retour,
            km_parcourus,
            statut
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("numero_om"),
        data.get("commande"),
        data.get("camion"),
        data.get("remorque"),
        data.get("chauffeur"),
        data.get("client"),
        data.get("mission"),
        data.get("date_depart"),
        data.get("heure_depart"),
        data.get("date_retour"),
        data.get("heure_retour"),
        data.get("km_depart"),
        data.get("km_retour"),
        data.get("km_parcourus"),
        data.get("statut")
    ))

    conn.commit()
    conn.close()


# ============================================================
# CAMIONS
# ============================================================

def get_camions():

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM camions ORDER BY id",
        conn
    )

    conn.close()

    return df


def ajouter_camion(
    camion,
    remorque="",
    chauffeur="",
    statut="",
    client="",
    mission=""
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO camions (
            camion,
            remorque,
            chauffeur,
            statut,
            client,
            mission
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        camion,
        remorque,
        chauffeur,
        statut,
        client,
        mission
    ))

    conn.commit()
    conn.close()


# ============================================================
# CHAUFFEURS
# ============================================================

def get_chauffeurs():

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM chauffeurs ORDER BY id",
        conn
    )

    conn.close()

    return df


def ajouter_chauffeur(
    badge,
    chauffeur,
    fonction="",
    section_affectation="",
    superviseur=""
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO chauffeurs (
            badge,
            chauffeur,
            fonction,
            section_affectation,
            superviseur
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        badge,
        chauffeur,
        fonction,
        section_affectation,
        superviseur
    ))

    conn.commit()
    conn.close()


# ============================================================
# CLIENTS
# ============================================================

def get_clients():

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM clients ORDER BY id",
        conn
    )

    conn.close()

    return df


def ajouter_client(
    code_client,
    client,
    ville="",
    adresse="",
    telephone="",
    email="",
    contact=""
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO clients (
            code_client,
            client,
            ville,
            adresse,
            telephone,
            email,
            contact
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        code_client,
        client,
        ville,
        adresse,
        telephone,
        email,
        contact
    ))

    conn.commit()
    conn.close()


# ============================================================
# STATISTIQUES
# ============================================================

def statistiques():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM ordres_mission"
    )
    nombre_om = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM camions"
    )
    nombre_camions = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM chauffeurs"
    )
    nombre_chauffeurs = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM clients"
    )
    nombre_clients = cursor.fetchone()[0]

    conn.close()

    return {
        "ordres_mission": nombre_om,
        "camions": nombre_camions,
        "chauffeurs": nombre_chauffeurs,
        "clients": nombre_clients
    }


# ============================================================
# SUPPRESSION
# ============================================================

def supprimer_camion(id_camion):

    conn = get_connection()

    conn.execute(
        "DELETE FROM camions WHERE id = ?",
        (id_camion,)
    )

    conn.commit()
    conn.close()


def supprimer_chauffeur(id_chauffeur):

    conn = get_connection()

    conn.execute(
        "DELETE FROM chauffeurs WHERE id = ?",
        (id_chauffeur,)
    )

    conn.commit()
    conn.close()


def supprimer_client(id_client):

    conn = get_connection()

    conn.execute(
        "DELETE FROM clients WHERE id = ?",
        (id_client,)
    )

    conn.commit()
    conn.close()


def supprimer_ordre_mission(id_om):

    conn = get_connection()

    conn.execute(
        "DELETE FROM ordres_mission WHERE id = ?",
        (id_om,)
    )

    conn.commit()
    conn.close()


# ============================================================
# LANCEMENT DIRECT
# ============================================================

if __name__ == "__main__":

    init_database()

    print("===================================")
    print(" TMF LOGISTICS - DATABASE")
    print("===================================")
    print(f"Base créée : {DATABASE_FILE}")
    print("Tables créées avec succès.")