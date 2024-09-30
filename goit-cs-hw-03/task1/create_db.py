import psycopg2
from psycopg2 import sql
from info_db import db_params


def create_db():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="root",
        host="localhost",
        port="5432",
    )

    # Set auto commit
    conn.autocommit = True

    cur = conn.cursor()

    new_db_name = db_params["dbname"]

    # Checking for db existence
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (new_db_name,))
    exists = cur.fetchone()

    if exists:
        # Disconn users from db 
        cur.execute(
            sql.SQL(
                "SELECT pg_terminate_backend(pg_stat_activity.pid) "
                "FROM pg_stat_activity "
                "WHERE pg_stat_activity.datname = %s AND pid <> pg_backend_pid()"
            ),
            (new_db_name,),
        )

        # Delete db if exis
        drop_db_query = sql.SQL("DROP DATABASE {}").format(sql.Identifier(new_db_name))
        cur.execute(drop_db_query)
        print(f"База данных '{new_db_name}' успешно удалена.")

    # Create new db 
    create_db_query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(new_db_name))
    cur.execute(create_db_query)
    print(f"База данных '{new_db_name}' успешно создана.")

    conn.commit()
    cur.close()
    conn.close()

    conn = psycopg2.connect(**db_params)

    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS tasks")
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("DROP TABLE IF EXISTS status")

    # SQL-for new tables 
    create_users_table = """
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(100),
        email VARCHAR(100) UNIQUE
    );
    """

    create_status_table = """
    CREATE TABLE status (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE
    );
    """

    create_tasks_table = """
    CREATE TABLE tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100),
        description TEXT,
        status_id INTEGER REFERENCES status(id) ON UPDATE CASCADE,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
    );
    """

    cur.execute(create_users_table)
    cur.execute(create_status_table)
    cur.execute(create_tasks_table)

    conn.commit()
    cur.close()
    conn.close()
