import click
from authentication import Authentication
from data_text import is_user_logged
from main2 import setup_or_run
@click.command()


def main():
    click.echo("Welcome to the program!")

    while True:
        if is_user_logged():
            setup_or_run()

        click.echo("\nPlease select an option:")
        click.echo("1. Login")
        click.echo("2. Register")
        click.echo("3. Exit")

        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
            Authentication.login()
        elif choice == 2:
            Authentication.register()
        elif choice == 3:
            click.echo("Exiting the program. Goodbye!")
            break
        else:
            click.echo("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()


