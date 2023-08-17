from data_text import get_credentials
import requests
import schedule
import time
from window import create_notification
import click
from common_query_utility import SelectQueryUtility

class HourlyScheduler:
    def __init__(self):
        self.email = get_credentials()[0]
        self.select_query_utility = SelectQueryUtility()

    def get_request(self):
        key = "f28885ea1b07d58b3b777554dc61e2e0"
        hour = time.strftime("%H")

        status, cities = self.select_query_utility.fetch_timer_by_user__email_and_hour(self.email, hour)

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
        result, minutes = self.select_query_utility.fetch_user_by_email(self.email, "minutes")

        for minute_timer in minutes[0]:
            schedule.every().hour.at(f":{minute_timer}").do(self.get_request)

        while True:
            schedule.run_pending()
            time.sleep(1)


