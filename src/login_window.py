# وارد کردن ماژول‌های مورد نیاز
from tkinter import ttk, messagebox
import tkinter as tk
import sys

# اضافه کردن مسیر ماژول ORM به sys.path
sys.path.append('H:\Term-5\DB\Project\DB-Project\db')

# وارد کردن کلاس ORM از ماژول ORM
from orm import ORM
from time import sleep

# تعریف تابع برای تغییر قابلیت مشاهده یا عدم مشاهده رمز عبور
def toggle_password_visibility():
    if password_entry.cget("show") == "":
        password_entry.config(show="*")
        toggle_password_button.config(text="نمایش رمز")
    else:
        password_entry.config(show="")
        toggle_password_button.config(text="پنهان کردن رمز")

# تعریف تابع برای ورود به سیستم
def login():
    # دریافت نام کاربری و رمز عبور از ورودی‌ها
    username = username_entry.get()
    password = password_entry.get()

    # بررسی صحت نام کاربری و رمز عبور با استفاده از کلاس ORM
    result: bool = ORM.login(username, password)
    print(f"{result=}")

    # اگر نتیجه برابر True بود
    if result == True:
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
root.configure(bg="#f0f0f0")  # تنظیم رنگ پس زمینه
root.geometry("420x140")  # تنظیم اندازه پنجره
root.resizable(False, False)  # غیر قابل تغییر اندازه کردن پنجره

# تعریف ویجت‌های صفحه لاگین
username_label = ttk.Label(root, text="نام کاربری :", background="#f0f0f0", foreground="black", font=("Arial", 12))
username_entry = ttk.Entry(root, font=("Arial", 12))
password_label = ttk.Label(root, text="رمز عبور :", background="#f0f0f0", foreground="black", font=("Arial", 12))
password_entry = ttk.Entry(root, show="*", font=("Arial", 12))
toggle_password_button = ttk.Button(root, text="پنهان کردن رمز", command=toggle_password_visibility, cursor="hand2", style="TButton")  # تغییر اندازه فونت و دکمه‌ها
login_button = ttk.Button(root, text="ورود", command=login, style="TButton", cursor="hand2", width=20)  # تغییر اندازه دکمه‌ها و متن
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
