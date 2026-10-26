from src.services.report_service import ReportService

class ReportsMenu:
    def __init__(self):
        self.service = ReportService()

    def show_menu(self):
        while True:
            print("\n" + "="*40)
            print(" REPORTS & EXPORT MENU")
            print("="*40)
            print("1. Export Products to CSV")
            print("2. Export Movements to CSV")
            print("3. Generate Inventory Report")
            print("4. Generate Movement Summary")
            print("0. Exit to Main Menu")
            print("="*40)
            
            choice = input("Select an option: ")

            if choice == '1':
                self.service.export_products_to_csv()
            elif choice == '2':
                self.export_movements_with_date()
            elif choice == '3':
                self.service.generate_inventory_report()
            elif choice == '4':
                self.generate_movement_summary_with_date()
            elif choice == '0':
                break
            else:
                print("Invalid option. Try again.")

    def export_movements_with_date(self):
        print("\n--- Export Movements ---")
        print("Leave dates blank to export all movements")
        start_date = input("Start Date (YYYY-MM-DD): ").strip()
        end_date = input("End Date (YYYY-MM-DD): ").strip()
        
        if not start_date or not end_date:
            start_date = None
            end_date = None
        
        self.service.export_movements_to_csv(start_date, end_date)

    def generate_movement_summary_with_date(self):
        print("\n--- Movement Summary ---")
        print("Leave dates blank for all-time summary")
        start_date = input("Start Date (YYYY-MM-DD): ").strip()
        end_date = input("End Date (YYYY-MM-DD): ").strip()
        
        if not start_date or not end_date:
            start_date = None
            end_date = None
        
        self.service.generate_movement_summary(start_date, end_date)
