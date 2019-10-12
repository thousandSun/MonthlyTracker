import json

"""
JSON object will be
[
    {'category': string_value, 'spent': float_value}
]
"""

categories_file = "categories.json"


def create_file():  # makes sure file is there
    try:
        with open(categories_file, 'x') as file:
            json.dump([], file)
    except FileExistsError:
        pass


def show_categories():
    categories = _get_categories()

    for category in categories:
        category_name = category['category']
        category_spent = category['spent']

        category_string = f'| {category_name.title()}: Total spent: ${category_spent:,.2f} |'
        print("-"*len(category_string))
        print(category_string)
        print("-"*len(category_string))


def add_category(name):
    categories = _get_categories()

    categories.append({
        'category': name,
        'spent': 0.0
    })

    _write_file(categories)


def remove(name):
    categories = _get_categories()
    categories = [category for category in categories if category['category'] != name]

    _write_file(categories)


def add_expense(name, amount):
    index, category = _get_category(name)

    if category is not None:
        category['spent'] += amount
        _update_and_write(index, category)


def find_category(name):
    categories = _get_categories()
    return any(category['category'] == name for category in categories)


def _get_categories():
    with open(categories_file, 'r') as file:
        return json.load(file)


def _write_file(categories):
    with open(categories_file, "w") as file:
        json.dump(categories, file)


def _get_category(name):
    categories = _get_categories()
    for index, category in enumerate(categories):
        if category['category'] == name:
            return index, category


def _update_and_write(index, category):
    categories = _get_categories()
    categories[index] = category

    _write_file(categories)
