from b_email_handler import send_code_for_verification, notice_for_login_with_account
import sqlite3
from important_variables import DATABASE_PATH


def is_first() -> bool:
    '''Checks this is first user.'''
    db = sqlite3.connect(DATABASE_PATH)
    cursor = db.execute('SELECT COUNT(*) FROM users')
    is_empty = not bool(cursor.fetchone()[0])
    db.close()
    return is_empty

def name_is_new(name:str) -> bool:
    '''Checks user name is unique.'''
    db = sqlite3.connect(DATABASE_PATH)
    if is_first():
        return True
    cursor = db.execute('SELECT name FROM users')
    names = cursor.fetchall()
    names_ = [n[0] for n in names]
    db.close()
    if name in names_:
        return False
    else:
        return True
    
def email_is_new(email:str) -> bool:
    '''Checks user email is unique.'''
    db = sqlite3.connect(DATABASE_PATH)
    email = email.lower()
    cursor = db.execute('SELECT email FROM users')
    emails = cursor.fetchall()
    emails_ = [e[0] for e in emails]
    db.close()
    if email in emails_:
        return False
    else:
        return True
    
def register_user(username: str, password: str, email: str) -> bool:
    '''Inserts a new user information in database.'''
    if name_is_new(username):
        db = sqlite3.connect(DATABASE_PATH)
        it_is_first = is_first()
        if it_is_first == True:
            type = 'creator' 
        else:
            type= 'normal'
        db.execute('INSERT INTO users (name, password, email, type, is_current) VALUES (?,?,?,?,?)', (username, password, email, type, 'False'))
        db.commit()
        db.close()
        return True
    else:
        return False
    
def enter_user(username: str, password: str) -> bool | str:
    '''Changes current user info.'''
    try:
        db = sqlite3.connect(DATABASE_PATH)
        cursor = db.execute('SELECT * FROM users WHERE name=?', (username,))
        data = list(cursor.fetchone())
        if password == data[1]:
            email_sended = notice_for_login_with_account(email=data[2])
            if not email_sended:
                return 'internet'
            db.execute('UPDATE users SET is_current=? WHERE is_current=?', ('False', 'True'))
            db.execute('UPDATE users SET is_current=? WHERE name=?', ('True', username,))
            db.commit()
            db.close()
            return True
        else:
            db.close()
            return 'password'
    except:
        return 'name'
    
def user_type(name:str) -> str:
    '''Returns user type.'''
    db = sqlite3.connect(DATABASE_PATH)
    cursor = db.execute('SELECT type FROM users WHERE name=?', (name,))
    t = str(cursor.fetchone()[0])
    db.close()
    return t

def current_user_name() -> str:
    '''Returns current user name.'''
    db = sqlite3.connect(DATABASE_PATH)
    cursor = db.execute('SELECT name FROM users WHERE is_current=?', ('True',))
    name = str(cursor.fetchone()[0])
    db.close()
    return name
    
def change_user_type(name:str):
    '''Changes user type.'''
    db = sqlite3.connect(DATABASE_PATH)
    cursor = db.execute('SELECT type FROM users WHERE name=?', (name,))
    old_type = str(cursor.fetchone()[0])
    if old_type=='normal':
        db.execute('UPDATE users SET type=? WHERE name=?', ('admin', name))
    else:
        db.execute('UPDATE users SET type=? WHERE name=?', ('normal', name))
    db.commit()
    db.close()

def all_users() -> list:
    '''Returns a list of all users, except Creator.'''
    db = sqlite3.connect(DATABASE_PATH)
    cursor = db.execute('SELECT name FROM users')
    data = cursor.fetchall()
    users = [user[0] for user in data]
    db.close()
    return users[1:]

def forget_password(name:str) -> int | str:
    '''When user forgot his password, we use this method for get email and send the code.'''
    try:
        db = sqlite3.connect(DATABASE_PATH)
        cursor = db.execute('SELECT email FROM users WHERE name=?', (name,))
        email = cursor.fetchone()[0]
        code = send_code_for_verification(email)
        db.close()
        return code
    except:
        return 'name'

def change_name(old_name:str, new_name:str) -> None:
    '''Changes user name.'''
    db = sqlite3.connect(DATABASE_PATH)
    db.execute('UPDATE users SET name=? WHERE name=?', (new_name, old_name))
    db.commit()
    db.close()

def change_password(new_password:str, name:str=None) -> None:
    '''Changes user password.'''
    if name:
        db = sqlite3.connect(DATABASE_PATH)
        db.execute('UPDATE users SET password=? WHERE name=?', (new_password, name))
        db.commit()
        db.close()