import psycopg2
from info_db import db_params
from create_db import create_db
from seed import (
    generate_fake_data,
    insert_users_to_db,
    insert_tasks_to_db,
    insert_status_to_db,
)
from queries import do_queries


def main():
    NUMBER_USERS = 50
    NUMBER_TASKS = 100
    TASK_STATUS = ["new", "in progress", "completed"]

    create_db()
    conn = psycopg2.connect(**db_params)

    insert_status_to_db(TASK_STATUS, conn)

    # Generate fake data
    fake_users, fake_tasks = generate_fake_data(NUMBER_USERS, NUMBER_TASKS, conn)

    # Insert data in table
    insert_users_to_db(fake_users, conn)
    insert_tasks_to_db(fake_tasks, conn)
    # Close connection
    do_queries(conn)
    conn.close()


if __name__ == "__main__":
    main()
