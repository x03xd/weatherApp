from data_text import get_credentials
from database_connection import db
import requests
import schedule
import time
from window import create_notification
import click


class HourlyScheduler:
    email = None

    @classmethod
    def get_request(cls):
        key = "f28885ea1b07d58b3b777554dc61e2e0"
        hour = time.strftime("%H")

        query = """SELECT cities FROM timers WHERE user_email = %s AND hour = %s"""
        params = (cls.email, hour)

        result, cities = db.execute_query(query, params)

        if result:
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

    @classmethod
    def run(cls):
        cls.email = get_credentials()[0]

        query = """SELECT minutes FROM timers WHERE user_email = s%;"""


        schedule.every().hour.at(":00").do(cls.get_request)

        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    HourlyScheduler().get_request()