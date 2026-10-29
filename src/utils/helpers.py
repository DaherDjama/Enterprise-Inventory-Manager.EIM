import os

def clear_screen():
    """Efface l'écran du terminal (compatible Windows et Linux/Android)."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_valid_float(prompt):
    """Demande un nombre à l'utilisateur jusqu'à ce qu'il soit valide."""
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("❌ Format invalide. Veuillez entrer un nombre (ex: 10.5)")

def get_valid_int(prompt):
    """Demande un entier à l'utilisateur jusqu'à ce qu'il soit valide."""
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print(" Format invalide. Veuillez entrer un nombre entier.")

def press_enter_to_continue():
    """Affiche un message pour que l'utilisateur appuie sur Entrée."""
    input("\nAppuyez sur Entrée pour continuer...")
    clear_screen()
