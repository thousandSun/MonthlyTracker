import tzlocal
from billsdb import BillTracker

WELCOME_MESSAGE = """
Welcome to MonthlyTracker!"""

USER_PROMPT = """--> 1 - add bill
--> 2 - make payment
--> 3 - remove bill
--> 4 - quick pay
--> 5 - update bill
--> 6 - show logs
--> 7 - help
--> 9 - main menu
--> 0 - show credits

Make a selection: """

HELP_MESSAGE = """Welcome to Help

Option 1 - add bill
    this option lets you add a monthly expenditure to your list of
    expenses

Option 2 - make payment
    this option allows you to enter a custom payment amount that
    will be saved to use in `quick pay` functionality

option 3 - remove bill
    this option does what it says, it removes a specific expense

Option 4 - quick pay
    this option allows you to use last months payment amount as
    this months payment amount, you don't enter a payment amount

Option 5 - update bill
    allows you to change the name, remaining balance, and payment amount of an expense
    (ex. your current credit card remaining balance is $500, you make a $50 purchase increasing the remaining balance to $550)

Option 6 - show logs
    displays payments you've made in a friendly to read manner

Option 7 - help
    shows this somewhat useful help message

Option 9 - main menu
    returns to the main menu

Option 0 - show credits
    shows the author and the contributors to this project
"""

CREDITS_MESSAGE = """
!!!!!!!!!!!!!!!!!!!!!!!!!
Written by Filiberto Rios
!!!!!!!!!!!!!!!!!!!!!!!!!
*************
Contributors:
*************
"""

db = BillTracker()


def menu():
    db.create_table()
    print(WELCOME_MESSAGE)
    user_choice = ''
    while user_choice != 9:
        db.show_expenses()
        print("You have the following options available:")
        try:
            user_choice = int(input(USER_PROMPT))
        except ValueError:
            print('!! Invalid Selection !!')
            continue

        if user_choice == 1:
            add()
        elif user_choice == 2:
            make_payment()
        elif user_choice == 3:
            remove()
        elif user_choice == 4:
            quick_pay()
        elif user_choice == 5:
            update()
        elif user_choice == 6:
            show_log()
        elif user_choice == 7:
            print(HELP_MESSAGE)
        elif user_choice == 0:
            print(CREDITS_MESSAGE)


def add():
    name = input("Bill name: ").lower()
    isalpha = name.isalnum()
    if not isalpha and (name.find(" ") == -1):
        print('!! Invalid Name !!')
        return
    total = _to_float(input("Total : $"))
    payment = _to_float(input("Payment: $"))

    if total is not None and payment is not None:
        db.add_bill(name, payment, total)
    else:
        print(f'{"!! Invalid total amount" if total is None else "!! Invalid payment amount"}, try again !!')


def make_payment():
    name = input("Bill name: ").lower()
    payment = _to_float(input("Payment: $"))

    if payment is not None:
        db.make_payment(name, payment)
    else:
        print('!! Invalid payment amount !!')


def remove():
    name = input("Bill to remove: ")
    db.remove(name)


def quick_pay():
    name = input("Bill name: ")
    db.quick_pay(name)


def update():
    name = input("Bill name: ")
    db.update_bill(name)


def _to_float(variable):
    variable = variable.split(',')
    variable = ''.join(variable)

    try:
        variable = float(variable)
    except ValueError:
        return None

    return variable


def show_log():
    with open("log.log") as f:
        logs = f.readlines()
        logs = [log.strip().split(" : ") for log in logs if "Payment" in log]

    tz = tzlocal.get_localzone()
    for log in logs:
        date, time, expense_type = log[0].split()
        if 'PAID IN FULL' in log[1]:
            payment = log[1]
        else:
            payment = log[1][:-6]
        message = f'{expense_type}: {payment} on {date} at {time} {tz}'
        print("*"*len(message))
        print(message)
        print("*" * len(message))
    print(" END OF LOG ".center(40, "!"))


if __name__ == '__main__':
    menu()
    # show_log()
