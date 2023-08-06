from database_connection import db

def save_user_to_file(email, hashed_password):
    with open('weatherApp_auth_data', 'w') as file:
        file.write(email + '\n')
        file.write(hashed_password + '\n')

def read_credentials():
    credentials = []

    with open('weatherApp_auth_data', 'r') as file:
        for line in file:
            credentials.append(line.strip())

    return credentials

def is_user_logged():
    credentials = read_credentials()

    if credentials:
        email, hashed_password = credentials

        query = """SELECT * FROM users WHERE email = %s AND password = %s"""
        params = (email, hashed_password)

        result, record = db.execute_query(query, params, "SELECT")

        return result

def get_credentials():
    return read_credentials() if is_user_logged() else None
