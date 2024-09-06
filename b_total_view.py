from important_variables import DATABASE_PATH, LANGUAGE_PATH
import matplotlib.pyplot as plt
import sqlite3
from bidi.algorithm import get_display
from arabic_reshaper import reshape
from datetime import date as d ,timedelta


def show_the_most_purchased_products() -> plt.bar:
    '''A good and helpful plt for show the must purchased products!'''
    try:
        db = sqlite3.connect(DATABASE_PATH)
        cursor = db.execute('SELECT name,count FROM products')
        dict = {get_display(reshape(row[0])):row[1] for row in cursor}
        with open(LANGUAGE_PATH, 'r') as file:
            lang = file.read()
        for key, value in dict.items():
            plt.bar(key, value)
        if lang=='per':
            plt.title(get_display(reshape('میزان فروش کالاها')))
            plt.xlabel(get_display(reshape('کالا')))
            plt.ylabel(get_display(reshape('مقدار')))
        else:
            plt.title('Products sell count')
            plt.xlabel('Product')
            plt.ylabel('Count')
        plt.show()
        db.close()
    except IndexError:
        pass

def buffet_log_as_chart():
        db = sqlite3.connect(DATABASE_PATH)
        today = d.today()
        dates = [str(today)]
        for i in range(1,7):
            dates.append(str(today-timedelta(i)))
        dates.reverse()
        buys = {}
        charges = {}
        for date in dates:
            cursor_buy  = db.execute('SELECT price From logs WHERE DATE(date)=? AND operation=?', (date,'buy'))
            cursor_charge = db.execute('SELECT price From logs WHERE DATE(date)=? AND operation=?', (date,'charge'))
            buys[str(date)] = cursor_buy.fetchall()
            charges[str(date)] = cursor_charge.fetchall()
        for date in buys.keys():
            buy_operations = buys[date]
            buy_price = 0
            for operation in buy_operations:
                price = operation[0]
                buy_price += price
            buys[date] = buy_price
        for date in charges.keys():
            charge_operations = charges[date]
            charge_price = 0
            for operation in charge_operations:
                price = operation[0]
                charge_price += price
            charges[date] = charge_price
        buy_keys = buys.keys()
        buy_values = buys.values()
        charge_keys = charges.keys()
        charge_values = charges.values()
        plt.figure(figsize=(len(buy_keys)*1.2, 6))
        with open(LANGUAGE_PATH, 'r') as file:
            lang = file.read()
        if lang == 'per':
            plt.xlabel(get_display(reshape("تاریخ")))
            plt.ylabel(get_display(reshape("مبلغ")))
            plt.title(get_display(reshape("تاریخچه بوفه")))
            plt.plot(buy_keys, buy_values, label='خرید')
            plt.plot(charge_keys, charge_values, label='شارژ')
        else:
            plt.xlabel(get_display(reshape("Date")))
            plt.ylabel(get_display(reshape("Price")))
            plt.title(get_display(reshape("Buffet history")))
            plt.plot(buy_keys, buy_values, label='Buy')
            plt.plot(charge_keys, charge_values, label='Charge')
        plt.show()
        db.close()
