import psycopg2
import os
from dotenv import main
main.load_dotenv()

class DatabaseConnection:
    __instance = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, db_name, user, password, host="localhost", port="5432"):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
        except psycopg2.Error as e:
            print(f"Error connecting to {self.db_name}: {e}")

    def execute_query(self, query, params=None, operation_type="SELECT"):
        try:
            cursor = self.connection.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            self.connection.commit()

            if operation_type == "SELECT":
                result = cursor.fetchone()

                if result is not None:
                    return True, result

                else:
                    return False, result

            elif operation_type == "INSERT":
                return True

            elif operation_type == "UPDATE":
                return True

        except psycopg2.Error as e:
            print(f"Error executing query: {e}")

    def close(self):
        if self.connection:
            self.connection.close()


DB_NAME = os.getenv('DB_NAME')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')

db = DatabaseConnection(DB_NAME, USER, PASSWORD)
db.connect()

