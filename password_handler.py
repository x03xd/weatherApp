import bcrypt

def hash_password(password):

    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password, salt


def verify_login(entered_password, stored_hashed_password, stored_salt):

    if isinstance(stored_salt, memoryview):
        stored_salt = stored_salt.tobytes()

    entered_password_bytes = entered_password.encode('utf-8')
    hashed_input = bcrypt.hashpw(entered_password_bytes, stored_salt)

    hashed_input = hashed_input.hex()

    return hashed_input == stored_hashed_password