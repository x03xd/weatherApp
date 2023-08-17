from abc import ABC
from database_connection import db

class AbstractUtilityCategory(ABC):
    pass


class SelectQueryUtility(AbstractUtilityCategory):

    @staticmethod
    def fetch_timer_by_user__email_and_hour(email, hour):
        query = """SELECT cities FROM timers WHERE user_email = %s AND hour = %s;"""
        params = (email, hour)
        result = db.execute_query(query, params)
        return result

    @staticmethod
    def fetch_user_by_email(email, columns, rest=""):
        query = f"""SELECT {columns} FROM users WHERE email = %s{rest};"""
        params = (email,)
        result = db.execute_query(query, params)
        return result



class UpdateQueryUtility(AbstractUtilityCategory):

    @staticmethod
    def restart_cities(email):
        query = """UPDATE timers SET cities = '{}' WHERE user_email = %s;"""
        params = (email,)
        db.execute_query(query, params, "UPDATE")

    @staticmethod
    def restart_minutes_timers(email):
        query = """UPDATE users SET minutes = '{}' WHERE email = %s;"""
        params = (email,)
        db.execute_query(query, params, "UPDATE")

    @staticmethod
    def update_user_minutes(operation, minutes, email):
        query = f"""UPDATE users SET minutes = ARRAY_{operation}(minutes, %s) WHERE email = %s;"""

        params = (minutes, email)
        db.execute_query(query, params, "UPDATE")

    @staticmethod
    def update_timer_city(city, operation, email, hour):
        query = f"""UPDATE timers SET cities = ARRAY_{operation}(cities, %s) WHERE user_email = %s AND hour = %s;"""
        params = (city, email, hour)

        db.execute_query(query, params, "UPDATE")


class InsertQueryUtility(AbstractUtilityCategory):

    @staticmethod
    def create_new_user(email, hashed_password, salt):
        new_user = "INSERT INTO users(email, password, salt) VALUES (%s, %s, %s)"
        params = (email, hashed_password, salt)
        new_user_creation_result = db.execute_query(new_user, params, "INSERT")

        return new_user_creation_result

    @staticmethod
    def create_new_timer(hour, email):
        query_insert = """INSERT INTO timers(hour, user_email, cities) VALUES(%s, %s, %s);"""
        params_insert = (hour, email, [])
        db.execute_query(query_insert, params_insert, "INSERT")



