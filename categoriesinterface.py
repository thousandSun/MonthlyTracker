from categoriesdb import CatTracker

WELCOME_MESSAGE = """
Welcome to the Category Expense Tracker!"""

USER_PROMPT = """--> 1 - add category
--> 2 - update category
--> 3 - remove category
--> 4 - help message
--> 9 - main menu
--> 0 - credits

Make a selection: """

HELP_MESSAGE = """Welcome to Help

Option 1 - add category
    allows you to add an expense category

Option 2 - update category
    allows you to add money spent to specified category

Option 3 - remove category
    removes specified category

Option 4 - help message
    shows this rather useful help message

Option 9 - main menu
    go back to the main menu

Option 0 - show credits
    displays the credit message"""

CREDITS_MESSAGE = """
!!!!!!!!!!!!!!!!!!!!!!!!!
Written by Filiberto Rios
!!!!!!!!!!!!!!!!!!!!!!!!!
*************
Contributors:
*************
"""

db = CatTracker()


def menu():
    db.create_table()
    print(WELCOME_MESSAGE)
    choice = ''

    while choice != 9:
        db.show_categories()
        print("You have the following options available:")
        try:
            choice = int(input(USER_PROMPT))
        except ValueError:
            choice = 999999

        if choice == 1:
            add()
        elif choice == 2:
            update()
        elif choice == 3:
            remove()
        elif choice == 4:
            print(HELP_MESSAGE)
        elif choice == 0:
            print(CREDITS_MESSAGE)


def add():
    name = input("Category name: ").lower()
    db.add_category(name)


def update():
    name = input("Category name: ").lower()
    amount = _to_float(input("Amount: $"))

    if amount is not None:
        db.update_category(name, amount)
    else:
        print("!! Invalid amount !!")


def remove():
    name = input("Category name: ").lower()
    db.remove(name)


def _to_float(variable):
    variable = variable.split(",")
    variable = ''.join(variable)

    try:
        variable = float(variable)
        return variable
    except TypeError:
        return None


if __name__ == '__main__':
    menu()
