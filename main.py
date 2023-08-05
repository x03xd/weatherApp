import click
from authentication import login, register, is_user_logged

@click.command()
def main():
    click.echo("Welcome to the program!")
    is_user_logged()

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








if __name__ == "__main__":
    main()


