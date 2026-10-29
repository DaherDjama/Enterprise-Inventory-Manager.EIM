from src.utils.database import get_connection
from src.models.product import Product

class ProductService:
    
    def add_product(self, product):
        """Ajoute un nouveau produit dans la base de données."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO products 
                (sku, barcode, name, description, category, brand, unit,
                 purchase_price, sale_price_ht, sale_price_ttc, tax_rate,
                 alert_threshold, safety_stock, location, current_stock, cump, units_per_carton)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                product.sku, product.barcode, product.name, product.description,
                product.category, product.brand, product.unit,
                product.purchase_price, product.sale_price_ht, product.sale_price_ttc,
                product.tax_rate, product.alert_threshold, product.safety_stock,
                product.location, product.current_stock, product.cump, product.units_per_carton
            ))
            conn.commit()
            print(f"✅ Produit '{product.name}' ajouté avec succès !")
            return True
        except Exception as e:
            print(f"❌ Erreur lors de l'ajout: {e}")
            return False
        finally:
            conn.close()
    
    def get_all_products(self):
        """Récupère tous les produits."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products ORDER BY name")
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return []
        finally:
            conn.close()
    
    def get_product_by_sku(self, sku):
        """Récupère un produit par son SKU."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE sku = ?", (sku,))
            return cursor.fetchone()
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return None
        finally:
            conn.close()
    
    def delete_product(self, sku):
        """Supprime un produit par son SKU."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE sku = ?", (sku,))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"✅ Produit {sku} supprimé avec succès.")
                return True
            else:
                print("️ Produit non trouvé.")
                return False
        except Exception as e:
            print(f" Erreur lors de la suppression: {e}")
            return False
        finally:
            conn.close()
    
    def update_product(self, sku, **kwargs):
        """Met à jour des champs spécifiques d'un produit."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            updates = []
            values = []
            for key, value in kwargs.items():
                if value is not None:
                    updates.append(f"{key} = ?")
                    values.append(value)
            
            if not updates:
                print("⚠️ Aucune modification à effectuer.")
                return False
                
            query = f"UPDATE products SET {', '.join(updates)} WHERE sku = ?"
            values.append(sku)
            cursor.execute(query, values)
            conn.commit()
            
            if cursor.rowcount > 0:
                print(f"✅ Produit {sku} mis à jour avec succès !")
                return True
            else:
                print("⚠️ Produit non trouvé.")
                return False
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour: {e}")
            return False
        finally:
            conn.close()
    
    def search_products(self, keyword):
        """Recherche des produits par SKU ou Nom."""
        try:
            conn = get_connection()
            cursor = conn.cursor()
            search_term = f"%{keyword}%"
            cursor.execute("SELECT * FROM products WHERE sku LIKE ? OR name LIKE ? ORDER BY name", (search_term, search_term))
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Erreur de recherche: {e}")
            return []
        finally:
            conn.close()
