import sqlite3
from important_variables import DATABASE_PATH


def save_school(school_name:str) -> None:
    '''Insert a school in database.'''
    db = sqlite3.connect(DATABASE_PATH)
    db.execute('INSERT INTO schools_classes (school,classes) VALUES (?,?)', (school_name, '[]'))
    db.commit()
    db.close()

def save_class(school_name:str, class_name:str) -> None:
    '''Insert a class in database.'''
    db = sqlite3.connect(DATABASE_PATH)
    cursor = db.execute('SELECT classes FROM schools_classes WHERE school=?', (school_name,))
    classes = eval(cursor.fetchone()[0])
    classes.append(class_name)
    db.execute('UPDATE schools_classes SET classes=? WHERE school=?', (f'{classes}', school_name))
    db.commit()
    db.close()

def read_schools() -> list:
    '''Reads all schools from database.'''
    db = sqlite3.connect(DATABASE_PATH)
    cursor = db.execute('SELECT school FROM schools_classes')
    data = cursor.fetchall()
    schools = [school[0] for school in data]
    db.close()
    return schools

def read_classes(school_name:str) -> list:
    '''Reads all classes of a school from database.'''
    db = sqlite3.connect(DATABASE_PATH)
    cursor = db.execute('SELECT classes FROM schools_classes WHERE school=?', (school_name,))
    classes = eval(cursor.fetchone()[0])
    db.close()
    return classes

def delete_school(school_name:str) -> None:
    '''Deletes a school and all of it classes from database.'''
    db = sqlite3.connect(DATABASE_PATH)
    db.execute('DELETE FROM schools_classes WHERE school=?', (school_name,))
    db.commit()
    db.close()

def delete_class(school_name:str, class_name:str) -> None:
    '''Deletes a class from database.'''
    db = sqlite3.connect(DATABASE_PATH)
    cursor = db.execute('SELECT classes FROM schools_classes WHERE school=?', (school_name,))
    classes = eval(cursor.fetchone()[0])
    classes.remove(class_name)
    db.execute('UPDATE schools_classes SET classes=? WHERE school=?', (f'{classes}', school_name))
    db.commit()
    db.close()