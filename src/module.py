# وارد کردن ماژول‌های مورد نیاز
from tkinter import ttk  # وارد کردن ماژول ttk از کتابخانه tkinter
import tkinter as tk  # وارد کردن کتابخانه tkinter به عنوان tk
import sys  # وارد کردن ماژول sys برای دسترسی به متغیرهای سیستمی
import hashlib  # وارد کردن ماژول hashlib برای هش کردن رمز عبور
import os  # وارد کردن ماژول os برای ارتباط با سیستم عامل
from tkinter import messagebox

BASEDIR: str = os.path.dirname(os.path.abspath(__file__))  # تعیین مسیر پایه برنامه
orm_path = BASEDIR  # انتساب مسیر پایه به متغیر orm_path
email_path = BASEDIR  # انتساب مسیر پایه به متغیر email_path
orm_path: str = orm_path.replace("\src", "\db")  # جایگزینی قسمت src با db در مسیر orm_path
email_path: str = email_path.replace("\src", "\\utils")  # جایگزینی قسمت src با utils در مسیر email_path

# اضافه کردن مسیر ماژول ORM به sys.path
sys.path.append(orm_path)  # اضافه کردن مسیر orm_path به sys.path
sys.path.append(email_path)  # اضافه کردن مسیر email_path به sys.path
# print(email_path)  # چاپ مسیر email_path برای اطمینان از صحت آن

# وارد کردن کلاس ORM از ماژول ORM
from orm import ORM  # وارد کردن کلاس ORM از ماژول ORM
from time import sleep  # وارد کردن تابع sleep از ماژول time

from email_sender import EmailSender  # وارد کردن کلاس EmailSender از ماژول email_sender
from email_message import EmailNotification  # وارد کردن کلاس EmailNotification از ماژول email_message
from khayyam import JalaliDatetime
import re
from tkcalendar import DateEntry  # نیاز به نصب کتابخانه tkcalendar دارید
import jdatetime
from datetime import datetime, timedelta
import threading

def hash_password(password):
    # هش کردن رمز عبور با الگوریتم SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password


def send_email_login(email, subject):
    try:
        email_sender = EmailSender()
        email_sender.connect_email()
        email_sender.send_mail(receiver=email, subject=subject,
                               html_body=EmailNotification.login_message())
        email_sender.close_connection()
    except Exception as e:
        print("Error sending email:", e)


def send_email_deposite(email, deposite_amount, account_number):
    try:
        amount = ORM.get_amount_account(account_number)

        email_sender = EmailSender()
        email_sender.connect_email()
        email_sender.send_mail(receiver=email, subject="واریز",
                               html_body=EmailNotification.deposite(amount, str(deposite_amount),
                                                                    account_number))
        email_sender.close_connection()
    except Exception as e:
        print("Error sending email:", e)


def send_email_withdraw(email, transfer_amount, account_number):
    try:

        amount = ORM.get_amount_account(account_number)

        email_sender = EmailSender()
        email_sender.connect_email()

        email_sender.send_mail(receiver=email, subject="برداشت",
                               html_body=EmailNotification.withdraw(amount, transfer_amount,
                                                                    account_number))
        email_sender.close_connection()
    except Exception as e:
        print("Error sending email:", e)


def secondary_password(email, password):
    try:

        email_sender = EmailSender()
        email_sender.connect_email()

        email_sender.send_mail(receiver=email, subject="رمز دوم",
                               html_body=EmailNotification.secondary_password(password))
        email_sender.close_connection()
    except Exception as e:
        print("Error sending email:", e)