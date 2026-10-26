#!/usr/bin/env python3
import sys
import os
import sqlite3

# Ensure we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def init_db():
    """Ensure DB and tables exist"""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/stock_management.db")
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT, sku TEXT UNIQUE NOT NULL,
                barcode TEXT, name TEXT NOT NULL, description TEXT, category TEXT,
                brand TEXT, unit TEXT DEFAULT 'piece', purchase_price REAL,
                sale_price_ht REAL, sale_price_ttc REAL, tax_rate REAL DEFAULT 20.0,
                alert_threshold REAL DEFAULT 10.0, safety_stock REAL DEFAULT 5.0,
                location TEXT, current_stock REAL DEFAULT 0.0, cump REAL DEFAULT 0.0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
                
    cursor.execute('''CREATE TABLE IF NOT EXISTS stock_movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER NOT NULL,
                movement_type TEXT NOT NULL, quantity REAL NOT NULL, unit_cost REAL,
                movement_date DATETIME DEFAULT CURRENT_TIMESTAMP, user_id TEXT NOT NULL,
                reason TEXT NOT NULL, reference TEXT)''')
                
    conn.commit()
    conn.close()

def main():
    init_db()
    from src.ui.product_menu import ProductMenu
    from src.ui.stock_menu import StockMenu
    from src.ui.dashboard import DashboardMenu
    
    print("\n" + "="*40)
    print(" ENTERPRISE INVENTORY MANAGER")
    print("="*40)
    
    while True:
        print("\n1. Manage Products")
        print("2. Stock Movements")
        print("3. Financial Dashboard")
        print("0. Exit")
        choice = input("Choice: ")
        
        if choice == '1':
            ProductMenu().show_menu()
        elif choice == '2':
            StockMenu().show_menu()
        elif choice == '3':
            DashboardMenu().show_menu()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
