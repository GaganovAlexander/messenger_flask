import psycopg2.extras
from configs import *


conn = psycopg2.connect(host="localhost", port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)