import click
from database_connection import db
from password_handler import hash_password, verify_login
import base64

class Program:
    pass

@click.command()
def main():
    """Console menu to redirect to login or register."""
    click.echo("Welcome to the program!")

    while True:
        click.echo("\nPlease select an option:")
        click.echo("1. Login")
        click.echo("2. Register")
        click.echo("3. Exit")

        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
            login()
        elif choice == 2:
            register()
        elif choice == 3:
            click.echo("Exiting the program. Goodbye!")
            break
        else:
            click.echo("Invalid choice. Please try again.")


def login():
    click.echo("You selected Login.")

    while True:
        email = click.prompt("Please enter your email", type=str)

        query = "SELECT * FROM users WHERE email = %s;"
        params = (email,)

        result, record = db.execute_query(query, params)

        if not result:
            click.echo("User with given email does not exist. Try again")
            continue

        password = click.prompt("Please enter your password", type=str)

        result = verify_login(password, record[2], record[-1])

        if not result:
            click.echo("The User does not exist")

        #personalization



def register():
    click.echo("You selected Register.")

    while True:
        email = click.prompt("Please enter your email", type=str)
        query = "SELECT * FROM users WHERE email = %s;"
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

        new_user = "INSERT INTO users(email, password, rank, salt) " \
                   "VALUES (%s, %s, %s, %s)"

        params = (email, hashed_password, rank, salt)

        new_user_creation_result = db.execute_query(new_user, params, "INSERT")

        if new_user_creation_result:
            click.echo("New user has been created")

        #personalization

def personalize_info():
    pass




if __name__ == "__main__":

    main()


