import categoriesdb

WELCOME_MESSAGE = """Welcome to the Category Expense Tracker v0.1
You have the following options available:"""

USER_PROMPT = """--> 1 - add category
--> 2 - update category
--> 3 - remove category
--> 4 - help message
--> 9 - main menu
--> 0 - credits

Make a selection: """

HELP_MESSAGE = """Welcome to Help

Option 1 - add category
    allows you to add expense categories like groceries, movies, gas, etc.

Option 2 = update category
    this option lets you add expenses to the categories (e.g. spent $10 on gas)

Option 3 - remove category
    allows you to remove an expense category

Option 4 - help message
    displays this message

Option 9 - main menu
    returns to the main menu

Option 0 - credits
    displays credits message
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
    categoriesdb.create_file()
    print(WELCOME_MESSAGE)

    while True:
        categoriesdb.show_categories()
        try:
            user_choice = int(input(USER_PROMPT))
        except ValueError:
            user_choice = 9999

        if user_choice == 1:
            add_category()
        elif user_choice == 2:
            update_category()
        elif user_choice == 3:
            remove_category()
        elif user_choice == 4:
            print(HELP_MESSAGE)
        elif user_choice == 9:
            return
        elif user_choice == 0:
            print(CREDITS_MESSAGE)
        else:
            print("Invalid input, try again")


def add_category():
    name = input("Category name: ").lower()
    categoriesdb.add_category(name)


def update_category():
    name = input("Category name: ").lower()
    if categoriesdb.find_category(name):
        amount = _to_float(input("Amount spent: $"))
        if amount is not None:
            categoriesdb.add_expense(name, amount)
        else:
            print("Invalid input, try again")
    else:
        print("!! Category not found, try again !!")


def remove_category():
    name = input("Category name: ").lower()
    categoriesdb.remove(name)


def _to_float(variable):
    variable = variable.split(",")
    variable = "".join(variable)

    try:
        variable = float(variable)
    except ValueError:
        return None
    return variable
