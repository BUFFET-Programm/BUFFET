import sqlite3
from important_variables import DATABASE_PATH


def is_new(name: str, code: str) -> list[bool, str]:
    '''Checks the product information is unique.'''
    db = sqlite3.connect(DATABASE_PATH)
    cursor = db.execute('SELECT name,code FROM products')
    data = cursor.fetchall()
    problem = None
    output = True
    names = []
    codes = []
    for product in data:
        names.append(product[0])
        codes.append(product[1])
    if name in names and code in codes:
        problem = "b"
    elif name in names:
        problem = "n"
    elif code in codes:
        problem = "c"
    if problem:
        output = False
    db.close()
    return [output, problem]

def save_product(name: str, code: str, price: str) -> None:
    '''Inserts product information in database.'''
    db = sqlite3.connect(DATABASE_PATH)
    db.execute('INSERT INTO products (name, code, price, count) VALUES (?,?,?,?)', (name, code, price, 0))
    db.commit()
    db.close()

def read_product(code: str) -> str:
    '''Read product information from database.'''
    try:
        db = sqlite3.connect(DATABASE_PATH)
        cursor = db.execute('SELECT * FROM products WHERE code=?', (code,))
        data = list(cursor.fetchone())
        db.close()
        return data
    except TypeError:
        return False

def read_all_products() -> list:
    '''Reads all products information from database.'''
    db = sqlite3.connect(DATABASE_PATH)
    cursor = db.execute('SELECT * FROM products')
    data = cursor.fetchall()
    products = [[product[0], product[1], product[2]] for product in data]
    db.close()
    return products

def delete_product(code: str) -> None:
    '''Deletes a product from database.'''
    db = sqlite3.connect(DATABASE_PATH)
    db.execute('DElETE FROM products WHERE code=?', (code,))
    db.commit()
    db.close()

def change_product_count(products_names:list) -> None:
    '''Updates product count when it bayed by buyer.'''
    db = sqlite3.connect(DATABASE_PATH)
    for name in products_names:
        count = int(db.execute('SELECT count FROM products WHERE name=?', (name,)).fetchone()[0])
        db.execute('UPDATE products SET count=? WHERE name=?', (count+1, name))
    db.commit()
    db.close()