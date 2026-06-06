import psycopg2

def get_connection():

    return psycopg2.connect(
        host="localhost",
        database="waluty",
        user="postgres",
        password="postgres"
    )