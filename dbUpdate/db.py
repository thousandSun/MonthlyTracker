import sqlite3


def create_table():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS expenses(category text, name text primary key, total real, payment real, remaining real, paid real)")

    connection.commit()
    connection.close()


def add_expense(category, name, total, payment):
    conection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    #cursor.execute(f'INSERT INTO expenses VALUES("{category}", "{name}", {total}, {payment}, {total}, 0.0)')

    connection.commit()
    connection.close()


create_table()
