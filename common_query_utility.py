from abc import ABC
from database_connection import db

class AbstractUtilityCategory(ABC):
    def __init__(self, email):
        self.email = email

class SelectQueryUtility(AbstractUtilityCategory):
    def fetch_timer_by_user__email_and_hour(self, hour):
        query = """SELECT cities FROM timers WHERE user_email = %s AND hour = %s;"""
        params = (self.email, hour)
        result = db.execute_query(query, params)
        return result

    def fetch_user_by_email(self, columns, rest=""):
        query = f"""SELECT {columns} FROM users WHERE email = %s{rest};"""
        params = (self.email,)
        result = db.execute_query(query, params)
        return result

    @staticmethod
    def is_user_logged(credentials):
        if credentials:
            email, hashed_password = credentials
            query = """SELECT * FROM users WHERE email = %s AND password = %s"""
            params = (email, hashed_password)
            result, record = db.execute_query(query, params, "SELECT")
            return result



class UpdateQueryUtility(AbstractUtilityCategory):
    def restart_cities(self):
        query = """UPDATE timers SET cities = '{}' WHERE user_email = %s;"""
        params = (self.email,)
        db.execute_query(query, params, "UPDATE")

    def restart_minutes_timers(self):
        query = """UPDATE users SET minutes = '{}' WHERE email = %s;"""
        params = (self.email,)
        db.execute_query(query, params, "UPDATE")

    def update_user_minutes(self, operation, minutes):
        query = f"""UPDATE users SET minutes = ARRAY_{operation}(minutes, %s) WHERE email = %s;"""
        params = (minutes, self.email)
        db.execute_query(query, params, "UPDATE")

    def update_timer_city(self, city, operation, hour):
        query = f"""UPDATE timers SET cities = ARRAY_{operation}(cities, %s) WHERE user_email = %s AND hour = %s;"""
        params = (city, self.email, hour)
        db.execute_query(query, params, "UPDATE")


class InsertQueryUtility(AbstractUtilityCategory):
    def create_new_user(self, hashed_password, salt):
        new_user = "INSERT INTO users(email, password, salt) VALUES (%s, %s, %s)"
        params = (self.email, hashed_password, salt)
        new_user_creation_result = db.execute_query(new_user, params, "INSERT")
        return new_user_creation_result

    def create_new_timer(self, hour):
        query_insert = """INSERT INTO timers(hour, user_email, cities) VALUES(%s, %s, %s);"""
        params_insert = (hour, self.email, [])
        db.execute_query(query_insert, params_insert, "INSERT")



