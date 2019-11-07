import dbUpdate.billsdb as db

WELCOME_MESSAGE = """Welcome to MonthlyTracker v0.4!"""

USER_PROMPT = """You have the following options available:
--> 1 - add bill
--> 2 - make payment
--> 3 - remove bill
--> 4 - quick pay
--> 5 - update bill
--> 6 - help
--> 9 - exit
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

Option 6 - help
    displays this somewhat useful help message

Option 9 - exit program
    closes the program

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


def menu():
    db.create_table()
    print(WELCOME_MESSAGE)
    user_choice = ''
    while user_choice != 9:
        db.show_expenses()
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
            print(HELP_MESSAGE)
        elif user_choice == 9:
            break
        elif user_choice == 0:
            print(CREDITS_MESSAGE)


def add():
    name = input("Bill name: ").lower()
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


menu()
