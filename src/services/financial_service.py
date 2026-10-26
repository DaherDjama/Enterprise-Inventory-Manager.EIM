from src.utils.database import get_connection
from datetime import datetime, timedelta

class FinancialService:
    
    def calculate_product_margins(self, product_sku):
        """
        Calculate all margin metrics for a product.
        Returns: dict with margin, rates, and multiplier
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT name, sale_price_ht, cump, purchase_price 
                FROM products WHERE sku = ?
            """, (product_sku,))
            product = cursor.fetchone()
            
            if not product:
                return None
            
            sale_price = product['sale_price_ht']
            cump = product['cump']
            
            # Marge Commerciale (in value)
            margin = sale_price - cump
            
            # Taux de Marge (%)
            margin_rate = (margin / cump * 100) if cump > 0 else 0
            
            # Taux de Marque (%)
            markup_rate = (margin / sale_price * 100) if sale_price > 0 else 0
            
            # Coefficient Multiplicateur
            multiplier = sale_price / cump if cump > 0 else 0
            
            return {
                'name': product['name'],
                'sku': product_sku,
                'sale_price_ht': sale_price,
                'cump': cump,
                'margin': margin,
                'margin_rate': margin_rate,
                'markup_rate': markup_rate,
                'multiplier': multiplier
            }
        except Exception as e:
            print(f"❌ Error calculating margins: {e}")
            return None
        finally:
            conn.close()
    
    def calculate_profitability(self, start_date=None, end_date=None):
        """
        Calculate overall profitability (Revenue, COGS, Gross Profit).
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Get all stock exits (sales) in date range
            if start_date and end_date:
                cursor.execute("""
                    SELECT sm.quantity, sm.unit_cost, p.sale_price_ht
                    FROM stock_movements sm
                    JOIN products p ON sm.product_id = p.id
                    WHERE sm.movement_type = 'EXIT'
                    AND sm.movement_date BETWEEN ? AND ?
                """, (start_date, end_date))
            else:
                cursor.execute("""
                    SELECT sm.quantity, sm.unit_cost, p.sale_price_ht
                    FROM stock_movements sm
                    JOIN products p ON sm.product_id = p.id
                    WHERE sm.movement_type = 'EXIT'
                """)
            
            sales = cursor.fetchall()
            
            total_revenue = 0.0
            total_cogs = 0.0
            
            for sale in sales:
                qty = sale['quantity']
                cump = sale['unit_cost']
                sale_price = sale['sale_price_ht']
                
                total_revenue += qty * sale_price
                total_cogs += qty * cump
            
            gross_profit = total_revenue - total_cogs
            profit_margin = (gross_profit / total_revenue * 100) if total_revenue > 0 else 0
            
            return {
                'revenue': total_revenue,
                'cogs': total_cogs,
                'gross_profit': gross_profit,
                'profit_margin': profit_margin
            }
        except Exception as e:
            print(f"❌ Error calculating profitability: {e}")
            return None
        finally:
            conn.close()
    
    def get_stock_alerts(self):
        """
        Get products below alert threshold or safety stock.
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT sku, name, current_stock, alert_threshold, safety_stock
                FROM products
                WHERE current_stock <= alert_threshold
                OR current_stock <= safety_stock
                ORDER BY current_stock ASC
            """)
            
            return cursor.fetchall()
        except Exception as e:
            print(f" Error getting alerts: {e}")
            return []
        finally:
            conn.close()
    
    def get_dead_stock(self, days_inactive=90):
        """
        Find products with no movement in X days (dead stock).
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cutoff_date = (datetime.now() - timedelta(days=days_inactive)).strftime('%Y-%m-%d')
            
            cursor.execute("""
                SELECT p.sku, p.name, p.current_stock, p.cump
                FROM products p
                WHERE p.current_stock > 0
                AND p.id NOT IN (
                    SELECT DISTINCT product_id 
                    FROM stock_movements 
                    WHERE movement_date >= ?
                )
            """, (cutoff_date,))
            
            return cursor.fetchall()
        except Exception as e:
            print(f"❌ Error getting dead stock: {e}")
            return []
        finally:
            conn.close()
    
    def abc_analysis(self):
        """
        ABC Analysis (Pareto 80/20 rule).
        Class A: 20% products = 80% revenue
        Class B: 30% products = 15% revenue
        Class C: 50% products = 5% revenue
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Get total revenue per product
            cursor.execute("""
                SELECT p.id, p.sku, p.name, 
                       SUM(sm.quantity * p.sale_price_ht) as revenue
                FROM products p
                LEFT JOIN stock_movements sm ON p.id = sm.product_id 
                    AND sm.movement_type = 'EXIT'
                GROUP BY p.id
                ORDER BY revenue DESC
            """)
            
            products = cursor.fetchall()
            total_revenue = sum(p['revenue'] or 0 for p in products)
            
            if total_revenue == 0:
                return []
            
            results = []
            cumulative_revenue = 0.0
            cumulative_percentage = 0.0
            
            for product in products:
                revenue = product['revenue'] or 0
                percentage = (revenue / total_revenue * 100) if total_revenue > 0 else 0
                cumulative_percentage += percentage
                
                # Classify based on cumulative percentage
                if cumulative_percentage <= 80:
                    abc_class = 'A'
                elif cumulative_percentage <= 95:
                    abc_class = 'B'
                else:
                    abc_class = 'C'
                
                results.append({
                    'sku': product['sku'],
                    'name': product['name'],
                    'revenue': revenue,
                    'percentage': percentage,
                    'cumulative_percentage': cumulative_percentage,
                    'class': abc_class
                })
            
            return results
        except Exception as e:
            print(f" Error in ABC analysis: {e}")
            return []
        finally:
            conn.close()
    
    def get_total_stock_value(self):
        """
        Calculate total value of current stock (at CUMP).
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT SUM(current_stock * cump) as total_value
                FROM products
            """)
            
            result = cursor.fetchone()
            return result['total_value'] or 0.0
        except Exception as e:
            print(f"❌ Error calculating stock value: {e}")
            return 0.0
        finally:
            conn.close()
