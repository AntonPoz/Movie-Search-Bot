import sqlite3


with sqlite3.connect('test_database.db') as conn:
    # add_student_1 = f'INSERT INTO students (name, surname) VALUES ("Ivan", "Ivanov");'
    # add_student_2 = f'INSERT INTO students (name, surname) VALUES ("Petr", "Petrov");'
    # add_student_3 = f'INSERT INTO students (name, surname) VALUES ("Anna", "Annova");'
    # conn.commit()
    cursor = conn.cursor()
    # cursor.execute(create_table_query)
    # cursor.execute(add_student_1)
    # cursor.execute(add_student_2)
    # cursor.execute(add_student_3)
    # cursor.execute("UPDATE students SET id = 3 WHERE id = 4")
    # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # cursor.execute("SELECT * FROM 'request';")
    # add_student_1 = f'INSERT INTO request (id, movie_title) VALUES ("1", "Ivanov");'
    # cursor.execute(add_student_1)
    cursor.execute("SELECT * FROM 'response';")
    # cursor.execute("DROP table 'response';")
    # print(cursor.fetchall())
    # cursor.execute("PRAGMA table_info(movie);")

    print(cursor.fetchall())