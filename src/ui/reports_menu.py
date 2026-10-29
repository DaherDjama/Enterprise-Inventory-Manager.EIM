from src.services.report_service import ReportService
from src.utils.helpers import clear_screen, press_enter_to_continue

class ReportsMenu:
    def __init__(self):
        self.service = ReportService()

    def show_menu(self):
        while True:
            clear_screen()
            print("\n" + "="*40)
            print(" MENU RAPPORTS & EXPORT")
            print("="*40)
            print("1. Exporter les Produits en CSV")
            print("2. Exporter les Mouvements en CSV")
            print("3. Générer un Rapport d'Inventaire")
            print("4. Générer un Résumé des Mouvements")
            print("0. Retour au Menu Principal")
            print("="*40)
            
            choice = input("Sélectionnez une option: ")

            if choice == '1':
                self.service.export_products_to_csv()
                press_enter_to_continue()
            elif choice == '2':
                self.export_movements_with_date()
            elif choice == '3':
                self.service.generate_inventory_report()
                press_enter_to_continue()
            elif choice == '4':
                self.generate_movement_summary_with_date()
            elif choice == '0':
                break
            else:
                print("❌ Option invalide. Réessayez.")
                input("\nAppuyez sur Entrée pour continuer...")

    def export_movements_with_date(self):
        clear_screen()
        print("\n--- Export des Mouvements ---")
        print("Laissez les dates vides pour exporter tous les mouvements")
        start_date = input("Date de début (YYYY-MM-DD): ").strip()
        end_date = input("Date de fin (YYYY-MM-DD): ").strip()
        
        if not start_date or not end_date:
            start_date = None
            end_date = None
        
        self.service.export_movements_to_csv(start_date, end_date)
        press_enter_to_continue()

    def generate_movement_summary_with_date(self):
        clear_screen()
        print("\n--- Résumé des Mouvements ---")
        print("Laissez les dates vides pour le résumé complet")
        start_date = input("Date de début (YYYY-MM-DD): ").strip()
        end_date = input("Date de fin (YYYY-MM-DD): ").strip()
        
        if not start_date or not end_date:
            start_date = None
            end_date = None
        
        self.service.generate_movement_summary(start_date, end_date)
        press_enter_to_continue()
