from database_connection import DatabaseConnection

categories_database = "categories.db"


def create_table():
    with DatabaseConnection(categories_database) as connection:
        cursor = connection.cursor()

        cursor.execute('CREATE TABLE IF NOT EXISTS categories(name text primary key, total real)')


def show_categories():
    categories = _get_categories()

    for category in categories:
        name = category['category']
        total = category['total']

        cat_str = f'| {name.title()}: ${total:,.2f} |'
        print('-'*len(cat_str))
        print(cat_str)
        print('-'*len(cat_str))


def add_category(name):
    with DatabaseConnection(categories_database) as connection:
        cursor = connection.cursor()

        cursor.execute('INSERT INTO categories VALUES(?, ?)', (name, 0))


def update_category(name, amount):
    category = _get_category(name)

    if category is not None:
        total = category['total']
        total += amount
        with DatabaseConnection(categories_database) as connection:
            cursor = connection.cursor()

            cursor.execute('UPDATE categories SET total=? WHERE name=?', (total, name))


def remove(name):
    with DatabaseConnection(categories_database) as connection:
        cursor = connection.cursor()

        cursor.execute('DELETE FROM categories WHERE name=?', (name,))


def _get_category(name):
    with DatabaseConnection(categories_database) as connection:
        connection.text_factory = str
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT * FROM categories WHERE name=?', (name,))
            category = cursor.fetchone()
            category = {'category': category[0], 'total': category[1]}

            return category
        except TypeError:
            return None


def _get_categories():
    with DatabaseConnection(categories_database) as connection:
        connection.text_factory = str
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM categories')

        categories = [{'category': row[0], 'total': row[1]} for row in cursor.fetchall()]

        return categories
