import click
from authentication_data_functions import hash_password, verify_login, is_valid_email, is_valid_password
from main2 import setup_or_run
from data_text import save_user_to_file
from common_query_utility import SelectQueryUtility, InsertQueryUtility

class Authentication:
    def __init__(self):
        self.select_query_utility = SelectQueryUtility(None)
        self.insert_query_utility = InsertQueryUtility(None)
    def login(self):
        click.echo("You selected Login.")

        while True:
            email = click.prompt("Please enter your email", type=str)
            self.select_query_utility.email = email
            self.insert_query_utility.email = email

            result, record = self.select_query_utility.fetch_user_by_email("*")

            if not result:
                click.echo("User with given email does not exist. Try again")
                continue

            password = click.prompt("Please enter your password", type=str)
            result = verify_login(password, record[2], record[3])

            if result:
                click.echo("You have been logged in")
                save_user_to_file(email, record[2])
                setup_or_run()

            else:
                click.echo("The User does not exist")

    def register(self):
        click.echo("You selected Register.")

        while True:
            email = click.prompt("Please enter your email", type=str)
            self.select_query_utility.email = email
            self.insert_query_utility.email = email

            email_validation = is_valid_email(email)

            if not email_validation:
                click.echo("Email has wrong structure")
                continue

            result, _ = self.select_query_utility.fetch_user_by_email("*")

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

            new_user_creation_result = self.insert_query_utility.create_new_user(hashed_password, salt)

            if new_user_creation_result:
                click.echo("New user has been created")
            else:
                click.echo("Something went wrong")

            save_user_to_file(email, hashed_password)
            setup_or_run()

