from .module import *
from .main_window import MainWindow


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
    username: str = username_entry.get()
    password: str = password_entry.get()

    # بررسی صحت نام کاربری و رمز عبور با استفاده از کلاس ORM
    result: tuple = ORM.login(username, hash_password(password))

    flag = bool(int(result[0]))

    # اگر نتیجه برابر True بود
    if flag == True:

        id = result[1]
        email = result[2]
        username = result[3]
        first_name = result[4]
        last_name = result[5]
        try:
            email_thread = threading.Thread(target=send_email, args=[email, "ورود به همراه بانک"])
            email_thread.start()
            root.destroy()  # بستن پنجره
            MainWindow(int(id), email, username, first_name, last_name)

        except Exception as e:
            messagebox.showerror("خطا", "ارتباط با برنامه با مشکل مواجه شد.")
            root.destroy()  # بستن پنجره در صورت خطا

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
