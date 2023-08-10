import click
from database_connection import db
from authentication_data_functions import hash_password, verify_login, is_valid_email, is_valid_password
from main2 import setup_or_run
from data_text import save_user_to_file


class Authentication:
    @staticmethod
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

            if result:
                click.echo("You have been logged in")
                save_user_to_file(email, record[2])
                setup_or_run()

            else:
                click.echo("The User does not exist")


    @staticmethod
    def register():
        click.echo("You selected Register.")

        while True:
            email = click.prompt("Please enter your email", type=str)
            query = """SELECT * FROM users WHERE email = %s;"""

            email_validation = is_valid_email(email)

            if not email_validation:
                click.echo("Email has wrong structure")
                continue

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

            password_validation = is_valid_password(password)

            if not password_validation:
                click.echo("Password must contain at least 8 characters,"
                            " one uppercase, one lowercase, one digit, and one special character")
                continue

            hashed_password, salt = hash_password(password)
            hashed_password = hashed_password.hex()

            new_user = """INSERT INTO users(email, password, salt) VALUES (%s, %s, %s)"""

            params = (email, hashed_password, salt)
            new_user_creation_result = db.execute_query(new_user, params, "INSERT")

            if new_user_creation_result:
                click.echo("New user has been created")
            else:
                click.echo("Something went wrong")

            save_user_to_file(email, hashed_password)
            setup_or_run()

