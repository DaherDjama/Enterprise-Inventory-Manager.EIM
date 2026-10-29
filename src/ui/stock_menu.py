from src.services.stock_service import StockService
from src.services.product_service import ProductService
from src.utils.helpers import clear_screen, press_enter_to_continue, get_valid_float, get_valid_int

def get_upc(product):
    """Récupère le nombre d'unités par carton de façon sécurisée."""
    try:
        return product['units_per_carton']
    except (KeyError, IndexError, TypeError):
        return 1

class StockMenu:
    def __init__(self):
        self.stock_service = StockService()
        self.product_service = ProductService()
        self.current_user = "admin"

    def show_menu(self):
        while True:
            clear_screen()
            print("\n" + "="*40)
            print(" MENU MOUVEMENTS DE STOCK")
            print("="*40)
            print("1. Entrée de Stock (Réception)")
            print("2. Sortie de Stock (Expédition)")
            print("3. Voir les Mouvements d'un Produit")
            print("4. Voir Tous les Mouvements")
            print("0. Retour au Menu Principal")
            print("="*40)
            
            choice = input("Sélectionnez une option: ")

            if choice == '1': self.stock_entry_flow()
            elif choice == '2': self.stock_exit_flow()
            elif choice == '3': self.view_product_movements()
            elif choice == '4': self.view_all_movements()
            elif choice == '0': break
            else:
                print("❌ Option invalide.")
                input("\nAppuyez sur Entrée pour continuer...")

    def _select_product(self):
        """Affiche la liste des produits et demande à l'utilisateur de choisir par numéro."""
        products = self.product_service.get_all_products()
        if not products:
            print("Aucun produit disponible.")
            return None
        
        print("\nProduits disponibles:")
        print("-" * 60)
        for i, p in enumerate(products, 1):
            upc = get_upc(p)
            print(f"  {i}. {p['sku']} - {p['name']} (Stock: {p['current_stock']} cartons | {upc} unités/carton)")
        print("-" * 60)
        
        while True:
            choice = input("\nTapez le numéro du produit (ou 0 pour annuler): ").strip()
            
            if choice == '0':
                return None
            
            if choice.isdigit() and 1 <= int(choice) <= len(products):
                return products[int(choice) - 1]
            
            print("❌ Choix invalide. Réessayez.")

    def stock_entry_flow(self):
        clear_screen()
        print("\n--- Entrée de Stock (Réception) ---")
        
        product = self._select_product()
        if not product:
            press_enter_to_continue()
            return
        
        sku = product['sku']
        units_per_carton = get_upc(product)
        
        print(f"\n📦 Produit sélectionné: {product['name']} ({sku})")
        
        # Numéro de carton/lot
        carton_number = input("Numéro de carton/lot (ex: LOT-2026-001): ").strip()
        
        # Saisie en cartons
        cartons_quantity = get_valid_int(f"Nombre de cartons reçus: ")
        total_units = cartons_quantity * units_per_carton
        
        print(f"→ Total: {cartons_quantity} cartons × {units_per_carton} unités = {total_units} unités")
        
        unit_cost = get_valid_float("Coût unitaire (par unité): ")
        reason = input("Raison (ex: Réception Fournisseur, Retour): ")
        reference = input("Référence (ex: Facture #123): ")
        
        self.stock_service.add_stock_entry(
            product_sku=sku, quantity=total_units, unit_cost=unit_cost,
            user_id=self.current_user, reason=reason, reference=reference,
            carton_number=carton_number, units_per_carton=units_per_carton
        )
        press_enter_to_continue()

    def stock_exit_flow(self):
        clear_screen()
        print("\n--- Sortie de Stock (Expédition) ---")
        
        product = self._select_product()
        if not product:
            press_enter_to_continue()
            return
        
        sku = product['sku']
        units_per_carton = get_upc(product)
        
        print(f"\n📦 Produit sélectionné: {product['name']} ({sku})")
        
        # Numéro de carton/lot
        carton_number = input("Numéro de carton/lot expédié (ex: CART-045): ").strip()
        
        cartons_quantity = get_valid_int(f"Nombre de cartons expédiés: ")
        total_units = cartons_quantity * units_per_carton
        
        print(f"→ Total: {cartons_quantity} cartons × {units_per_carton} unités = {total_units} unités")
        
        reason = input("Raison (ex: Vente, Perte, Transfert): ")
        reference = input("Référence (ex: Bon de livraison #456): ")
        
        self.stock_service.add_stock_exit(
            product_sku=sku, quantity=total_units,
            user_id=self.current_user, reason=reason, reference=reference,
            carton_number=carton_number
        )
        press_enter_to_continue()

    def view_product_movements(self):
        clear_screen()
        print("\n--- Historique des Mouvements ---")
        
        product = self._select_product()
        if not product:
            press_enter_to_continue()
            return
        
        movements = self.stock_service.get_movements_by_product(product['sku'])
        
        if not movements:
            print("Aucun mouvement trouvé pour ce produit.")
        else:
            print(f"\n--- Historique pour {product['name']} ({product['sku']}) ---")
            print(f"{'Date':<18} {'Type':<8} {'Qté':<8} {'Lot/Carton':<15} {'Raison'}")
            print("-" * 70)
            for m in movements:
                carton = m.get('carton_number', '') if isinstance(m, dict) else (m['carton_number'] if 'carton_number' in m.keys() else '')
                print(f"{m['movement_date']:<18} {m['movement_type']:<8} {m['quantity']:<8} {carton:<15} {m['reason']}")
        press_enter_to_continue()

    def view_all_movements(self):
        clear_screen()
        print("\n--- Tous les Mouvements de Stock ---")
        movements = self.stock_service.get_all_movements()
        
        if not movements:
            print("Aucun mouvement enregistré.")
        else:
            print(f"{'Date':<18} {'SKU':<10} {'Type':<8} {'Qté':<8} {'Lot/Carton':<15} {'Utilisateur'}")
            print("-" * 80)
            for m in movements:
                carton = m.get('carton_number', '') if isinstance(m, dict) else (m['carton_number'] if 'carton_number' in m.keys() else '')
                print(f"{m['movement_date']:<18} {m['sku']:<10} {m['movement_type']:<8} {m['quantity']:<8} {carton:<15} {m['user_id']}")
        press_enter_to_continue()
