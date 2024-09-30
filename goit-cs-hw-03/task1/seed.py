import faker
import random


def generate_fake_data(number_users, number_tasks, conn) -> tuple:
    fake = faker.Faker()
    fake_users = []
    fake_tasks = []

    cur = conn.cursor()

    for _ in range(number_users):
        name = fake.name()
        email = fake.unique.email()
        fake_users.append((name, email))

    #  Receive all statuses
    cur.execute("SELECT id FROM status")
    status_ids = [row[0] for row in cur.fetchall()]

    if not status_ids:
        raise ValueError(
            "Таблица 'status' пуста. Пожалуйста, вставьте статусы перед генерацией задач."
        )

    for _ in range(number_tasks):
        title = fake.sentence()
        description = fake.paragraph()
        status_id = random.choice(status_ids)
        user_id = random.randint(1, number_users)
        fake_tasks.append((title, description, status_id, user_id))

    return fake_users, fake_tasks


def insert_users_to_db(users, conn):
    try:
        cur = conn.cursor()
        insert_query = """
        INSERT INTO users (fullname, email)
        VALUES (%s, %s)
        """
        cur.executemany(insert_query, users)
        conn.commit()
        print(f"Вставлено {len(users)} пользователей в таблицу users.")
    except Exception as e:
        print(f"Ошибка при вставке данных: {e}")
    finally:
        cur.close()


def insert_tasks_to_db(tasks, conn):
    try:
        cur = conn.cursor()
        insert_query = """
        INSERT INTO tasks (title, description, status_id, user_id)
        VALUES (%s, %s, %s, %s)
        """
        cur.executemany(insert_query, tasks)
        conn.commit()
        print(f"Вставлено {len(tasks)} задач в таблицу tasks.")
    except Exception as e:
        print(f"Ошибка при вставке данных: {e}")
    finally:
        cur.close()


def insert_status_to_db(status, conn):
    try:
        cur = conn.cursor()
        insert_status_query = """
        INSERT INTO status (name) VALUES (%s)
        """
        cur.executemany(insert_status_query, [(s,) for s in status])
        conn.commit()
        print(f"Вставлено {len(status)} статусов в таблицу status.")
    except Exception as e:
        print(f"Ошибка при вставке данных: {e}")
    finally:
        cur.close()
