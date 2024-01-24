import mysql.connector
from mysql.connector import Error


class DatabaseFactory:
    @staticmethod
    def create_connection(host, database, user, password):
        try:
            connection = mysql.connector.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )
            if connection.is_connected():
                print('Connected to MySQL database')
                return connection
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            return None
