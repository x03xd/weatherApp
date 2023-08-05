import click
from database_connection import db
from password_handler import hash_password, verify_login
from main2 import setup_or_run



def save_user_to_file(email, hashed_password):
    with open('weatherApp_auth_data', 'w') as file:
        file.write(email + '\n')
        file.write(hashed_password + '\n')

def is_user_logged():
    credentials = []

    with open('weatherApp_auth_data', 'r') as file:
        for line in file:
            credentials.append(line.strip())

        email, hashed_password = credentials

        query = """SELECT * FROM users WHERE email = %s AND password = %s"""
        params = (email, hashed_password)

        result = db.execute_query(query, params, "SELECT")

        if result:
            setup_or_run()



def login():
    click.echo("You selected Login.")

    while True:
        email = click.prompt("Please enter your email", type=str)

        query = """SELECT * FROM users WHERE email = %s;"""
        params = (email,)

        result, record = db.execute_query(query, params)

        if not result:
            click.echo("User with given email does not exist. Try again")
            continue

        password = click.prompt("Please enter your password", type=str)

        result = verify_login(password, record[2], record[-1])

        if not result:
            click.echo("The User does not exist")

        save_user_to_file(email, record[2])
        setup_or_run()



def register():
    click.echo("You selected Register.")

    while True:
        email = click.prompt("Please enter your email", type=str)
        query = """SELECT * FROM users WHERE email = %s;"""
        params = (email,)

        result, record = db.execute_query(query, params, "SELECT")

        if result:
            click.echo("Email with that email already exists")
            continue

        password = click.prompt("Please enter your password", type=str)
        password2 = click.prompt("Please enter your password again", type=str)

        if password != password2:
            click.echo("Given passwords are not equal")
            continue

        rank = click.prompt("Please enter your rank", type=str)

        hashed_password, salt = hash_password(password)
        hashed_password = hashed_password.hex()

        new_user = """"INSERT INTO users(email, password, rank, salt) " \
                   "VALUES (%s, %s, %s, %s)"""""

        params = (email, hashed_password, rank, salt)
        new_user_creation_result = db.execute_query(new_user, params, "INSERT")

        if new_user_creation_result:
            click.echo("New user has been created")

        save_user_to_file(email)
        setup_or_run()
