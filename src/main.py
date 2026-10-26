#!/usr/bin/env python3
"""
Enterprise Inventory Manager (EIM)
Desktop inventory management application
Built with Python/SQLite for Windows 10 32-bit
"""

import sqlite3
import os
from datetime import datetime

class StockManager:
    def __init__(self):
        self.db_path = "data/stock_management.db"
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with all tables"""
        os.makedirs("data", exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sku TEXT UNIQUE NOT NULL,
                barcode TEXT,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT,
                brand TEXT,
                unit TEXT DEFAULT 'piece',
                purchase_price REAL,
                sale_price_ht REAL,
                sale_price_ttc REAL,
                tax_rate REAL DEFAULT 20.0,
                alert_threshold REAL DEFAULT 10.0,
                safety_stock REAL DEFAULT 5.0,
                location TEXT,
                current_stock REAL DEFAULT 0.0,
                cump REAL DEFAULT 0.0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Stock movements table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                movement_type TEXT NOT NULL,
                quantity REAL NOT NULL,
                unit_cost REAL,
                movement_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_id TEXT NOT NULL,
                reason TEXT NOT NULL,
                reference TEXT,
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        ''')
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Audit logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_id TEXT NOT NULL,
                action TEXT NOT NULL,
                entity_type TEXT NOT NULL,
                entity_id INTEGER NOT NULL,
                old_value TEXT,
                new_value TEXT,
                reason TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully!")
    
    def test_connection(self):
        """Test database connection"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"✅ Connection successful! Tables created: {len(tables)}")
            for table in tables:
                print(f"   - {table[0]}")
            conn.close()
            return True
        except Exception as e:
            print(f" Error: {e}")
            return False

if __name__ == "__main__":
    print("=" * 60)
    print("ENTERPRISE INVENTORY MANAGER (EIM)")
    print("Version: 1.0.0")
    print("Built for Windows 10 32-bit")
    print("=" * 60)
    
    manager = StockManager()
    manager.test_connection()
