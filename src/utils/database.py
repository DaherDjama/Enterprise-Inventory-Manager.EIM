import sqlite3
import os

DB_PATH = "data/stock_management.db"

def get_connection():
    """Retourne une connexion à la base de données avec row_factory activé."""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    # Active le mode "dictionnaire" pour accéder aux colonnes par leur nom
    conn.row_factory = sqlite3.Row
    return conn
