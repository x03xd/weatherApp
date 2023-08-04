import click

# Dummy user credentials for demonstration purposes
VALID_USERNAME = "user"
VALID_PASSWORD = "password"

@click.command()
@click.option('--username', prompt='Your username', help='Your login username')
@click.password_option(prompt='Your password', confirmation_prompt=False, help='Your login password')
def login(username, password):
    """Simple login command."""
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        click.echo(f"Login successful. Welcome, {username}!")
    else:
        click.echo("Invalid credentials. Login failed.")

if __name__ == '__main__':
    login()