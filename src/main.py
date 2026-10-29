#!/usr/bin/env python3
import sys
import os
import sqlite3

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.helpers import clear_screen

def init_db():
    """Crée les tables et ajoute les nouvelles colonnes si nécessaire."""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/stock_management.db")
    cursor = conn.cursor()
    
    # 1. Création des tables de base (si elles n'existent pas)
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT, sku TEXT UNIQUE NOT NULL,
                barcode TEXT, name TEXT NOT NULL, description TEXT, category TEXT,
                brand TEXT, unit TEXT DEFAULT 'carton', purchase_price REAL,
                sale_price_ht REAL, sale_price_ttc REAL, tax_rate REAL DEFAULT 20.0,
                alert_threshold REAL DEFAULT 10.0, safety_stock REAL DEFAULT 5.0,
                location TEXT, current_stock REAL DEFAULT 0.0, cump REAL DEFAULT 0.0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
                
    cursor.execute('''CREATE TABLE IF NOT EXISTS stock_movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER NOT NULL,
                movement_type TEXT NOT NULL, quantity REAL NOT NULL, unit_cost REAL,
                movement_date DATETIME DEFAULT CURRENT_TIMESTAMP, user_id TEXT NOT NULL,
                reason TEXT NOT NULL, reference TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_id TEXT NOT NULL,
                action TEXT NOT NULL,
                entity_type TEXT NOT NULL,
                entity_id INTEGER NOT NULL,
                old_value TEXT,
                new_value TEXT,
                reason TEXT)''')

    # 2. AJOUT DES NOUVELLES COLONNES (Sécurisé pour les anciennes bases de données)
    try:
        # Ajoute le nombre d'unités par carton dans la fiche produit
        cursor.execute("ALTER TABLE products ADD COLUMN units_per_carton INTEGER DEFAULT 1")
        
        # Ajoute le numéro de carton/lot dans les mouvements de stock
        cursor.execute("ALTER TABLE stock_movements ADD COLUMN carton_number TEXT DEFAULT ''")
        
        # Ajoute le nombre d'unités par carton dans les mouvements de stock
        cursor.execute("ALTER TABLE stock_movements ADD COLUMN units_per_carton INTEGER DEFAULT 1")
        
        conn.commit()
        print("✅ Base de données mise à jour avec les champs 'carton'.")
    except Exception:
        # Si les colonnes existent déjà, SQLite renvoie une erreur qu'on ignore
        pass 
                
    conn.commit()
    conn.close()

def main():
    init_db()
    
    from src.ui.login import login_screen, logout_user
    from src.ui.product_menu import ProductMenu
    from src.ui.stock_menu import StockMenu
    from src.ui.dashboard import DashboardMenu
    from src.ui.reports_menu import ReportsMenu
    from src.services.audit_service import view_audit_logs
    from src.utils.session import get_user

    clear_screen()
    if not login_screen():
        return

    while True:
        user = get_user()
        clear_screen()
        print("\n" + "="*40)
        print(f" CONNECTÉ EN TANT QUE: {user['username']} ({user['role']})")
        print("="*40)
        print("1. Gestion des Produits")
        print("2. Mouvements de Stock")
        print("3. Tableau de Bord Financier")
        print("4. Rapports & Export")
        if user['role'] == 'Administrator':
            print("5. Journaux d'Audit (Admin Seulement)")
        print("0. Déconnexion")
        print("="*40)
        
        choice = input("Choix: ")
        
        if choice == '1':
            ProductMenu().show_menu()
        elif choice == '2':
            StockMenu().show_menu()
        elif choice == '3':
            DashboardMenu().show_menu()
        elif choice == '4':
            ReportsMenu().show_menu()
        elif choice == '5' and user['role'] == 'Administrator':
            clear_screen()
            view_audit_logs()
            input("\nAppuyez sur Entrée pour revenir au menu...")
        elif choice == '0':
            clear_screen()
            logout_user()
            break
        else:
            print("❌ Option invalide ou accès refusé.")
            input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
