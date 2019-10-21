import sqlite3


def create_table():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS expenses(name text primary key, total real, payment real, "
                   "remaining real, paid real, complete BIT)")

    connection.commit()
    connection.close()


def show_expenses():
    expenses = _get_bills()

    for bill in expenses:
        bill_name = bill['name']
        if not bool(bill['complete']):
            bill_total = bill['total']
            bill_payment = bill['payment']
            bill_remaining = bill['remaining']
            bill_paid = bill['paid']

            bill_string = f'| {bill_name.title()}: Total: {bill_total:,.2f} Payment: {bill_payment:,.2f} ' \
                          f'Remaining: {bill_remaining:,.2f} Paid to Date: {bill_paid:,.2f} |'
            print("-" * len(bill_string))
            print(bill_string)
            print("-" * len(bill_string))
        else:
            bill_string = f'| {bill_name.title()}: PAID IN FULL |'
            print('-' * len(bill_string))
            print(bill_string)
            print('-' * len(bill_string))


def add_bill(name, payment, total):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO expenses VALUES(?, ?, ?, ?, ?, ?)', (name, total, payment, total, 0, 0))

    connection.commit()
    connection.close()


def make_payment(name, amount):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    try:
        cursor.execute('SELECT remaining FROM expenses WHERE name=?', (name,))
        expense_remaining = cursor.fetchone()[0]
        cursor.execute('SELECT paid FROM expenses WHERE name=?', (name,))
        expense_paid = cursor.fetchone()[0]
    except TypeError:
        print('!! Invalid Query !!')
        connection.close()
        return

    expense_remaining -= amount
    if expense_remaining <= 0:
        cursor.execute('UPDATE expenses SET complete=? WHERE name=?', (1, name))
        print('aaaa')
    else:
        expense_paid += amount
        cursor.execute('UPDATE expenses SET remaining=? WHERE name=?', (expense_remaining, name))
        cursor.execute('UPDATE expenses SET paid=? WHERE name=?', (expense_paid, name))
        cursor.execute('UPDATE expenses SET payment=? WHERE name=?', (amount, name))

    connection.commit()
    connection.close()


def quick_pay(name):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    try:
        cursor.execute('SELECT remaining FROM expenses WHERE name=?', (name,))  # finish quick pay method
        expense_remaining = cursor.fetchone()[0]
        cursor.execute('SELECT payment FROM expenses WHERE name=?', (name,))
        expense_payment = cursor.fetchone()[0]
        cursor.execute('SELECT paid FROM expenses WHERE name=?', (name,))
        expense_paid = cursor.fetchone()[0]
    except TypeError:
        print('!! Invalid Query !!')
        connection.close()
        return

    expense_remaining -= expense_payment
    if expense_remaining <= 0:
        cursor.execute('UPDATE expenses SET complete=? WHERE name=?', (1, name))
    else:
        expense_paid += expense_payment
        cursor.execute('UPDATE expenses SET remaining=? WHERE name=?', (expense_remaining, name))
        cursor.execute('UPDATE expenses SET paid=? WHERE name=?', (expense_paid, name))

    connection.commit()
    connection.close()


def remove(name):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('DELETE FROM expenses WHERE name=?', (name,))

    connection.commit()
    connection.close()


def update_bill(name):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    update_string = """What property do you want to update
    --> name
    --> total
    --> payment
Selection: """
    expense = _get_bill(name)
    if expense is not None:
        updated_field = input(update_string).lower()
        if updated_field == 'name':
            new_name = input('New name: ').lower()
            cursor.execute('UPDATE expenses SET name=? WHERE name=?', (new_name, name))
        elif updated_field == 'total':
            new_total = _to_float(input('New total: '))
            if new_total is not None:
                cursor.execute('UPDATE expenses SET total=? WHERE name=?', (new_total, name))
            else:
                pass
        elif updated_field == 'payment':
            new_payment = _to_float(input('New payment: '))
            if new_payment is not None:
                cursor.execute('UPDATE expenses SET payment=? WHERE name=?', (new_payment, name))
            else:
                pass
        else:
            print('!! Invalid Selection !!')
        connection.commit()
    else:
        print("!! Invalid Query !!")

    connection.close()


def add_expense(name, amount):  # finish making method to add expenditure e.g. total = 500, spent = 50, remaining = 550
    pass


def _get_bills():
    connection = sqlite3.connect("data.db")
    connection.text_factory = str
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM expenses')
    expenses = [{'name': row[0], 'total': row[1], 'payment': row[2],
                 'remaining': row[3], 'paid': row[4], 'complete': row[5]} for row in cursor.fetchall()]

    connection.close()
    return expenses


def _get_bill(name):
    connection = sqlite3.connect("data.db")
    connection.text_factory = str
    cursor = connection.cursor()

    try:
        cursor.execute('SELECT * FROM expenses WHERE name=?', (name,))
        expense = cursor.fetchone()
        expense = {'name': expense[0], 'total': expense[1], 'payment': expense[2],
                   'remaining': expense[3], 'paid': expense[4], 'complete': expense[5]}
    except TypeError:
        connection.close()
        return None

    connection.close()
    return expense


def _to_float(variable):
    variable = variable.split(',')
    variable = ''.join(variable)

    try:
        variable = float(variable)
    except ValueError:
        return None

    return variable
