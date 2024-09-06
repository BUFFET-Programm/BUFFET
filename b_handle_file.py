from important_variables import BASE_DIR, BUFFET_EXTENSIONS_PATH, THEME_PATH, DATABASE_PATH, ALGORITHM_PATH, LANGUAGE_PATH
from os import mkdir, listdir
from urllib.request import urlretrieve
from shutil import rmtree
import sqlite3
from os.path import exists


def create_files_and_folders() -> None:
    '''Creates required files and folders.'''
    try:
        try:
            mkdir(BASE_DIR)
        except FileExistsError:
            pass
        mkdir(BASE_DIR+'/data')
        mkdir(BASE_DIR+"/data/text")
        mkdir(BASE_DIR+"/data/trainer")
        if not exists(THEME_PATH):
            with open(THEME_PATH, "w") as file:
                file.write("Light,Blue,False")
        if not exists(LANGUAGE_PATH):
            with open(LANGUAGE_PATH, "w") as file:
                file.write("eng")
        db = sqlite3.connect(DATABASE_PATH)
        try:
            db.execute('CREATE TABLE buyers (name text, id int, school text, class text, charge int)')
        except:
            pass
        try:
            db.execute('CREATE TABLE users (name text, password text, email text, type text, is_current text)')
        except:
            pass
        try:
            db.execute('CREATE TABLE logs (name text, operation text, price int, date datetime, products text)')
        except:
            pass
        try:
            db.execute('CREATE TABLE schools_classes (school text, classes text)')
        except:
            pass
        try:
            db.execute('CREATE TABLE products (name text, code int, price int, count int)')
        except:
            pass
        try:
            mkdir(BUFFET_EXTENSIONS_PATH)
        except FileExistsError:
            pass
    except FileExistsError:
        pass

def download_files() -> bool:
    '''Downloads extensions from internet. returns False when internet error.'''
    files = set(listdir(BUFFET_EXTENSIONS_PATH))
    if not files == {'haarcascade_frontalface_alt.xml', 'iransans.ttf', 'icon.ico'}:
        try:
            rmtree(BUFFET_EXTENSIONS_PATH)
            mkdir(BUFFET_EXTENSIONS_PATH)
            urlretrieve('https://github.com/BUFFET-Programm/Extensions-Of-Buffet-Project/raw/main/haarcascade_frontalface_alt.xml',
                        ALGORITHM_PATH)
            urlretrieve('https://github.com/BUFFET-Programm/Extensions-Of-Buffet-Project/raw/main/iransans.ttf',
                        BUFFET_EXTENSIONS_PATH+'/iransans.ttf')
            urlretrieve('https://github.com/BUFFET-Programm/Extensions-Of-Buffet-Project/raw/main/icon.ico',
                        BUFFET_EXTENSIONS_PATH+'/icon.ico')
        except:
            return False
    else:
        pass
    return True

def delete_all_data() -> None:
    """Deletes all data."""
    try:
        rmtree(BASE_DIR+'/data')
        create_files_and_folders()
    except FileNotFoundError:
        pass
