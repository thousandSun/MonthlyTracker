import database

USER_PROMPT = """--> 1 - add expense
--> 2 - make payment
--> 3 - remove expense
--> 4 - quick pay
--> 5 - help
--> 9 - exit program
--> 0 - show credits

Make a selection: """

WELCOME_MESSAGE = """Welcome to the Monthly Expense Tracker v0.2!
you have the following options available:"""

HELP_MESSAGE = """Welcome to Help

Option 1 - add expense
    this option lets you add a monthly expenditure to your list of
    expenses

Option 2 - make payment
    this option allows you to enter a custom payment amount that
    will be saved to use in `quick pay` functionality

option 3 - remove expense
    this option does what it says, it removes a specific expense

Option 4 - quick pay
    this option allows you to use last months payment amount as
    this months payment amount, you don't enter a payment amount

Option 5 - help
    show this somewhat useful help message

Option 9 - exit program
    closes the program

Option 0 - show credits
    shows the author and the contributors to this project
"""

CREDITS_MESSAGE = """
!!!!!!!!!!!!!!!!!!!!!!!!!
Written by Filiberto Rios
!!!!!!!!!!!!!!!!!!!!!!!!!
This is my first "real-world" application, will be trying to add
more features shortly if you have any ideas please contact me at
filibertoerios@gmail.com with ideas and be added to the credits.

if you happen to find a bug, also contact me at the email above
including the data passed into the program that caused the bug
i'll be happy to take a look at it

*********************************
Contributors: Cpt Eman since v0.1
*********************************
"""


def menu():
    database.create_file()
    user_choice = ""
    print(WELCOME_MESSAGE)
    while user_choice != 9:
        database.show_payments()
        try:
            user_choice = int(input(USER_PROMPT))
        except ValueError:
            user_choice = 9999

        if user_choice == 1:
            add_expense()
        elif user_choice == 2:
            make_payment()
        elif user_choice == 3:
            remove_expense()
        elif user_choice == 4:
            quick_pay()
        elif user_choice == 5:
            show_help()
        elif user_choice == 0:
            print(CREDITS_MESSAGE)
        elif user_choice == 9:
            print("Goodbye")
        else:
            print("Invalid input, try again.")


def add_expense():
    expense = input("Payment name: ").lower()
    total = _convert_to_float(input("Total amount due: $"))
    amount = _convert_to_float(input("Monthly payment amount: $"))

    database.add_expense(expense, amount, total)


def make_payment():
    bill = input("For what expense are you making a payment: ").lower()
    if database._find_bill(bill):
        amount = _convert_to_float(input("Payment amount: $"))
        database.process_payment(expense, amount)
    else:
	print("!! Expense not found !!")


def remove_expense():
    expense = input("What payment do you want to remove: ").lower()
    database.remove(expense)


def quick_pay():
    expense = input("Expense: ")

    database.quick_pay(expense)


def show_help():
    print(HELP_MESSAGE)


def _convert_to_float(variable):
    variable = variable.split(",")
    variable = "".join(variable)
    return float(variable)


menu()
