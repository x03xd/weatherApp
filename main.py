import click
from authentication import Authentication
from main2 import setup_or_run
from common_query_utility import SelectQueryUtility
from data_text import read_credentials

@click.command()
def main():
    click.echo("Welcome to the program!")
    authentication = Authentication()

    while True:
        credentials = read_credentials()
        if SelectQueryUtility.is_user_logged(credentials):
            setup_or_run()

        click.echo("\nPlease select an option:")
        click.echo("1. Login")
        click.echo("2. Register")
        click.echo("3. Exit")

        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
            authentication.login()
        elif choice == 2:
            authentication.register()
        elif choice == 3:
            click.echo("Exiting the program. Goodbye!")
            break
        else:
            click.echo("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()


