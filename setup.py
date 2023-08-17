import click
from data_text import get_credentials
import bisect
from common_query_utility import SelectQueryUtility, InsertQueryUtility, UpdateQueryUtility

class SetupHub():
    def __init__(self):
        self.email = get_credentials()[0]
        self.minutes = []
        self.cities = None
        self.hour = None

        self.select_query_utility = SelectQueryUtility()
        self.insert_query_utility = InsertQueryUtility()
        self.update_query_utility = UpdateQueryUtility()

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
                self.update_query_utility.restart_cities(self.email)
                click.echo("Cities have been removed.")
            elif choice == 4:
                self.update_query_utility.restart_minutes_timers(self.email)
                click.echo("Minutes timers have been removed.")
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

            result, record = self.select_query_utility.fetch_timer_by_user__email_hour(self.email, self.hour)

            if record is None:
                self.insert_query_utility.create_new_timer(self.hour, self.email)

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
        result, minutes_array = self.select_query_utility.fetch_user_by_email(self.email, "minutes", " ORDER BY minutes;")
        self.minutes = minutes_array[0]

        click.echo(f"Minutes: {self.minutes}")

        while True:
            minutes = click.prompt("Add minute timer in which the notification should be displayed."
                                   " Range <0, 59>. If it already exists, it will be removed", type=str)

            if not self.validate_minutes_method():
                continue

            if len(minutes) == 1:
                minutes = "0" + minutes

            operation = "REMOVE" if minutes in self.minutes else "APPEND"
            self.update_query_utility.update_user_minutes(operation, minutes, self.email)

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

    def __remove_city(self, city):
        if city in self.cities:
            self.update_query_utility.update_timer_city(city, "REMOVE", self.email, self.hour)
            self.cities.remove(city)
        self.city_interface()

    def __add_city(self, city):
        if city in self.cities:
            click.echo("Given city is already in your choices")
        else:
            self.update_query_utility.update_timer_city(city, "APPEND", self.email, self.hour)
            self.cities.append(city)
        self.city_interface()

