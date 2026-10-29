from src.services.auth_service import authenticate_user, create_default_admin
from src.utils.session import set_user, logout, get_user
from src.utils.helpers import clear_screen

def login_screen():
    """Affiche l'écran de connexion."""
    create_default_admin()
    clear_screen()
    
    print("\n" + "="*40)
    print(" GESTIONNAIRE D'INVENTAIRE D'ENTREPRISE")
    print(" CONNEXION SÉCURISÉE")
    print("="*40)
    
    while True:
        username = input("Nom d'utilisateur: ")
        password = input("Mot de passe: ")
        
        user = authenticate_user(username, password)
        
        if user:
            set_user(user)
            print(f"\n✅ Bon retour, {user['username']} ({user['role']})!")
            return True
        else:
            print("❌ Identifiants invalides. Réessayez.")
            print("   (Indice: utilisez 'admin' / 'admin123')")

def logout_user():
    """Déconnecte l'utilisateur."""
    logout()
    print("✅ Déconnexion réussie.")
