from src.utils.database import get_connection
from datetime import datetime

class StockService:
    
    def add_stock_entry(self, product_sku, quantity, unit_cost, user_id, reason, reference=""):
        """
        Add stock (supplier reception, return, adjustment).
        Recalculates CUMP automatically.
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Get current product data
            cursor.execute("SELECT id, current_stock, cump FROM products WHERE sku = ?", (product_sku,))
            product = cursor.fetchone()
            
            if not product:
                print(f"❌ Product with SKU '{product_sku}' not found.")
                return False
            
            product_id = product['id']
            current_stock = product['current_stock']
            current_cump = product['cump']
            
            # Calculate new CUMP (Weighted Average Cost)
            # Formula: (Current Stock × Current CUMP + New Qty × New Cost) / (Current Stock + New Qty)
            total_value = (current_stock * current_cump) + (quantity * unit_cost)
            new_total_stock = current_stock + quantity
            new_cump = total_value / new_total_stock if new_total_stock > 0 else 0
            
            # Update product stock and CUMP
            cursor.execute('''
                UPDATE products 
                SET current_stock = ?, cump = ? 
                WHERE id = ?
            ''', (new_total_stock, new_cump, product_id))
            
            # Record the movement
            cursor.execute('''
                INSERT INTO stock_movements 
                (product_id, movement_type, quantity, unit_cost, user_id, reason, reference)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (product_id, 'ENTRY', quantity, unit_cost, user_id, reason, reference))
            
            conn.commit()
            print(f"✅ Stock Entry successful!")
            print(f"   Product: {product_sku}")
            print(f"   Quantity: +{quantity}")
            print(f"   New Stock: {new_total_stock}")
            print(f"   New CUMP: {new_cump:.2f}")
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
        finally:
            conn.close()
    
    def add_stock_exit(self, product_sku, quantity, user_id, reason, reference=""):
        """
        Remove stock (sale, loss, transfer).
        Uses current CUMP for valuation.
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Get current product data
            cursor.execute("SELECT id, current_stock, cump FROM products WHERE sku = ?", (product_sku,))
            product = cursor.fetchone()
            
            if not product:
                print(f"❌ Product with SKU '{product_sku}' not found.")
                return False
            
            product_id = product['id']
            current_stock = product['current_stock']
            current_cump = product['cump']
            
            # Check if enough stock
            if current_stock < quantity:
                print(f"❌ Insufficient stock! Available: {current_stock}, Requested: {quantity}")
                return False
            
            # Update product stock
            new_stock = current_stock - quantity
            cursor.execute('''
                UPDATE products 
                SET current_stock = ? 
                WHERE id = ?
            ''', (new_stock, product_id))
            
            # Record the movement
            cursor.execute('''
                INSERT INTO stock_movements 
                (product_id, movement_type, quantity, unit_cost, user_id, reason, reference)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (product_id, 'EXIT', quantity, current_cump, user_id, reason, reference))
            
            conn.commit()
            print(f"✅ Stock Exit successful!")
            print(f"   Product: {product_sku}")
            print(f"   Quantity: -{quantity}")
            print(f"   New Stock: {new_stock}")
            print(f"   Value (CUMP): {current_cump:.2f} per unit")
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
        finally:
            conn.close()
    
    def get_movements_by_product(self, product_sku):
        """Get all movements for a specific product (audit trail)."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT sm.*, p.name, p.sku 
                FROM stock_movements sm
                JOIN products p ON sm.product_id = p.id
                WHERE p.sku = ?
                ORDER BY sm.movement_date DESC
            ''', (product_sku,))
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
        finally:
            conn.close()
    
    def get_all_movements(self):
        """Get all stock movements."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT sm.*, p.name, p.sku 
                FROM stock_movements sm
                JOIN products p ON sm.product_id = p.id
                ORDER BY sm.movement_date DESC
            ''')
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
        finally:
            conn.close()
