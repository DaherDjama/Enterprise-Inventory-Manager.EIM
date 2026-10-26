class Product:
    def __init__(self, sku, name, category, brand, unit, purchase_price, sale_price_ht, tax_rate, alert_threshold, location, current_stock=0.0, cump=0.0, barcode=None, description=None):
        self.sku = sku
        self.name = name
        self.category = category
        self.brand = brand
        self.unit = unit
        self.purchase_price = purchase_price
        self.sale_price_ht = sale_price_ht
        self.tax_rate = tax_rate
        self.alert_threshold = alert_threshold
        self.location = location
        self.current_stock = current_stock
        self.cump = cump
        self.barcode = barcode
        self.description = description

    def calculate_sale_price_ttc(self):
        """Calculate Price with Tax."""
        return self.sale_price_ht * (1 + (self.tax_rate / 100))
