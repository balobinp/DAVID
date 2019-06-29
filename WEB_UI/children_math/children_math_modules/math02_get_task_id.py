import sqlite3
import numpy as np

def math_get_task_id(username, db_path):
    # Collect the data from database
    query1 = f"""SELECT MIN(id) AS TASK_ID FROM children_math_contest01 WHERE id NOT IN \
    (SELECT TASK_ID FROM V_CHILDREN_MATH_TASK02_DETAILED WHERE USER_NAME = '{username}' AND USER_RESULT = 1);"""

    query2 = "SELECT DISTINCT ID FROM children_math_contest01;"

    con = sqlite3.connect(db_path)
    task_id = con.execute(query1).fetchone()[0]

    cursor = con.cursor()
    cursor.execute(query2)  # .fetchall()
    all_task_id = []
    for row in cursor:
        all_task_id.append(row[0])

    con.close()

    random_task_id = np.random.choice(all_task_id, 1)[0]

    if task_id:
        return task_id
    else:
        return random_task_id