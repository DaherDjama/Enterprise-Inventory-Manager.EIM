from src.utils.database import get_connection
from src.models.product import Product

class ProductService:
    
    def add_product(self, product: Product):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            sale_price_ttc = product.calculate_sale_price_ttc()
            
            cursor.execute('''
                INSERT INTO products 
                (sku, barcode, name, description, category, brand, unit, 
                 purchase_price, sale_price_ht, sale_price_ttc, tax_rate, 
                 alert_threshold, location, current_stock, cump)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                product.sku, product.barcode, product.name, product.description,
                product.category, product.brand, product.unit,
                product.purchase_price, product.sale_price_ht, sale_price_ttc,
                product.tax_rate, product.alert_threshold, product.location,
                product.current_stock, product.cump
            ))
            conn.commit()
            print(f"✅ Product '{product.name}' added successfully!")
        except Exception as e:
            print(f"❌ Error adding product: {e}")
        finally:
            conn.close()

    def get_all_products(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products ORDER BY name")
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print(f"❌ Error fetching products: {e}")
            return []
        finally:
            conn.close()

    def get_product_by_sku(self, sku):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE sku = ?", (sku,))
            return cursor.fetchone()
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
        finally:
            conn.close()

    def delete_product(self, sku):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE sku = ?", (sku,))
            conn.commit()
            if cursor.rowcount > 0:
                print(f"✅ Product {sku} deleted.")
            else:
                print("⚠️ Product not found.")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            conn.close()

