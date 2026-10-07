import os
import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="gestor_tareas",
        user="postgres",
        password=os.getenv("DB_PASSWORD")
    )


def create_tables():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT FALSE
            )
            """)


create_tables()