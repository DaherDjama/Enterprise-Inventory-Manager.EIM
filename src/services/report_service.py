import csv
import os
from datetime import datetime
from src.utils.database import get_connection

class ReportService:
    
    def export_products_to_csv(self, filename="reports/products_export.csv"):
        """Export all products to CSV file."""
        try:
            os.makedirs("reports", exist_ok=True)
            conn = get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM products ORDER BY name")
            products = cursor.fetchall()
            
            if not products:
                print(" No products to export.")
                return False
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Header
                writer.writerow([
                    'SKU', 'Name', 'Category', 'Brand', 'Unit',
                    'Purchase Price', 'Sale Price HT', 'Sale Price TTC',
                    'Tax Rate', 'Current Stock', 'CUMP', 'Location',
                    'Alert Threshold', 'Safety Stock'
                ])
                
                # Data
                for p in products:
                    writer.writerow([
                        p['sku'], p['name'], p['category'], p['brand'], p['unit'],
                        p['purchase_price'], p['sale_price_ht'], p['sale_price_ttc'],
                        p['tax_rate'], p['current_stock'], p['cump'], p['location'],
                        p['alert_threshold'], p['safety_stock']
                    ])
            
            print(f"✅ Products exported to {filename}")
            print(f"   Total products: {len(products)}")
            return True
            
        except Exception as e:
            print(f"❌ Export error: {e}")
            return False
        finally:
            conn.close()
    
    def export_movements_to_csv(self, start_date=None, end_date=None, 
                                 filename="reports/movements_export.csv"):
        """Export stock movements to CSV with optional date filter."""
        try:
            os.makedirs("reports", exist_ok=True)
            conn = get_connection()
            cursor = conn.cursor()
            
            if start_date and end_date:
                cursor.execute('''
                    SELECT sm.*, p.sku, p.name 
                    FROM stock_movements sm
                    JOIN products p ON sm.product_id = p.id
                    WHERE sm.movement_date BETWEEN ? AND ?
                    ORDER BY sm.movement_date DESC
                ''', (start_date, end_date))
            else:
                cursor.execute('''
                    SELECT sm.*, p.sku, p.name 
                    FROM stock_movements sm
                    JOIN products p ON sm.product_id = p.id
                    ORDER BY sm.movement_date DESC
                ''')
            
            movements = cursor.fetchall()
            
            if not movements:
                print("❌ No movements to export.")
                return False
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Date', 'SKU', 'Product', 'Type', 'Quantity',
                    'Unit Cost', 'User', 'Reason', 'Reference'
                ])
                
                for m in movements:
                    writer.writerow([
                        m['movement_date'], m['sku'], m['name'],
                        m['movement_type'], m['quantity'], m['unit_cost'],
                        m['user_id'], m['reason'], m['reference']
                    ])
            
            print(f"✅ Movements exported to {filename}")
            print(f"   Total movements: {len(movements)}")
            if start_date and end_date:
                print(f"   Date range: {start_date} to {end_date}")
            return True
            
        except Exception as e:
            print(f"❌ Export error: {e}")
            return False
        finally:
            conn.close()
    
    def generate_inventory_report(self, filename="reports/inventory_report.txt"):
        """Generate a comprehensive text-based inventory report."""
        try:
            os.makedirs("reports", exist_ok=True)
            conn = get_connection()
            cursor = conn.cursor()
            
            # Get summary statistics
            cursor.execute("SELECT COUNT(*) as count FROM products")
            total_products = cursor.fetchone()['count']
            
            cursor.execute("SELECT SUM(current_stock * cump) as total_value FROM products")
            total_value = cursor.fetchone()['total_value'] or 0
            
            cursor.execute("SELECT SUM(current_stock) as total_units FROM products")
            total_units = cursor.fetchone()['total_units'] or 0
            
            cursor.execute("""
                SELECT COUNT(*) as count FROM products 
                WHERE current_stock <= alert_threshold
            """)
            low_stock_count = cursor.fetchone()['count']
            
            # Generate report
            report_lines = []
            report_lines.append("=" * 60)
            report_lines.append("ENTERPRISE INVENTORY MANAGER - INVENTORY REPORT")
            report_lines.append("=" * 60)
            report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report_lines.append("")
            
            report_lines.append("SUMMARY")
            report_lines.append("-" * 60)
            report_lines.append(f"Total Products:        {total_products}")
            report_lines.append(f"Total Units in Stock:  {total_units:.0f}")
            report_lines.append(f"Total Stock Value:     ${total_value:,.2f}")
            report_lines.append(f"Low Stock Alerts:      {low_stock_count}")
            report_lines.append("")
            
            report_lines.append("PRODUCT DETAILS")
            report_lines.append("-" * 60)
            
            cursor.execute("""
                SELECT sku, name, category, current_stock, cump, 
                       (current_stock * cump) as value
                FROM products
                ORDER BY name
            """)
            
            products = cursor.fetchall()
            report_lines.append(f"{'SKU':<10} {'Name':<20} {'Stock':<8} {'CUMP':<10} {'Value':<12}")
            report_lines.append("-" * 60)
            
            for p in products:
                report_lines.append(
                    f"{p['sku']:<10} {p['name']:<20} {p['current_stock']:<8} "
                    f"${p['cump']:<9.2f} ${p['value']:<11.2f}"
                )
            
            report_lines.append("")
            report_lines.append("=" * 60)
            report_lines.append("END OF REPORT")
            report_lines.append("=" * 60)
            
            # Write to file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(report_lines))
            
            print(f"✅ Inventory report generated: {filename}")
            print(f"\n{'='*60}")
            for line in report_lines[:15]:  # Show preview
                print(line)
            print("...")
            print(f"{'='*60}")
            
            return True
            
        except Exception as e:
            print(f"❌ Report generation error: {e}")
            return False
        finally:
            conn.close()
    
    def generate_movement_summary(self, start_date=None, end_date=None,
                                   filename="reports/movement_summary.txt"):
        """Generate a summary of stock movements."""
        try:
            os.makedirs("reports", exist_ok=True)
            conn = get_connection()
            cursor = conn.cursor()
            
            # Get movement statistics
            if start_date and end_date:
                cursor.execute('''
                    SELECT 
                        COUNT(*) as total_movements,
                        SUM(CASE WHEN movement_type = 'ENTRY' THEN quantity ELSE 0 END) as total_entries,
                        SUM(CASE WHEN movement_type = 'EXIT' THEN quantity ELSE 0 END) as total_exits
                    FROM stock_movements
                    WHERE movement_date BETWEEN ? AND ?
                ''', (start_date, end_date))
            else:
                cursor.execute('''
                    SELECT 
                        COUNT(*) as total_movements,
                        SUM(CASE WHEN movement_type = 'ENTRY' THEN quantity ELSE 0 END) as total_entries,
                        SUM(CASE WHEN movement_type = 'EXIT' THEN quantity ELSE 0 END) as total_exits
                    FROM stock_movements
                ''')
            
            stats = cursor.fetchone()
            
            report_lines = []
            report_lines.append("=" * 60)
            report_lines.append("STOCK MOVEMENTS SUMMARY")
            report_lines.append("=" * 60)
            report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            if start_date and end_date:
                report_lines.append(f"Period: {start_date} to {end_date}")
            report_lines.append("")
            
            report_lines.append("MOVEMENT STATISTICS")
            report_lines.append("-" * 60)
            report_lines.append(f"Total Movements:    {stats['total_movements']}")
            report_lines.append(f"Total Entries:      +{stats['total_entries'] or 0:.0f} units")
            report_lines.append(f"Total Exits:        -{stats['total_exits'] or 0:.0f} units")
            report_lines.append("")
            
            # Top 5 most moved products
            cursor.execute('''
                SELECT p.sku, p.name, 
                       SUM(CASE WHEN sm.movement_type = 'ENTRY' THEN sm.quantity ELSE 0 END) as entries,
                       SUM(CASE WHEN sm.movement_type = 'EXIT' THEN sm.quantity ELSE 0 END) as exits
                FROM products p
                LEFT JOIN stock_movements sm ON p.id = sm.product_id
                GROUP BY p.id
                ORDER BY (entries + exits) DESC
                LIMIT 5
            ''')
            
            top_products = cursor.fetchall()
            
            if top_products:
                report_lines.append("TOP 5 MOST ACTIVE PRODUCTS")
                report_lines.append("-" * 60)
                report_lines.append(f"{'SKU':<10} {'Name':<20} {'Entries':<10} {'Exits':<10}")
                report_lines.append("-" * 60)
                
                for prod in top_products:
                    report_lines.append(
                        f"{prod['sku']:<10} {prod['name']:<20} "
                        f"+{prod['entries'] or 0:<9.0f} -{prod['exits'] or 0:<9.0f}"
                    )
            
            report_lines.append("")
            report_lines.append("=" * 60)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(report_lines))
            
            print(f"✅ Movement summary generated: {filename}")
            print(f"\n{'='*60}")
            for line in report_lines:
                print(line)
            print(f"{'='*60}")
            
            return True
            
        except Exception as e:
            print(f"❌ Report error: {e}")
            return False
        finally:
            conn.close()
