import hashlib
from src.utils.database import get_connection

def hash_password(password):
    """Hash a password using SHA-256 with a salt."""
    # In a real app, use bcrypt. Here we use hashlib for simplicity.
    salt = "enterprise_salt_2026" 
    return hashlib.sha256(f"{password}{salt}".encode()).hexdigest()

def verify_password(password, hashed_password):
    return hash_password(password) == hashed_password

def create_default_admin():
    """Create a default admin user if none exists."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if admin exists
        cursor.execute("SELECT id FROM users WHERE username = 'admin'")
        if cursor.fetchone():
            return # Admin already exists

        # Create admin
        hashed = hash_password("admin123")
        cursor.execute('''
            INSERT INTO users (username, password_hash, role, is_active)
            VALUES (?, ?, ?, ?)
        ''', ('admin', hashed, 'Administrator', 1))
        
        conn.commit()
        print("✅ Default admin user created (username: admin, password: admin123)")
    except Exception as e:
        print(f" Error creating admin: {e}")
    finally:
        conn.close()

def authenticate_user(username, password):
    """Check credentials and return user data if valid."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        hashed = hash_password(password)
        
        cursor.execute('''
            SELECT id, username, role FROM users 
            WHERE username = ? AND password_hash = ? AND is_active = 1
        ''', (username, hashed))
        
        user = cursor.fetchone()
        return user
    except Exception as e:
        print(f"❌ Auth error: {e}")
        return None
    finally:
        conn.close()
