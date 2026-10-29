class Product:
    def __init__(self, sku, name, category, brand, unit,
                 purchase_price, sale_price_ht, tax_rate,
                 alert_threshold, location, current_stock,
                 units_per_carton=1, sale_price_ttc=None, barcode=None, 
                 description=None, safety_stock=5.0, cump=0.0):
        """
        Initialise un nouveau produit.
        units_per_carton: Nombre d'unités individuelles à l'intérieur d'un carton (ex: 12 bouteilles).
        """
        self.sku = sku
        self.barcode = barcode
        self.name = name
        self.description = description
        self.category = category
        self.brand = brand
        self.unit = unit  # Par défaut 'carton'
        self.purchase_price = purchase_price
        self.sale_price_ht = sale_price_ht
        self.tax_rate = tax_rate
        self.alert_threshold = alert_threshold
        self.safety_stock = safety_stock
        self.location = location
        self.current_stock = current_stock
        self.cump = cump
        self.units_per_carton = units_per_carton
        
        # Calcul automatique du prix TTC si non fourni
        if sale_price_ttc is not None:
            self.sale_price_ttc = sale_price_ttc
        else:
            self.sale_price_ttc = sale_price_ht * (1 + tax_rate / 100)
