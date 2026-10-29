from src.services.product_service import ProductService
from src.models.product import Product
from src.utils.helpers import clear_screen, press_enter_to_continue, get_valid_float, get_valid_int

def get_upc(product):
    """Récupère le nombre d'unités par carton de façon sécurisée."""
    try:
        return product['units_per_carton']
    except (KeyError, IndexError, TypeError):
        return 1

class ProductMenu:
    def __init__(self):
        self.service = ProductService()

    def show_menu(self):
        while True:
            clear_screen()
            print("\n" + "="*40)
            print(" MENU GESTION DES PRODUITS")
            print("="*40)
            print("1. Ajouter un Nouveau Produit")
            print("2. Lister Tous les Produits")
            print("3. Rechercher un Produit (Nom ou SKU)")
            print("4. Supprimer un Produit")
            print("5. Modifier un Produit")
            print("0. Retour au Menu Principal")
            print("="*40)
            
            choice = input("Sélectionnez une option: ")

            if choice == '1': self.add_product_flow()
            elif choice == '2': self.list_products()
            elif choice == '3': self.search_product()
            elif choice == '4': self.delete_product_flow()
            elif choice == '5': self.edit_product_flow()
            elif choice == '0': break
            else:
                print("❌ Option invalide.")
                input("\nAppuyez sur Entrée pour continuer...")

    def add_product_flow(self):
        clear_screen()
        print("\n--- Ajouter un Nouveau Produit ---")
        sku = input("SKU (Code Unique): ")
        name = input("Nom du Produit: ")
        category = input("Catégorie: ")
        brand = input("Marque: ")
        
        unit = "carton"
        print(f"Unité: {unit} (par défaut)")
        
        units_per_carton = get_valid_int("Nombre d'unités à l'intérieur d'un carton: ")
        
        purchase_price = get_valid_float("Prix d'Achat (HT) par unité: ")
        sale_price_ht = get_valid_float("Prix de Vente (HT) par unité: ")
        tax_rate = get_valid_float("Taux de Taxe % (ex: 20): ")
        alert_threshold = get_valid_float("Seuil d'Alerte (en cartons): ")
        current_stock = get_valid_float("Stock Initial (en cartons): ")
        location = input("Emplacement (Étagère A1): ")
        
        sale_price_ttc = sale_price_ht * (1 + tax_rate / 100)

        product = Product(
            sku=sku, name=name, category=category, brand=brand, unit=unit,
            purchase_price=purchase_price, sale_price_ht=sale_price_ht,
            sale_price_ttc=sale_price_ttc, tax_rate=tax_rate,
            alert_threshold=alert_threshold, units_per_carton=units_per_carton,
            location=location, current_stock=current_stock
        )
        self.service.add_product(product)
        press_enter_to_continue()

    def list_products(self):
        clear_screen()
        print("\n--- Tous les Produits ---")
        products = self.service.get_all_products()
        if not products:
            print("Aucun produit trouvé.")
        else:
            print(f"{'SKU':<8} {'Nom':<15} {'Unités/Cart':<12} {'Stock':<8} {'Prix HT/Unit':<12}")
            print("-" * 60)
            for p in products:
                upc = get_upc(p)
                print(f"{p['sku']:<8} {p['name']:<15} {upc:<12} {p['current_stock']:<8} {p['sale_price_ht']:<12}")
        press_enter_to_continue()

    def search_product(self):
        clear_screen()
        keyword = input("\n🔍 Entrez un mot-clé (Nom ou SKU): ")
        products = self.service.search_products(keyword)
        if not products:
            print("❌ Aucun produit trouvé.")
        else:
            print(f"\n✅ {len(products)} produit(s) trouvé(s):")
            print(f"{'SKU':<8} {'Nom':<15} {'Unités/Cart':<12} {'Stock':<8} {'Prix HT/Unit':<12}")
            print("-" * 60)
            for p in products:
                upc = get_upc(p)
                print(f"{p['sku']:<8} {p['name']:<15} {upc:<12} {p['current_stock']:<8} {p['sale_price_ht']:<12}")
        press_enter_to_continue()

    def delete_product_flow(self):
        clear_screen()
        sku = input("\nEntrez le SKU à supprimer: ")
        self.service.delete_product(sku)
        press_enter_to_continue()

    def edit_product_flow(self):
        clear_screen()
        print("\n--- Modifier un Produit ---")
        sku = input("Entrez le SKU du produit à modifier: ")
        product = self.service.get_product_by_sku(sku)
        if not product:
            print("❌ Produit non trouvé.")
            press_enter_to_continue()
            return
        
        current_upc = get_upc(product)
        
        print(f"\n📦 Valeurs actuelles: {product['name']}")
        print(f"   Unités par carton: {current_upc}")
        print(f"   Prix de Vente HT par unité: {product['sale_price_ht']}")
        print("\n💡 (Appuyez sur Entrée pour garder la valeur actuelle)\n")
        
        name = input(f"Nouveau Nom [{product['name']}]: ").strip() or None
        
        upc_input = input(f"Nouvelles unités par carton [{current_upc}]: ").strip()
        units_per_carton = int(upc_input) if upc_input else None
        
        sale_price_input = input(f"Nouveau Prix de Vente HT par unité [{product['sale_price_ht']}]: ").strip()
        sale_price_ht = float(sale_price_input) if sale_price_input else None
        
        updates = {}
        if name: updates['name'] = name
        if units_per_carton: updates['units_per_carton'] = units_per_carton
        if sale_price_ht is not None: updates['sale_price_ht'] = sale_price_ht
        
        if updates:
            self.service.update_product(sku, **updates)
        else:
            print("⚠️ Aucune modification effectuée.")
        press_enter_to_continue()
