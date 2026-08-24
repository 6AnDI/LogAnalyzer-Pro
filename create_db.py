import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

connection = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="Docker@123",
    host="localhost",
    port=5432
)

connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = connection.cursor()

try:
    cursor.execute("CREATE DATABASE security_logs_db;")
    print("Database 'security_logs_db' created successfully!")
except Exception as e:
    print("Notice:", e)

cursor.close()
connection.close()
