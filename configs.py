from os import environ

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

DB_NAME = environ.get("DB_NAME")
DB_PASSWORD = environ.get("DB_PASSWORD")
DB_PORT = environ.get("DB_PORT")
DB_USER = environ.get("DB_USER")
MAIN_ROUTE = '/api/messenger'