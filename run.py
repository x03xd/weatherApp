from data_text import get_credentials
from database_connection import db
import requests
import schedule
import time
from window import create_notification
import click


class HourlyScheduler:
    def __init__(self):
        self.email = get_credentials()[0]

    def fetch_timer_by_user__email_and_hour(self, hour):
        query = """SELECT cities FROM timers WHERE user_email = %s AND hour = %s"""
        params = (self.email, hour)
        result = db.execute_query(query, params)

        return result

    def fetch_user_by_email(self):
        query = """SELECT minutes FROM users WHERE email = %s"""
        params = (self.email,)

        result = db.execute_query(query, params)

        return result

    def get_request(self):
        key = "f28885ea1b07d58b3b777554dc61e2e0"
        hour = time.strftime("%H")

        status, cities = self.fetch_timer_by_user__email_and_hour(hour)

        if status:
            for city in cities[0]:
                url = f"http://api.openweathermap.org/data/2.5/weather?appid={key}&q={city}&units=metric"

                try:
                    response = requests.get(url).json()
                    create_notification(response, city)

                except Exception as e:
                    click.echo(f"Error fetching weather data for '{city}': {e}")
                    return None

        else:
            click.echo("There are no cities for current hour")

    def run(self):
        result, minutes = self.fetch_user_by_email()

        for minute_timer in minutes[0]:
            schedule.every().hour.at(f":{minute_timer}").do(self.get_request)

        while True:
            schedule.run_pending()
            time.sleep(1)

