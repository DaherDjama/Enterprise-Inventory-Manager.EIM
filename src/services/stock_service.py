from src.utils.database import get_connection
from src.services.audit_service import log_action
from datetime import datetime

class StockService:
    
    def add_stock_entry(self, product_sku, quantity, unit_cost, user_id, reason, reference, carton_number="", units_per_carton=1):
        """Ajoute une entrée de stock (réception)."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # 1. Récupérer l'ID du produit
            cursor.execute("SELECT id, current_stock, cump FROM products WHERE sku = ?", (product_sku,))
            product = cursor.fetchone()
            
            if not product:
                print("❌ Produit non trouvé.")
                return False
            
            product_id = product['id']
            old_stock = product['current_stock']
            old_cump = product['cump']
            
            # 2. Calculer le nouveau CUMP (Coût Unitaire Moyen Pondéré)
            total_value = old_stock * old_cump + quantity * unit_cost
            new_stock = old_stock + quantity
            new_cump = total_value / new_stock if new_stock > 0 else 0
            
            # 3. Insérer le mouvement
            cursor.execute('''
                INSERT INTO stock_movements 
                (product_id, movement_type, quantity, unit_cost, user_id, reason, reference, carton_number, units_per_carton)
                VALUES (?, 'ENTREE', ?, ?, ?, ?, ?, ?, ?)
            ''', (product_id, quantity, unit_cost, user_id, reason, reference, carton_number, units_per_carton))
            
            # 4. Mettre à jour le produit
            cursor.execute('''
                UPDATE products SET current_stock = ?, cump = ? WHERE id = ?
            ''', (new_stock, new_cump, product_id))
            
            conn.commit()
            print(f"✅ Entrée de {quantity} unités enregistrée pour {product_sku}.")
            print(f"   Nouveau stock: {new_stock} | Nouveau CUMP: {new_cump:.2f}")
            
            # 5. Journal d'audit
            log_action("ENTREE_STOCK", "product", product_id, 
                      f"+{quantity} unités (Lot: {carton_number})")
            return True
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return False
        finally:
            conn.close()
    
    def add_stock_exit(self, product_sku, quantity, user_id, reason, reference, carton_number=""):
        """Ajoute une sortie de stock."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, current_stock, cump FROM products WHERE sku = ?", (product_sku,))
            product = cursor.fetchone()
            
            if not product:
                print("❌ Produit non trouvé.")
                return False
            
            if product['current_stock'] < quantity:
                print(f"❌ Stock insuffisant. Disponible: {product['current_stock']}")
                return False
            
            product_id = product['id']
            new_stock = product['current_stock'] - quantity
            
            cursor.execute('''
                INSERT INTO stock_movements 
                (product_id, movement_type, quantity, unit_cost, user_id, reason, reference, carton_number)
                VALUES (?, 'SORTIE', ?, ?, ?, ?, ?, ?)
            ''', (product_id, quantity, product['cump'], user_id, reason, reference, carton_number))
            
            cursor.execute('''
                UPDATE products SET current_stock = ? WHERE id = ?
            ''', (new_stock, product_id))
            
            conn.commit()
            print(f"✅ Sortie de {quantity} unités enregistrée pour {product_sku}.")
            print(f"   Nouveau stock: {new_stock}")
            
            log_action("SORTIE_STOCK", "product", product_id, 
                      f"-{quantity} unités (Lot: {carton_number})")
            return True
        except Exception as e:
            print(f" Erreur: {e}")
            return False
        finally:
            conn.close()
    
    def get_movements_by_product(self, product_sku):
        """Récupère l'historique des mouvements d'un produit."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT m.*, p.sku 
                FROM stock_movements m 
                JOIN products p ON m.product_id = p.id 
                WHERE p.sku = ? 
                ORDER BY m.movement_date DESC
            ''', (product_sku,))
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return []
        finally:
            conn.close()
    
    def get_all_movements(self):
        """Récupère tous les mouvements de stock."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT m.*, p.sku 
                FROM stock_movements m 
                JOIN products p ON m.product_id = p.id 
                ORDER BY m.movement_date DESC
            ''')
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return []
        finally:
            conn.close()
