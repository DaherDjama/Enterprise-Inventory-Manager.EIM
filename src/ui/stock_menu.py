from src.services.stock_service import StockService
from src.services.product_service import ProductService

class StockMenu:
    def __init__(self):
        self.stock_service = StockService()
        self.product_service = ProductService()
        self.current_user = "admin"  # Default user (will be dynamic later)

    def show_menu(self):
        while True:
            print("\n" + "="*40)
            print(" STOCK MOVEMENTS MENU")
            print("="*40)
            print("1. Stock Entry (Add Stock)")
            print("2. Stock Exit (Remove Stock)")
            print("3. View Product Movements")
            print("4. View All Movements")
            print("0. Exit to Main Menu")
            print("="*40)
            
            choice = input("Select an option: ")

            if choice == '1':
                self.stock_entry_flow()
            elif choice == '2':
                self.stock_exit_flow()
            elif choice == '3':
                self.view_product_movements()
            elif choice == '4':
                self.view_all_movements()
            elif choice == '0':
                break
            else:
                print("Invalid option. Try again.")

    def stock_entry_flow(self):
        print("\n--- Stock Entry ---")
        print("First, let's see available products:")
        products = self.product_service.get_all_products()
        if not products:
            print("No products available. Add products first.")
            return
        
        for p in products:
            print(f"  {p['sku']} - {p['name']} (Stock: {p['current_stock']})")
        
        sku = input("\nEnter Product SKU: ")
        
        # Verify product exists
        product = self.product_service.get_product_by_sku(sku)
        if not product:
            print("❌ Product not found.")
            return
        
        try:
            quantity = float(input("Quantity to add: "))
            unit_cost = float(input("Unit Cost (Purchase Price): "))
        except ValueError:
            print(" Invalid number format.")
            return
        
        reason = input("Reason (e.g., Supplier Reception, Return): ")
        reference = input("Reference (e.g., Invoice #123): ")
        
        self.stock_service.add_stock_entry(
            product_sku=sku,
            quantity=quantity,
            unit_cost=unit_cost,
            user_id=self.current_user,
            reason=reason,
            reference=reference
        )

    def stock_exit_flow(self):
        print("\n--- Stock Exit ---")
        print("Available products:")
        products = self.product_service.get_all_products()
        if not products:
            print("No products available.")
            return
        
        for p in products:
            print(f"  {p['sku']} - {p['name']} (Stock: {p['current_stock']})")
        
        sku = input("\nEnter Product SKU: ")
        
        product = self.product_service.get_product_by_sku(sku)
        if not product:
            print("❌ Product not found.")
            return
        
        try:
            quantity = float(input("Quantity to remove: "))
        except ValueError:
            print("❌ Invalid number format.")
            return
        
        reason = input("Reason (e.g., Sale, Loss, Transfer): ")
        reference = input("Reference (e.g., Sale #456): ")
        
        self.stock_service.add_stock_exit(
            product_sku=sku,
            quantity=quantity,
            user_id=self.current_user,
            reason=reason,
            reference=reference
        )

    def view_product_movements(self):
        sku = input("\nEnter Product SKU to view history: ")
        movements = self.stock_service.get_movements_by_product(sku)
        
        if not movements:
            print("No movements found for this product.")
            return
        
        print(f"\n--- Movement History for {sku} ---")
        print(f"{'Date':<20} {'Type':<8} {'Qty':<8} {'Cost':<10} {'Reason'}")
        print("-" * 70)
        for m in movements:
            print(f"{m['movement_date']:<20} {m['movement_type']:<8} {m['quantity']:<8} {m['unit_cost']:<10} {m['reason']}")

    def view_all_movements(self):
        print("\n--- All Stock Movements ---")
        movements = self.stock_service.get_all_movements()
        
        if not movements:
            print("No movements recorded yet.")
            return
        
        print(f"{'Date':<20} {'SKU':<10} {'Type':<8} {'Qty':<8} {'User':<10} {'Reason'}")
        print("-" * 80)
        for m in movements:
            print(f"{m['movement_date']:<20} {m['sku']:<10} {m['movement_type']:<8} {m['quantity']:<8} {m['user_id']:<10} {m['reason']}")
