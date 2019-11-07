from database_connection import DatabaseConnection

bills_db = "bills.db"


def create_table():
    with DatabaseConnection(bills_db) as connection:
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS bills(name text primary key, total real, payment real, "
                       "remaining real, paid real, complete BIT)")


def show_expenses():
    expenses = _get_bills()

    for bill in expenses:
        bill_name = bill['name']
        if not bool(bill['complete']):
            bill_total = bill['total']
            bill_payment = bill['payment']
            bill_remaining = bill['remaining']
            bill_paid = bill['paid']

            bill_string = f'| {bill_name.title()}: Total: ${bill_total:,.2f} Payment: ${bill_payment:,.2f} ' \
                          f'Remaining: ${bill_remaining:,.2f} Paid to Date: ${bill_paid:,.2f} |'
            print("-" * len(bill_string))
            print(bill_string)
            print("-" * len(bill_string))
        else:
            bill_string = f'| {bill_name.title()}: PAID IN FULL |'
            print('-' * len(bill_string))
            print(bill_string)
            print('-' * len(bill_string))


def add_bill(name, payment, total):
    with DatabaseConnection(bills_db) as connection:
        cursor = connection.cursor()

        cursor.execute('INSERT INTO bills VALUES(?, ?, ?, ?, ?, ?)', (name, total, payment, total, 0, 0))


def make_payment(name, amount):
    with DatabaseConnection(bills_db) as connection:
        cursor = connection.cursor()

        try:
            cursor.execute('SELECT remaining FROM bills WHERE name=?', (name,))
            expense_remaining = cursor.fetchone()[0]
            cursor.execute('SELECT paid FROM bills WHERE name=?', (name,))
            expense_paid = cursor.fetchone()[0]
        except TypeError:
            print('!! Invalid Query !!')
            return

        expense_remaining -= amount
        if expense_remaining <= 0:
            cursor.execute('UPDATE bills SET complete=? WHERE name=?', (1, name))
        else:
            expense_paid += amount
            cursor.execute('UPDATE bills SET remaining=? WHERE name=?', (expense_remaining, name))
            cursor.execute('UPDATE bills SET paid=? WHERE name=?', (expense_paid, name))
            cursor.execute('UPDATE bills SET payment=? WHERE name=?', (amount, name))


def quick_pay(name):
    with DatabaseConnection(bills_db) as connection:
        cursor = connection.cursor()

        try:
            cursor.execute('SELECT remaining FROM bills WHERE name=?', (name,))  # finish quick pay method
            expense_remaining = cursor.fetchone()[0]
            cursor.execute('SELECT payment FROM bills WHERE name=?', (name,))
            expense_payment = cursor.fetchone()[0]
            cursor.execute('SELECT paid FROM bills WHERE name=?', (name,))
            expense_paid = cursor.fetchone()[0]
        except TypeError:
            print('!! Invalid Query !!')
            return

        expense_remaining -= expense_payment
        if expense_remaining <= 0:
            cursor.execute('UPDATE bills SET complete=? WHERE name=?', (1, name))
        else:
            expense_paid += expense_payment
            cursor.execute('UPDATE bills SET remaining=? WHERE name=?', (expense_remaining, name))
            cursor.execute('UPDATE bills SET paid=? WHERE name=?', (expense_paid, name))


def remove(name):
    with DatabaseConnection(bills_db) as connection:
        cursor = connection.cursor()

        cursor.execute('DELETE FROM bills WHERE name=?', (name,))


def update_bill(name):
    with DatabaseConnection(bills_db) as connection:
        cursor = connection.cursor()

        update_string = """What property do you want to update
    --> name
    --> remaining
    --> payment
Selection: """
        if _get_bill(name) is not None:
            updated_field = input(update_string).lower()
            if updated_field == 'name':
                new_name = input('New name: ').lower()
                cursor.execute('UPDATE bills SET name=? WHERE name=?', (new_name, name))
            elif updated_field == 'remaining':
                new_total = _to_float(input('Amount spent: $'))
                if new_total is not None:
                    _add_expense(name, new_total)
            elif updated_field == 'payment':
                new_payment = _to_float(input('New payment: $'))
                if new_payment is not None:
                    cursor.execute('UPDATE bills SET payment=? WHERE name=?', (new_payment, name))
                else:
                    pass
            else:
                print('!! Invalid Selection !!')
        else:
            print("!! Invalid Query !!")


def _add_expense(name, amount):  # finish making method to add expenditure e.g. total = 500, spent = 50, remaining = 550
    expense = _get_bill(name)
    expense['remaining'] += amount

    with DatabaseConnection(bills_db) as connection:
        cursor = connection.cursor()

        cursor.execute('UPDATE bills SET remaining=? WHERE name=?', (expense['remaining'], name))


def _get_bills():
    with DatabaseConnection(bills_db) as connection:
        connection.text_factory = str
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM bills')
        expenses = [{'name': row[0], 'total': row[1], 'payment': row[2],
                     'remaining': row[3], 'paid': row[4], 'complete': row[5]} for row in cursor.fetchall()]
    return expenses


def _get_bill(name):
    with DatabaseConnection(bills_db) as connection:
        connection.text_factory = str
        cursor = connection.cursor()

        try:
            cursor.execute('SELECT * FROM bills WHERE name=?', (name,))
            expense = cursor.fetchone()
            expense = {'name': expense[0], 'total': expense[1], 'payment': expense[2],
                       'remaining': expense[3], 'paid': expense[4], 'complete': expense[5]}
        except TypeError:
            return None

    return expense


def _to_float(variable):
    variable = variable.split(',')
    variable = ''.join(variable)

    try:
        variable = float(variable)
    except ValueError:
        return None

    return variable
