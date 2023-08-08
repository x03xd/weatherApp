import click
from data_text import get_credentials
from database_connection import db

class SetupHub:

    cities = []
    hour = None
    email = None

    @classmethod
    def setup(cls):

        cls.email, hashed_password = get_credentials()

        hour = click.prompt("Please enter an hour", type=str)

        query = """SELECT cities FROM timers WHERE user_email = %s AND hour = %s"""
        params = (cls.email, hour)

        result, record = db.execute_query(query, params, "SELECT")

        if result is False:
            query_insert = """INSERT INTO timers(hour, user_email, cities)
                    VALUES(%s, %s, %s);"""

            params_insert = (hour, cls.email, [])
            db.execute_query(query_insert, params_insert, "INSERT")

            cls.cities = []

        cls.cities = record[0]
        cls.hour = hour
        cls.interface()


    @classmethod
    def interface(cls):
        click.echo("You can either provide new city typing its name or remove existing doing the same things"
                   "If you provide not existing city you will receive info about this in the console while good ones will be shown")
        click.echo(f"Hour: {cls.hour}, Cities: {cls.cities}")

        city = click.prompt("Enter a city")
        city = city.lower()

        if city in cls.cities:
            cls.remove_city(city)

        else:
            cities_length = len(cls.cities)

            if cities_length >= 3:
                click.echo("You cannot add new city (limit equals 3)")
                cls.interface()

            else:
                cls.add_city(city)


    @classmethod
    def remove_city(cls, city):

        if city in cls.cities:
            query = """UPDATE timers SET cities = ARRAY_REMOVE(cities, %s) WHERE user_email = %s AND hour = %s;"""
            params = (city, cls.email, cls.hour)

            db.execute_query(query, params, "UPDATE")
            cls.cities.remove(city)

        cls.interface()


    @classmethod
    def add_city(cls, city):

        if city in cls.cities:
            click.echo("Given city is already in your choices")

        else:
            query = """UPDATE timers SET cities = ARRAY_APPEND(cities, %s) WHERE user_email = %s AND hour = %s;"""
            params = (city, cls.email, cls.hour)

            db.execute_query(query, params, "UPDATE")
            cls.cities.append(city)

        cls.interface()




