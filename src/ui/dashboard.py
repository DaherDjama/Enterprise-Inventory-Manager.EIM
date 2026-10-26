from src.services.financial_service import FinancialService
from src.services.product_service import ProductService

class DashboardMenu:
    def __init__(self):
        self.financial_service = FinancialService()
        self.product_service = ProductService()

    def show_menu(self):
        while True:
            print("\n" + "="*40)
            print(" FINANCIAL DASHBOARD")
            print("="*40)
            print("1. View Product Margins")
            print("2. View Profitability Summary")
            print("3. Stock Alerts")
            print("4. ABC Analysis (Pareto)")
            print("5. Dead Stock Report")
            print("6. Total Stock Value")
            print("0. Exit to Main Menu")
            print("="*40)
            
            choice = input("Select an option: ")

            if choice == '1':
                self.view_product_margins()
            elif choice == '2':
                self.view_profitability()
            elif choice == '3':
                self.view_stock_alerts()
            elif choice == '4':
                self.view_abc_analysis()
            elif choice == '5':
                self.view_dead_stock()
            elif choice == '6':
                self.view_total_stock_value()
            elif choice == '0':
                break
            else:
                print("Invalid option. Try again.")

    def view_product_margins(self):
        print("\n--- Product Margins ---")
        products = self.product_service.get_all_products()
        if not products:
            print("No products available.")
            return
        
        print(f"\n{'SKU':<10} {'Name':<20} {'Margin':<10} {'Margin %':<10} {'Mark %':<10}")
        print("-" * 70)
        
        for p in products:
            margins = self.financial_service.calculate_product_margins(p['sku'])
            if margins:
                print(f"{margins['sku']:<10} {margins['name']:<20} "
                      f"{margins['margin']:<10.2f} {margins['margin_rate']:<10.2f} "
                      f"{margins['markup_rate']:<10.2f}")

    def view_profitability(self):
        print("\n--- Profitability Summary ---")
        result = self.financial_service.calculate_profitability()
        
        if result:
            print(f"Total Revenue:      ${result['revenue']:,.2f}")
            print(f"Total COGS:         ${result['cogs']:,.2f}")
            print(f"Gross Profit:       ${result['gross_profit']:,.2f}")
            print(f"Profit Margin:      {result['profit_margin']:.2f}%")
        else:
            print("No sales data available.")

    def view_stock_alerts(self):
        print("\n--- Stock Alerts ---")
        alerts = self.financial_service.get_stock_alerts()
        
        if not alerts:
            print("✅ No stock alerts. All products are above thresholds.")
            return
        
        print(f"{'SKU':<10} {'Name':<20} {'Current':<10} {'Alert':<10} {'Safety':<10}")
        print("-" * 70)
        
        for alert in alerts:
            print(f"{alert['sku']:<10} {alert['name']:<20} "
                  f"{alert['current_stock']:<10} {alert['alert_threshold']:<10} "
                  f"{alert['safety_stock']:<10}")
        
        print(f"\n⚠️  {len(alerts)} product(s) need reordering!")

    def view_abc_analysis(self):
        print("\n--- ABC Analysis (Pareto 80/20) ---")
        results = self.financial_service.abc_analysis()
        
        if not results:
            print("No sales data for ABC analysis.")
            return
        
        # Count classes
        class_a = sum(1 for r in results if r['class'] == 'A')
        class_b = sum(1 for r in results if r['class'] == 'B')
        class_c = sum(1 for r in results if r['class'] == 'C')
        
        print(f"\nClass A: {class_a} products (Best sellers - 80% revenue)")
        print(f"Class B: {class_b} products (Medium sellers - 15% revenue)")
        print(f"Class C: {class_c} products (Slow movers - 5% revenue)")
        
        print(f"\n{'Class':<6} {'SKU':<10} {'Name':<20} {'Revenue':<15} {'%':<8}")
        print("-" * 70)
        
        for r in results[:10]:  # Show top 10
            print(f"{r['class']:<6} {r['sku']:<10} {r['name']:<20} "
                  f"${r['revenue']:<14,.2f} {r['percentage']:.1f}%")
        
        if len(results) > 10:
            print(f"... and {len(results) - 10} more products")

    def view_dead_stock(self):
        print("\n--- Dead Stock Report (No movement in 90 days) ---")
        dead_stock = self.financial_service.get_dead_stock(days_inactive=90)
        
        if not dead_stock:
            print("✅ No dead stock detected.")
            return
        
        print(f"{'SKU':<10} {'Name':<20} {'Stock':<10} {'Value':<15}")
        print("-" * 60)
        
        total_value = 0
        for item in dead_stock:
            value = item['current_stock'] * item['cump']
            total_value += value
            print(f"{item['sku']:<10} {item['name']:<20} "
                  f"{item['current_stock']:<10} ${value:,.2f}")
        
        print(f"\n⚠️  Total dead stock value: ${total_value:,.2f}")

    def view_total_stock_value(self):
        print("\n--- Total Stock Valuation ---")
        total_value = self.financial_service.get_total_stock_value()
        print(f"Total Stock Value (at CUMP): ${total_value:,.2f}")
