import sqlite3
import os

# Ensure data directory exists
os.makedirs("data", exist_ok=True)
DB_PATH = "data/stock_management.db"

def get_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn
