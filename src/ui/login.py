from src.services.auth_service import authenticate_user, create_default_admin
from src.utils.session import set_user, logout, get_user

def login_screen():
    """Display login prompt."""
    # Ensure tables exist and admin is created
    create_default_admin()
    
    print("\n" + "="*40)
    print(" ENTERPRISE INVENTORY MANAGER")
    print(" SECURE LOGIN")
    print("="*40)
    
    while True:
        username = input("Username: ")
        password = input("Password: ")
        
        user = authenticate_user(username, password)
        
        if user:
            set_user(user)
            print(f"\n✅ Welcome back, {user['username']} ({user['role']})!")
            return True
        else:
            print("❌ Invalid credentials. Try again.")
            print("   (Hint: use 'admin' / 'admin123')")

def logout_user():
    logout()
    print(" Logged out successfully.")
