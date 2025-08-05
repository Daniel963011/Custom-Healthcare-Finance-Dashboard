import mysql.connector

def db_connection():
    return mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'hazellnut',
        database = 'healthcare_finance'
    )