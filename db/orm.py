import mysql.connector
import configparser
from db_connection import DatabaseFactory


config = configparser.ConfigParser()
config.read('config.ini')

host = config.get('database', 'host')
database = config.get('database', 'database')
user = config.get('database', 'user')
password = config.get('database', 'password')

# connection = DatabaseFactory.create_connection(host, database, user, password)
