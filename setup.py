import click
from data_text import get_credentials
from database_connection import db
import bisect


class SetupHubQueries:
    def __init__(self):
        self.email = get_credentials()[0]
        self.minutes = []
        self.cities = None
        self.hour = None

    def restart_cities(self):
        query = """UPDATE timers SET cities = '{}' WHERE user_email = %s;"""
        params = (self.email,)
        db.execute_query(query, params, "UPDATE")
        click.echo("Cities have been removed.")

    def restart_minutes_timers(self):
        query = """UPDATE users SET minutes = '{}' WHERE email = %s;"""
        params = (self.email,)
        db.execute_query(query, params, "UPDATE")
        click.echo("Minutes timers have been removed.")

    def create_new_timer(self):
        query_insert = """INSERT INTO timers(hour, user_email, cities) VALUES(%s, %s, %s);"""
        params_insert = (self.hour, self.email, [])
        db.execute_query(query_insert, params_insert, "INSERT")

    def fetch_timer_by_user__email_hour(self):
        query = """SELECT cities FROM timers WHERE user_email = %s AND hour = %s"""
        params = (self.email, self.hour)
        result = db.execute_query(query, params, "SELECT")

        return result

    def fetch_user_by_email_ordered(self):
        query = """SELECT minutes FROM users WHERE email = %s ORDER BY minutes;"""
        params = (self.email,)

        result, minutes_array = db.execute_query(query, params, "SELECT")
        self.minutes = minutes_array[0]

    def update_user_minutes(self, operation, minutes):
        query = f"""UPDATE users SET minutes = ARRAY_{operation}(minutes, %s) WHERE email = %s;"""

        params = (minutes, self.email)
        db.execute_query(query, params, "UPDATE")

    def update_timer_city(self, city, operation):
        query = f"""UPDATE timers SET cities = ARRAY_{operation}(cities, %s) WHERE user_email = %s AND hour = %s;"""
        params = (city, self.email, self.hour)

        db.execute_query(query, params, "UPDATE")


class SetupHub(SetupHubQueries):

    def setup(self):
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
                self.hours()
            elif choice == 2:
                self.minutes_method()
            elif choice == 3:
                self.restart_cities()
            elif choice == 4:
                self.restart_minutes_timers()
            elif choice == 5:
                click.echo("Exiting the program. Goodbye!")
                break
            else:
                click.echo("Invalid choice. Please try again.")

    def hours(self):
        while True:
            hour = click.prompt("Please enter an hour", type=str)
            self.hour = hour

            if "0" > hour > "23":
                click.echo("The input must have range <0, 23>")
                continue

            result, record = self.fetch_timer_by_user__email_hour()

            if record is None:
                self.create_new_timer()

            self.cities = record[0] if record is not None else []
            self.city_interface()

    @staticmethod
    def validate_minutes_method(minutes):
        if not minutes.isdigit() or len(minutes) > 2 or len(minutes) == 0:
            click.echo("The input is not accepted because of characters other than numbers. Try again.")
            return False

        if 0 > int(minutes) > 60:
            click.echo("The input is not accepted because of violate the constraint -> Range <0, 59>. Try again.")
            return False


    def minutes_method(self):
        self.fetch_user_by_email_ordered()
        click.echo(f"Minutes: {self.minutes}")

        while True:
            minutes = click.prompt("Add minute timer in which the notification should be displayed."
                                   " Range <0, 59>. If it already exists, it will be removed", type=str)

            if not self.validate_minutes_method():
                continue

            if len(minutes) == 1:
                minutes = "0" + minutes

            operation = "REMOVE" if minutes in self.minutes else "APPEND"
            self.update_user_minutes(operation, minutes)

            if operation == "APPEND":
                index_to_insert = bisect.bisect_left(self.minutes, minutes)
                self.minutes.insert(index_to_insert, minutes)

            else:
                self.minutes.remove(minutes)

            click.echo(f"Minutes: {self.minutes}")

    def city_interface(self):
        click.echo("You can either provide new city typing its name or remove existing doing the same things"
                   "If you provide not existing city you will receive info about this in the console while good ones will be shown")

        while True:
            click.echo(f"Hour: {self.hour}, Cities: {self.cities}")

            city = click.prompt("Enter a city")
            city = city.lower()

            if city in self.cities:
                self.remove_city(city)

            else:
                cities_length = len(self.cities)

                if cities_length >= 3:
                    click.echo("You cannot add new city (limit equals 3)")

                else:
                    self.add_city(city)

    def remove_city(self, city):
        if city in self.cities:
            self.update_timer_city(city, "REMOVE")
            self.cities.remove(city)

        self.city_interface()

    def add_city(self, city):
        if city in self.cities:
            click.echo("Given city is already in your choices")
        else:
            self.update_timer_city(city, "APPEND")
            self.cities.append(city)

        self.city_interface()


if __name__ == "__main__":
    setup = SetupHub()


