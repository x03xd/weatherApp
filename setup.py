import click
from data_text import get_credentials
from database_connection import db
import bisect

class SetupHub:

    cities = []
    hour = None
    email = None
    minutes = []

    @classmethod
    def setup(cls):
        cls.email = get_credentials()[0]
        click.echo("Welcome to the setup menu!")

        while True:

            click.echo("\nPlease select an option:")
            click.echo("1. Change cities based on hour")
            click.echo("2. Change minutes")
            click.echo("3. Exit")

            choice = click.prompt("Enter your choice", type=int)

            if choice == 1:
                cls.hours()
            elif choice == 2:
                cls.minutes()
            elif choice == 3:
                click.echo("Exiting the program. Goodbye!")
                break
            else:
                click.echo("Invalid choice. Please try again.")


    @classmethod
    def hours(cls):
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
    def querying_minutes(cls):
        query = """SELECT minutes FROM users WHERE email = %s ORDER BY minutes;"""
        params = (cls.email,)

        result, minutes_array = db.execute_query(query, params, "SELECT")
        cls.minutes = minutes_array[0]

    @classmethod
    def minutes(cls):
        cls.querying_minutes()
        click.echo(f"Minutes: {cls.minutes}")

        while True:
            minutes = click.prompt("Add unique minute timer in which the notification should be displayed. Range <0, 59>.", type=str)

            if not minutes.isdigit() or len(minutes) > 2 or len(minutes) == 0:
                click.echo("Input is not accepted because of characters other than numbers. Try again.")
                continue

            if 0 > int(minutes) > 60:
                click.echo("Input is not accepted because of violate the constraint -> Range <0, 59>. Try again.")
                continue

            if minutes in cls.minutes:
                click.echo("Input already exists in the database.")
                continue

            if len(minutes) == 1:
                minutes = "0" + minutes

            query = """UPDATE users SET minutes = ARRAY_APPEND(minutes, %s) WHERE email = %s;"""

            params = (minutes, cls.email)
            db.execute_query(query, params, "UPDATE")

            index_to_insert = bisect.bisect_left(cls.minutes, minutes)
            cls.minutes.insert(index_to_insert, minutes)

            click.echo(f"Minutes: {cls.minutes}")



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




