#!/usr/bin/env python3
import sys
import os
import sqlite3

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def init_db():
    """Ensure DB and ALL tables exist"""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/stock_management.db")
    cursor = conn.cursor()
    
    # 1. Products Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT, sku TEXT UNIQUE NOT NULL,
                barcode TEXT, name TEXT NOT NULL, description TEXT, category TEXT,
                brand TEXT, unit TEXT DEFAULT 'piece', purchase_price REAL,
                sale_price_ht REAL, sale_price_ttc REAL, tax_rate REAL DEFAULT 20.0,
                alert_threshold REAL DEFAULT 10.0, safety_stock REAL DEFAULT 5.0,
                location TEXT, current_stock REAL DEFAULT 0.0, cump REAL DEFAULT 0.0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
                
    # 2. Stock Movements Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS stock_movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER NOT NULL,
                movement_type TEXT NOT NULL, quantity REAL NOT NULL, unit_cost REAL,
                movement_date DATETIME DEFAULT CURRENT_TIMESTAMP, user_id TEXT NOT NULL,
                reason TEXT NOT NULL, reference TEXT)''')

    # 3. Users Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    # 4. Audit Logs Table
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

    if not login_screen():
        return

    while True:
        user = get_user()
        print("\n" + "="*40)
        print(f" LOGGED IN AS: {user['username']} ({user['role']})")
        print("="*40)
        print("1. Manage Products")
        print("2. Stock Movements")
        print("3. Financial Dashboard")
        print("4. Reports & Export")
        if user['role'] == 'Administrator':
            print("5. View Audit Logs (Admin Only)")
        print("0. Logout")
        
        choice = input("Choice: ")
        
        if choice == '1':
            ProductMenu().show_menu()
        elif choice == '2':
            StockMenu().show_menu()
        elif choice == '3':
            DashboardMenu().show_menu()
        elif choice == '4':
            ReportsMenu().show_menu()
        elif choice == '5' and user['role'] == 'Administrator':
            view_audit_logs()
        elif choice == '0':
            logout_user()
            break
        else:
            print("Invalid option or access denied.")

if __name__ == "__main__":
    main()
