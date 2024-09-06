from b_buyer_log import save_log
from b_product import change_product_count
import sqlite3
from important_variables import DATABASE_PATH


def buy(name:str, products:list, price:str) -> None:
    '''Change charge of buyer when he buy something.'''
    if int(price) != 0:
        db = sqlite3.connect(DATABASE_PATH)
        cursor = db.execute('SELECT charge FROM buyers WHERE name=?', (name,))
        charge = int(cursor.fetchone()[0])
        db.execute('UPDATE buyers SET charge=? WHERE name=?', (charge-price, name))
        db.commit()
        save_log(name, 'buy', price, str(products))
        change_product_count(products)
        db.close()

def charge(name: str, price: str) -> None:
    '''Change charge of buyer when he charge his credit.'''
    if int(price) != 0:
        db = sqlite3.connect(DATABASE_PATH)
        cursor = db.execute('SELECT charge FROM buyers WHERE name=?', (name,))
        charge = int(cursor.fetchone()[0])
        db.execute('UPDATE buyers SET charge=? WHERE name=?', (charge+price, name))
        db.commit()   
        save_log(name, 'charge', price, '[]')
        db.close()

def read_charge(name:str) -> int:
    db = sqlite3.connect(DATABASE_PATH)
    cursor = db.execute('SELECT charge from buyers WHERE name=?', (name,))
    charge = int(cursor.fetchone()[0])
    db.close()
    return charge