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

def hash_password(password):
    # هش کردن رمز عبور با الگوریتم SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password


