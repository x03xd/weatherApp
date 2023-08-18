from common_query_utility import SelectQueryUtility

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

def get_credentials():
    read = read_credentials()
    return read_credentials() if SelectQueryUtility.is_user_logged(read) else None
