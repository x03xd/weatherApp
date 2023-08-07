from data_text import get_credentials
from database_connection import db
import requests
import schedule
import time
import ctypes

class HourlyScheduler:

    email = None

    @classmethod
    def get_request(cls):
        key = "f28885ea1b07d58b3b777554dc61e2e0"
        hour = time.strftime("%H")

        query = """SELECT cities FROM timers WHERE user_email = %s AND hour = %s"""
        params = (cls.email, hour)

        cities = db.execute_query(query, params)

        for city in cities:
            url = f"http://api.openweathermap.org/data/2.5/weather?appid={key}&q={city}"
            response = requests.get(url).json()
            print(response)


    @classmethod
    def run(cls):
        cls.email = get_credentials()[0]
        schedule.every().hour.at(":00").do(cls.get_request)

        while True:
            schedule.run_pending()
            time.sleep(1)




