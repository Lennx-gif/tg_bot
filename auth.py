# auth.py
def is_authenticated(username, phone, allowed_users):
    for user in allowed_users:
        if user['username'] == username and user['phone'] == phone:
            return True
    return False
