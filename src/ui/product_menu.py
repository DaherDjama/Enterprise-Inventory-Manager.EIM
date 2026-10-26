from src.services.product_service import ProductService
from src.models.product import Product

class ProductMenu:
    def __init__(self):
        self.service = ProductService()

    def show_menu(self):
        while True:
            print("\n" + "="*40)
            print(" PRODUCT MANAGEMENT MENU")
            print("="*40)
            print("1. Add New Product")
            print("2. List All Products")
            print("3. Search Product by SKU")
            print("4. Delete Product")
            print("0. Exit to Main Menu")
            print("="*40)
            
            choice = input("Select an option: ")

            if choice == '1':
                self.add_product_flow()
            elif choice == '2':
                self.list_products()
            elif choice == '3':
                self.search_product()
            elif choice == '4':
                self.delete_product_flow()
            elif choice == '0':
                break
            else:
                print("Invalid option. Try again.")

    def add_product_flow(self):
        print("\n--- Add New Product ---")
        sku = input("SKU (Unique Code): ")
        name = input("Product Name: ")
        category = input("Category: ")
        brand = input("Brand: ")
        unit = input("Unit (piece, kg, etc.): ")
        
        try:
            purchase_price = float(input("Purchase Price (HT): "))
            sale_price_ht = float(input("Sale Price (HT): "))
            tax_rate = float(input("Tax Rate % (e.g. 20): "))
            alert_threshold = float(input("Alert Threshold: "))
            current_stock = float(input("Initial Stock: "))
            location = input("Location (Shelf A1): ")
        except ValueError:
            print("❌ Invalid number format.")
            return

        product = Product(
            sku=sku, name=name, category=category, brand=brand, unit=unit,
            purchase_price=purchase_price, sale_price_ht=sale_price_ht,
            tax_rate=tax_rate, alert_threshold=alert_threshold,
            location=location, current_stock=current_stock
        )
        self.service.add_product(product)

    def list_products(self):
        print("\n--- All Products ---")
        products = self.service.get_all_products()
        if not products:
            print("No products found.")
            return
        
        print(f"{'SKU':<10} {'Name':<20} {'Stock':<8} {'Price HT':<10}")
        print("-" * 50)
        for p in products:
            print(f"{p['sku']:<10} {p['name']:<20} {p['current_stock']:<8} {p['sale_price_ht']:<10}")

    def search_product(self):
        sku = input("\nEnter SKU to search: ")
        product = self.service.get_product_by_sku(sku)
        if product:
            print(f"\nFound: {product['name']}")
            print(f"Stock: {product['current_stock']}")
            print(f"Price HT: {product['sale_price_ht']}")
        else:
            print("Product not found.")

    def delete_product_flow(self):
        sku = input("\nEnter SKU to delete: ")
        self.service.delete_product(sku)
