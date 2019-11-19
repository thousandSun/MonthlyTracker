import billsinterface
import categoriesinterface

WELCOME_MESSAGE = """Welcome to Expense Tracker v1.0
You have the following options available:"""

USER_PROMPT = """--> 1 - Bills Tracker
--> 2 - Categorical Tracker
--> 3 - Help
--> 4 - Exit
--> 0 - Credits

Make your selection: """

HELP_MESSAGE = """Welcome to Help
Option 1 - Bills Tracker
    allows you to keep your bill payments all in one place

Option 2 - Categorical Tracker
    allows you to create categories of expenses and track how much you've spent
    e.g. groceries, movies, gas, etc.

Option 3 - Help
    displays this help message

Option 4 - Exit
    exits the program

Option 0 - Credits
    displays credits message
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
I'll be happy to take a look at it
"""


def start():
    print(WELCOME_MESSAGE)
    user_choice = ""

    while user_choice != 4:
        print()
        print("Main Menu:")
        try:
            user_choice = int(input(USER_PROMPT))
        except ValueError:
            user_choice = 9999

        if user_choice == 1:
            billsinterface.menu()
        elif user_choice == 2:
            categoriesinterface.menu()
        elif user_choice == 3:
            print(HELP_MESSAGE)
        elif user_choice == 4:
            print("Goodbye")
        elif user_choice == 0:
            print(CREDITS_MESSAGE)
        else:
            print("Invalid input, try again")


start()
