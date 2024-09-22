from datetime import datetime, date as d
import sqlite3
from important_variables import DATABASE_PATH
from b_manage_users import current_user_name


def save_log(name: str, operation: str, price: str, products: str) -> None:
    '''Save log in the database.'''
    db = sqlite3.connect(DATABASE_PATH)
    date_as_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date = datetime.strptime(date_as_str, '%Y-%m-%d %H:%M:%S')
    user_name = current_user_name()
    db.execute('INSERT INTO logs (name,operation,price,date,products,user_name) VALUES (?,?,?,?,?,?)', (name, operation, price, date, products, user_name))
    db.commit()
    db.close()

def read_logs(by, name=None, start_date=None, end_date=None, start_price=None, end_price=None, operation=None, logs=None) -> list:
    '''Read logs from the database.'''
    db = sqlite3.connect(DATABASE_PATH)
    if logs:
        logs.reverse()
        all_logs_as_lst = list(logs)
    else:
        cursor = db.execute('SELECT * FROM logs')
        data = cursor.fetchall()
        all_logs_as_lst = [list(log) for log in data]

    if by == 'all':
        all_logs_as_lst.reverse()
        return all_logs_as_lst

    if by == 'operation':
        special_logs = []
        for log in all_logs_as_lst:
            log_operation = log[1]
            if log_operation == operation:
                special_logs.append(log)
            else:
                pass
        special_logs.reverse()
        return special_logs

    if by == 'date':
        if start_date == end_date:
            return False
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        special_logs = []
        for log in all_logs_as_lst:
            log_time = log[3]
            log_date = datetime.strptime(log_time.split(' ')[0], '%Y-%m-%d')
            if (log_date > start and log_date < end) or log_date == start:
                special_logs.append(log)
        special_logs.reverse()
        return special_logs

    if by == 'price':
        special_logs = []
        for log in all_logs_as_lst:
            log_price = log[2]
            if int(start_price) <= int(log_price) and int(log_price) <= int(end_price):
                special_logs.append(log)
            else:
                pass
        special_logs.reverse()
        return special_logs
    
    if by == 'name':
        special_logs = []
        for log in all_logs_as_lst:
            log_name = log[0]
            if log_name == name:
                special_logs.append(log)
            else:
                pass
        special_logs.reverse()
        return special_logs

    db.close()

def delete_log(logs_to_delete: list) -> None:
    '''delete logs from database.'''
    db = sqlite3.connect(DATABASE_PATH)
    for log in logs_to_delete:
        db.execute('DELETE FROM logs WHERE name=? AND operation=? AND price=? AND date=? AND products=?', (log[0], log[1], log[2], log[3], log[4]))
    db.commit()

def change_log_name(old_name:str, new_name:str) -> None:
    '''Change log buyer name when it changed from buyer settings.'''
    db = sqlite3.connect(DATABASE_PATH)
    db.execute('UPDATE logs SET name=? WHERE name=?', (new_name, old_name))
    db.commit()
    db.close()