# database.py
import mysql.connector

def setup_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kahitano1",
        database="EuWall"
    )