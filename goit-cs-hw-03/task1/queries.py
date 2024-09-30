
def do_queries(conn):

    cursor = conn.cursor()

    # 1.
    cursor.execute("SELECT * FROM tasks WHERE user_id = 6;")

    # 2. 
    cursor.execute(
        "SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = 'new');"
    )

    # 3. 
    cursor.execute(
        "UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = 'in progress') WHERE id = 6;"
    )

    # 4. 
    cursor.execute("SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks);")

    # 5. 
    cursor.execute(
        """
        INSERT INTO tasks (title, description, status_id, user_id)
        VALUES ('Clean', 'Make good clean', (SELECT id FROM status WHERE name = 'new'), 6);
    """
    )

    # 6. 
    cursor.execute(
        "SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'completed');"
    )

    # 7.
    cursor.execute("DELETE FROM tasks WHERE id = 1;")

    # 8.
    cursor.execute("SELECT * FROM users WHERE email LIKE '%org%';")

    # 9.
    cursor.execute("UPDATE users SET fullname = 'Mary' WHERE id = 11;")

    # 10.
    cursor.execute(
        """
        SELECT status.name, COUNT(tasks.id) AS task_count
        FROM tasks
        JOIN status ON tasks.status_id = status.id
        GROUP BY status.name;
    """
    )

    # 11. 
    cursor.execute(
        """
        SELECT tasks.*
        FROM tasks
        JOIN users ON tasks.user_id = users.id
        WHERE users.email LIKE '%@example.com';
    """
    )

    # 12. 
    cursor.execute("SELECT * FROM tasks WHERE description IS NULL OR description = '';")
    # 13. 
    cursor.execute(
        """
        SELECT users.fullname, tasks.title
        FROM users
        INNER JOIN tasks ON users.id = tasks.user_id
        WHERE tasks.status_id = (SELECT id FROM status WHERE name = 'in progress');
    """
    )

    # 14.
    cursor.execute(
        """
        SELECT users.fullname, COUNT(tasks.id) AS task_count
        FROM users
        LEFT JOIN tasks ON users.id = tasks.user_id
        GROUP BY users.fullname;
    """
    )

    conn.commit()
    cursor.close()
    conn.close()

    print("All queries were done")
