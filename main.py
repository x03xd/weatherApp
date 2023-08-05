import click
from database_connection import db




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
    """Function to handle login logic."""
    click.echo("You selected Login.")

    while True:
        email = click.prompt("Please enter your email", type=str)
        password = click.prompt("Please enter your password", type=str)

        query = "SELECT * FROM users WHERE email = %s AND password = %s;"
        params = (email, password)

        result = db.execute_query(query, params)

        if not result:
            click.echo("User does not exist. Try again")
            continue

        #personalization



def register():
    click.echo("You selected Register.")

    while True:
        email = click.prompt("Please enter your email", type=str)
        query = "SELECT * FROM users WHERE email = %s;"
        params = (email,)

        exists = db.execute_query(query, params)

        if exists:
            click.echo("Email with that email already exists")
            continue

        password = click.prompt("Please enter your password", type=str)
        password2 = click.prompt("Please enter your password again", type=str)

        if password != password2:
            click.echo("Given passwords are not equal")
            continue

        rank = click.prompt("Please enter your rank", type=str)

        new_user = "INSERT INTO users(email, password, rank) " \
                   "VALUES (%s, %s, %s)"

        params = (email, password, rank)

        new_user_creation_result = db.execute_query(new_user, params, "INSERT")

        if new_user_creation_result:
            click.echo("New user has been created")

        #personalization

def personalize_info():
    pass




if __name__ == "__main__":

    main()


