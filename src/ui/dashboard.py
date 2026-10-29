from src.services.financial_service import FinancialService
from src.services.product_service import ProductService
from src.utils.helpers import clear_screen, press_enter_to_continue

class DashboardMenu:
    def __init__(self):
        self.financial_service = FinancialService()
        self.product_service = ProductService()

    def show_menu(self):
        while True:
            clear_screen()
            print("\n" + "="*40)
            print(" TABLEAU DE BORD FINANCIER")
            print("="*40)
            print("1. Voir les Marges des Produits")
            print("2. Résumé de la Rentabilité")
            print("3. Alertes de Stock")
            print("4. Analyse ABC (Pareto)")
            print("5. Rapport de Stock Mort")
            print("6. Valeur Totale du Stock")
            print("0. Retour au Menu Principal")
            print("="*40)
            
            choice = input("Sélectionnez une option: ")

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
                print("❌ Option invalide. Réessayez.")
                input("\nAppuyez sur Entrée pour continuer...")

    def view_product_margins(self):
        clear_screen()
        print("\n--- Marges des Produits ---")
        products = self.product_service.get_all_products()
        if not products:
            print("Aucun produit disponible.")
            press_enter_to_continue()
            return
        
        print(f"\n{'SKU':<10} {'Nom':<20} {'Marge':<10} {'Taux Marge %':<12} {'Taux Marque %':<12}")
        print("-" * 70)
        
        for p in products:
            margins = self.financial_service.calculate_product_margins(p['sku'])
            if margins:
                print(f"{margins['sku']:<10} {margins['name']:<20} "
                      f"{margins['margin']:<10.2f} {margins['margin_rate']:<12.2f} "
                      f"{margins['markup_rate']:<12.2f}")
        press_enter_to_continue()

    def view_profitability(self):
        clear_screen()
        print("\n--- Résumé de la Rentabilité ---")
        result = self.financial_service.calculate_profitability()
        
        if result:
            print(f"Chiffre d'Affaires Total:  {result['revenue']:,.2f} DJF")
            print(f"Coût de Revient (COGS):   {result['cogs']:,.2f} DJF")
            print(f"Bénéfice Brut:            {result['gross_profit']:,.2f} DJF")
            print(f"Marge de Bénéfice:        {result['profit_margin']:.2f}%")
        else:
            print("Aucune donnée de vente disponible.")
        press_enter_to_continue()

    def view_stock_alerts(self):
        clear_screen()
        print("\n--- Alertes de Stock ---")
        alerts = self.financial_service.get_stock_alerts()
        
        if not alerts:
            print("✅ Aucune alerte. Tous les produits sont au-dessus des seuils.")
        else:
            print(f"{'SKU':<10} {'Nom':<20} {'Actuel':<10} {'Alerte':<10} {'Sécurité':<10}")
            print("-" * 70)
            
            for alert in alerts:
                print(f"{alert['sku']:<10} {alert['name']:<20} "
                      f"{alert['current_stock']:<10} {alert['alert_threshold']:<10} "
                      f"{alert['safety_stock']:<10}")
            
            print(f"\n⚠️  {len(alerts)} produit(s) nécessitent un réapprovisionnement !")
        press_enter_to_continue()

    def view_abc_analysis(self):
        clear_screen()
        print("\n--- Analyse ABC (Pareto 80/20) ---")
        results = self.financial_service.abc_analysis()
        
        if not results:
            print("Aucune donnée de vente pour l'analyse ABC.")
            press_enter_to_continue()
            return
        
        class_a = sum(1 for r in results if r['class'] == 'A')
        class_b = sum(1 for r in results if r['class'] == 'B')
        class_c = sum(1 for r in results if r['class'] == 'C')
        
        print(f"\nClasse A: {class_a} produits (Meilleures ventes - 80% du CA)")
        print(f"Classe B: {class_b} produits (Ventes moyennes - 15% du CA)")
        print(f"Classe C: {class_c} produits (Ventes lentes - 5% du CA)")
        
        print(f"\n{'Classe':<7} {'SKU':<10} {'Nom':<20} {'CA':<15} {'%':<8}")
        print("-" * 70)
        
        for r in results[:10]:
            print(f"{r['class']:<7} {r['sku']:<10} {r['name']:<20} "
                  f"{r['revenue']:<14,.2f} {r['percentage']:.1f}%")
        
        if len(results) > 10:
            print(f"... et {len(results) - 10} autres produits")
        press_enter_to_continue()

    def view_dead_stock(self):
        clear_screen()
        print("\n--- Rapport de Stock Mort (Aucun mouvement depuis 90 jours) ---")
        dead_stock = self.financial_service.get_dead_stock(days_inactive=90)
        
        if not dead_stock:
            print("✅ Aucun stock mort détecté.")
        else:
            print(f"{'SKU':<10} {'Nom':<20} {'Stock':<10} {'Valeur':<15}")
            print("-" * 60)
            
            total_value = 0
            for item in dead_stock:
                value = item['current_stock'] * item['cump']
                total_value += value
                print(f"{item['sku']:<10} {item['name']:<20} "
                      f"{item['current_stock']:<10} {value:,.2f} DJF")
            
            print(f"\n️  Valeur totale du stock mort: {total_value:,.2f} DJF")
        press_enter_to_continue()

    def view_total_stock_value(self):
        clear_screen()
        print("\n--- Valorisation Totale du Stock ---")
        total_value = self.financial_service.get_total_stock_value()
        print(f"Valeur Totale du Stock (au CUMP): {total_value:,.2f} DJF")
        press_enter_to_continue()
