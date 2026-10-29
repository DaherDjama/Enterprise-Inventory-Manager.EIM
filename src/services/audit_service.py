from src.utils.database import get_connection
from src.utils.session import get_user
from datetime import datetime

def log_action(action, entity_type, entity_id, details=""):
    """Enregistre une action dans le journal d'audit."""
    try:
        user = get_user()
        if not user:
            return  # Ne pas enregistrer si personne n'est connecté

        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO audit_logs (user_id, action, entity_type, entity_id, new_value, reason)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user['username'], action, entity_type, entity_id, details, "Action Système"))
        
        conn.commit()
    except Exception as e:
        print(f"❌ Erreur journal d'audit: {e}")
    finally:
        conn.close()

def view_audit_logs():
    """Affiche les journaux d'audit récents (Admin seulement)."""
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
        
        if not logs:
            print("Aucun journal d'audit disponible.")
            return
        
        print(f"\n{'Heure':<22} {'Utilisateur':<12} {'Action':<15} {'Type':<12} {'Détails'}")
        print("-" * 85)
        for log in logs:
            print(f"{log['timestamp']:<22} {log['user_id']:<12} {log['action']:<15} {log['entity_type']:<12} {log['new_value']}")
            
    except Exception as e:
        print(f" Erreur lors de l'affichage des journaux: {e}")
    finally:
        conn.close()
