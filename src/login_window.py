# وارد کردن ماژول‌های مورد نیاز
from tkinter import ttk  # وارد کردن ماژول ttk از کتابخانه tkinter
import tkinter as tk  # وارد کردن کتابخانه tkinter به عنوان tk
import sys  # وارد کردن ماژول sys برای دسترسی به متغیرهای سیستمی
import hashlib  # وارد کردن ماژول hashlib برای هش کردن رمز عبور
import os  # وارد کردن ماژول os برای ارتباط با سیستم عامل

BASEDIR: str = os.path.dirname(os.path.abspath(__file__))  # تعیین مسیر پایه برنامه
orm_path = BASEDIR  # انتساب مسیر پایه به متغیر orm_path
email_path = BASEDIR  # انتساب مسیر پایه به متغیر email_path
orm_path: str = orm_path.replace("\src", "\db")  # جایگزینی قسمت src با db در مسیر orm_path
email_path: str = email_path.replace("\src", "\\utils")  # جایگزینی قسمت src با utils در مسیر email_path

# اضافه کردن مسیر ماژول ORM به sys.path
sys.path.append(orm_path)  # اضافه کردن مسیر orm_path به sys.path
sys.path.append(email_path)  # اضافه کردن مسیر email_path به sys.path
print(email_path)  # چاپ مسیر email_path برای اطمینان از صحت آن

# وارد کردن کلاس ORM از ماژول ORM
from orm import ORM  # وارد کردن کلاس ORM از ماژول ORM
from time import sleep  # وارد کردن تابع sleep از ماژول time

from email_sender import EmailSender  # وارد کردن کلاس EmailSender از ماژول email_sender
from email_message import EmailNotification  # وارد کردن کلاس EmailNotification از ماژول email_message


# تعریف تابع برای تغییر قابلیت مشاهده یا عدم مشاهده رمز عبور
def toggle_password_visibility():
    if password_entry.cget("show") == "":
        password_entry.config(show="*")
        toggle_password_button.config(text="نمایش رمز")
    else:
        password_entry.config(show="")
        toggle_password_button.config(text="پنهان کردن رمز")


def hash_password(password):
    # هش کردن رمز عبور با الگوریتم SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password


# تعریف تابع برای ورود به سیستم
def login():
    # دریافت نام کاربری و رمز عبور از ورودی‌ها
    username: str = username_entry.get()
    password: str = password_entry.get()

    # بررسی صحت نام کاربری و رمز عبور با استفاده از کلاس ORM
    result: tuple = ORM.login(username, hash_password(password))

    flag = bool(int(result[0]))

    # اگر نتیجه برابر True بود
    if flag == True:

        email = result[1]
        username = result[2]
        first_name = result[3]
        last_name = result[4]

        email_sender = EmailSender()
        email_sender.connect_email()

        email_sender.send_mail(receiver=email, subject="ورود به همراه بانک",
                               html_body=EmailNotification.login_message())
        email_sender.close_connection()
        print("OK")
        sleep(5)
        root.destroy()  # بستن پنجره
        # اینجا کدهای مربوط به ورود کاربر به برنامه را قرار دهید
    else:
        # در غیر اینصورت، نمایش پیام خطا به کاربر
        error_label.config(text=".نام کاربری یا رمز عبور اشتباه است")


# تعریف و تنظیمات اولیه پنجره اصلی
root = tk.Tk()
root.title("صفحه لاگین")
root.configure(bg="#F0F0F0")  # تنظیم رنگ پس زمینه
root.geometry("420x140")  # تنظیم اندازه پنجره
root.resizable(False, False)  # غیر قابل تغییر اندازه کردن پنجره

# تعریف ویجت‌های صفحه لاگین
username_label = ttk.Label(root, text="نام کاربری :", background="#f0f0f0", foreground="black", font=("Arial", 12))
username_entry = ttk.Entry(root, font=("Arial", 12))
password_label = ttk.Label(root, text="رمز عبور :", background="#f0f0f0", foreground="black", font=("Arial", 12))
password_entry = ttk.Entry(root, show="*", font=("Arial", 12))
toggle_password_button = ttk.Button(root, text="پنهان کردن رمز", command=toggle_password_visibility, cursor="hand2",
                                    style="TButton")  # تغییر اندازه فونت و دکمه‌ها
login_button = ttk.Button(root, text="ورود", command=login, style="TButton", cursor="hand2",
                          width=20)  # تغییر اندازه دکمه‌ها و متن
error_label = ttk.Label(root, text="", background="#f0f0f0", foreground="red")  # تغییر رنگ متن

# تنظیم استایل دکمه‌ها
style = ttk.Style()
style.configure("TButton", font=("Arial", 12))  # تغییر اندازه فونت

# قرار دادن ویجت‌ها در صفحه
username_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
username_entry.grid(row=0, column=1, padx=10, pady=5)
password_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
password_entry.grid(row=1, column=1, padx=10, pady=5)
toggle_password_button.grid(row=1, column=2, padx=5, pady=5)
login_button.grid(row=2, column=0, columnspan=3, pady=10)
error_label.grid(row=3, column=0, columnspan=3)

root.mainloop()  # شروع حلقه اصلی برنامه
