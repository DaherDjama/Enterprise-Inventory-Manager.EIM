# Global variable to hold the currently logged-in user
current_user = None

def set_user(user):
    global current_user
    current_user = user

def get_user():
    return current_user

def is_logged_in():
    return current_user is not None

def logout():
    global current_user
    current_user = None
