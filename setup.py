import click
from data_text import get_credentials
from database_connection import db
import bisect

class SetupHub:

    cities, minutes = [], []
    hour, email = None, None

    @classmethod
    def setup(cls):
        cls.email = get_credentials()[0]
        click.echo("Welcome to the setup menu!")

        while True:

            click.echo("\nPlease select an option:")
            click.echo("1. Change cities list for specific hour")
            click.echo("2. Change minutes for display hours")
            click.echo("3. Restart list of cities for every hour")
            click.echo("4. Restart minutes timers")
            click.echo("5. Exit")

            choice = click.prompt("Enter your choice", type=int)

            if choice == 1:
                cls.hours()
            elif choice == 2:
                cls.minutes()
            elif choice == 3:
                cls.restart_cities()
            elif choice == 4:
                cls.restart_minutes_timers()
            elif choice == 5:
                click.echo("Exiting the program. Goodbye!")
                break
            else:
                click.echo("Invalid choice. Please try again.")

    @classmethod
    def restart_cities(cls):
        query = """UPDATE timers SET cities = '{}' WHERE user_email = %s;"""
        params = (cls.email,)
        db.execute_query(query, params, "UPDATE")
        click.echo("Cities have been removed.")

    @classmethod
    def restart_minutes_timers(cls):
        query = """UPDATE users SET minutes = '{}' WHERE email = %s;"""
        params = (cls.email,)
        db.execute_query(query, params, "UPDATE")
        click.echo("Minutes timers have been removed.")

    @classmethod
    def hours(cls):
        while True:
            hour = click.prompt("Please enter an hour", type=str)

            if "0" <= hour <= "23":
                click.echo("The input must have range <0, 23>")
                continue

            query = """SELECT cities FROM timers WHERE user_email = %s AND hour = %s"""
            params = (cls.email, hour)

            result, record = db.execute_query(query, params, "SELECT")

            if record is None:
                query_insert = """INSERT INTO timers(hour, user_email, cities) VALUES(%s, %s, %s);"""

                params_insert = (hour, cls.email, [])
                db.execute_query(query_insert, params_insert, "INSERT")

                cls.cities = []

            cls.cities = record[0] if record is not None else []
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
            minutes = click.prompt("Add minute timer in which the notification should be displayed."
                                   " Range <0, 59>. If it already exists, it will be removed", type=str)

            if not minutes.isdigit() or len(minutes) > 2 or len(minutes) == 0:
                click.echo("The input is not accepted because of characters other than numbers. Try again.")
                continue

            if 0 > int(minutes) > 60:
                click.echo("The input is not accepted because of violate the constraint -> Range <0, 59>. Try again.")
                continue

            if len(minutes) == 1:
                minutes = "0" + minutes

            remove_or_append = "REMOVE" if minutes in cls.minutes else "APPEND"

            query = f"""UPDATE users SET minutes = ARRAY_{remove_or_append}(minutes, %s) WHERE email = %s;"""

            params = (minutes, cls.email)
            db.execute_query(query, params, "UPDATE")

            if remove_or_append == "APPEND":
                index_to_insert = bisect.bisect_left(cls.minutes, minutes)
                cls.minutes.insert(index_to_insert, minutes)

            else:
                cls.minutes.remove(minutes)

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




