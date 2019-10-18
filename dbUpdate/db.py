import sqlite3


def create_table():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS expenses(name text primary key, total real, payment real, remaining real, paid real)")

    connection.commit()
    connection.close()


def add_expense(name, total, payment):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO expenses VALUES(?, ?, ?, ?, ?)', (name, total, payment, total, 0))


    connection.commit()
    connection.close()


def get_values():
    connection = sqlite3.connect("data.db")
    connection.text_factory = str
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM expenses')
    expenses = [{'name': row[0], 'total': row[1], 'payment': row[2], 'remaining': row[3], 'paid': row[4]} for row in cursor.fetchall()]  # gives a list of tuples
    print(expenses)

    connection.close()


create_table()
#add_expense('house', 200000, 1145.6)
get_values()
