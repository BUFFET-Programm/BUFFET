import random
from email.message import EmailMessage
import smtplib
from datetime import datetime
from important_variables import LANGUAGE_PATH, DATABASE_PATH
import sqlite3

sender = "buffetprogramm@gmail.com"
password = "aqkc qqxo iaiz jznt"

def send_code_for_verification(email:str) -> int | bool:
    '''Send a code to the email that given to it. returns the code that sent when operation was successful.'''
    try:
        code = random.randint(100000, 999999)
        with open(LANGUAGE_PATH, 'r') as file:
            lang = file.read()
        if lang=='per':
            path = 'html_pages/send_code_for_verification_per.html'
            subject = "کد اعتبارسنجی برنامه بوفه"
        else:
            path = 'html_pages/send_code_for_verification_eng.html'
            subject = "BUFFET verification code"
        with open(path, encoding='UTF-8') as file:
            content = file.read()
        modified_content = content.replace('{}', str(code))
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = email
        msg.set_content(modified_content, subtype="html")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, email, msg.as_string())
        return code
    except:
        return False

def notice_for_login_with_account(email:str) -> bool:
    '''Send a notification to the user email when we recognize someone entered to his account.'''
    try:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LANGUAGE_PATH, 'r') as file:
            lang = file.read()
        if lang=='per':
            path = 'html_pages/notice_for_login_with_account_per.html'
            subject = "اعلان ورود به برنامه بوفه"
        else:
            path = 'html_pages/notice_for_login_with_account_eng.html'
            subject = "BUFFET login notification"
        with open(path, encoding='UTF-8') as file:
            content = file.read()
        modified_content = content.replace('{}', str(date))
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = email
        msg.set_content(modified_content, subtype="html")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, email, msg.as_string())
        return True
    except:
        return False
    
def notify_creator_about_new_user(username:str, email:str) -> bool:
    '''Send a notification to the creator email when we recognize someone registered in BUFFET.'''
    try:
        db = sqlite3.connect(DATABASE_PATH)
        cursor = db.execute('SELECT email FROM users WHERE type=?', ('creator',))
        creator_email = cursor.fetchone()[0]
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LANGUAGE_PATH, 'r') as file:
            lang = file.read()
        if lang=='per':
            path = 'html_pages/notify_creator_about_new_user_per.html'
            subject = "اعلان ثبت نام در برنامه بوفه"
        else:
            path = 'html_pages/notify_creator_about_new_user_eng.html'
            subject = "BUFFET user registration notification"
        with open(path, encoding='UTF-8') as file:
            content = file.read()
        modified_content = content.replace('{1}', str(date))
        modified_content = modified_content.replace('{2}', str(username))
        modified_content = modified_content.replace('{3}', str(email))
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = creator_email
        msg.set_content(modified_content, subtype="html")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, creator_email, msg.as_string())
        return True
    except:
        return False
    
def welcome_new_user(name:str, email:str) -> bool:
    '''Say welcome to the new user.'''
    try:
        with open(LANGUAGE_PATH, 'r') as file:
            lang = file.read()
        if lang=='per':
            path = 'html_pages/say_welcome_to_new_user_per.html'
            subject = "به بوفه خوش آمدید!"
        else:
            path = 'html_pages/say_welcome_to_new_user_eng.html'
            subject = "Welcome to the BUFFET app!"
        with open(path, encoding='UTF-8') as file:
            content = file.read()
        modified_content = content.replace('{}', str(name))
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = email
        msg.set_content(modified_content, subtype="html")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, email, msg.as_string())
        return True
    except:
        return False