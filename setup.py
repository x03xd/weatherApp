import click
from data_text import get_credentials
from database_connection import db


class SetupHub:

    cities = []

    def setup(cls):

        email, hashed_password = get_credentials()
        hour = click.prompt("Please enter an hour", type=str)

        query = """SELECT hour, cities FROM timers WHERE user_email = %s AND hour = %s"""
        params = (email, hour)

        result, record = db.execute_query(query, params, "SELECT")
        hour_, SetupHub.cities = record

        click.echo("You can either provide new city typing its name or remove existing doing the same things")
        click.echo(f"Hour: {hour_}, Cities: {SetupHub.cities}")

        city = click.prompt("Enter a city")

        if city in SetupHub.cities:
            SetupHub.remove_city(city)


    def remove_city(cls, city):
        city = city.lower()

        if city in SetupHub.cities:
            SetupHub.remove(city)
            

    def add(cls, city):
        pass




