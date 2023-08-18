import click
import sys
from setup import SetupHub
from run import HourlyScheduler

def setup_or_run():
    click.echo("Run your program or make personalized choices")
    setup_instance = SetupHub()
    start = HourlyScheduler()

    while True:
        click.echo("\nPlease select an option:")
        click.echo("1. Run")
        click.echo("2. Setup")
        click.echo("3. Exit")
        click.echo("4. Logout")

        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
            start.run()
        elif choice == 2:
            setup_instance.setup()
        elif choice == 3:
            click.echo("Exiting the program. Goodbye!")
            break
        elif choice == 4:
            logout()
        else:
            click.echo("Invalid choice. Please try again.")

def logout():
    with open('weatherApp_auth_data', 'r+') as file:
        file.truncate()
        sys.exit()