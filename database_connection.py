import psycopg2

class DatabaseConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

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
            print(f"Connected to {self.db_name}")
        except psycopg2.Error as e:
            print(f"Error connecting to {self.db_name}: {e}")

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully.")
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection closed.")


if __name__ == "__main__":
    # Example usage:
    db_name = "weatherApp"
    user = "postgres"
    password = "admin"

    # Creating the singleton instance
    db = DatabaseConnection(db_name, user, password)
    db.connect()

    # Rest of the code remains the same...