from src.utils.database import get_connection
from src.utils.session import get_user
from datetime import datetime

def log_action(action, entity_type, entity_id, details=""):
    """Record an action in the audit log."""
    try:
        user = get_user()
        if not user:
            return # Don't log if no one is logged in

        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO audit_logs (user_id, action, entity_type, entity_id, new_value, reason)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user['username'], action, entity_type, entity_id, details, "System Action"))
        
        conn.commit()
    except Exception as e:
        print(f"❌ Audit log error: {e}")
    finally:
        conn.close()

def view_audit_logs():
    """Display recent audit logs (Admin only)."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT timestamp, user_id, action, entity_type, new_value 
            FROM audit_logs 
            ORDER BY timestamp DESC 
            LIMIT 20
        ''')
        logs = cursor.fetchall()
        
        print(f"\n{'Time':<20} {'User':<10} {'Action':<15} {'Type':<10} {'Details'}")
        print("-" * 80)
        for log in logs:
            print(f"{log['timestamp']:<20} {log['user_id']:<10} {log['action']:<15} {log['entity_type']:<10} {log['new_value']}")
            
    except Exception as e:
        print(f"❌ Error viewing logs: {e}")
    finally:
        conn.close()
