from tkinter import ttk  # وارد کردن ماژول ttk از کتابخانه tkinter
import tkinter as tk  # وارد کردن کتابخانه tkinter به عنوان tk

class LoansTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_loans_table()

    def create_loans_table(self):
        loans_label = ttk.Label(self, text="لیست وام‌ها")
        loans_label.pack()

        self.loans_tree = ttk.Treeview(self, columns=('ردیف', "شماره حساب", "مبلغ وام", "تاریخ شروع"),
                                       selectmode="browse")
        self.loans_tree.pack(fill=tk.BOTH, expand=True)

        self.loans_tree.heading("#0", text="شماره ردیف", anchor="center")
        self.loans_tree.column("#0", anchor='center')

        self.loans_tree.heading("#1", text="شماره حساب", anchor="center")
        self.loans_tree.column("#1", anchor='center')

        self.loans_tree.heading("#2", text="مبلغ وام", anchor="center")
        self.loans_tree.column("#2", anchor='center')

        self.loans_tree.heading("#3", text="تاریخ شروع", anchor="center")
        self.loans_tree.column("#3", anchor='center')

        for i in range(15):
            self.loans_tree.insert("", tk.END, text=str(i), values=("1234567890", "$5000", "2024-01-01"),
                                   tags=('center',))

        self.loans_tree.tag_configure('center', anchor='center')

        self.loans_tree.bind("<<TreeviewSelect>>", self.on_loan_selected)
        self.loans_tree.bind("<FocusOut>", lambda event: self.loans_tree.selection_remove(self.loans_tree.selection()))

    def on_loan_selected(self, event):
        selected_items = self.loans_tree.selection()
        if selected_items:
            selected_item = selected_items[0]
            loan_info = self.loans_tree.item(selected_item, "values")
            print("Selected Loan:", loan_info)


class AccountsTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_accounts_table()

    def create_accounts_table(self):
        accounts_label = ttk.Label(self, text="لیست حساب‌های بانکی")
        accounts_label.pack()

        self.accounts_tree = ttk.Treeview(self, columns=("شماره ردیف", "نام", "شماره حساب", "موجودی"),
                                          selectmode="browse")
        self.accounts_tree.pack(fill=tk.BOTH, expand=True)

        self.accounts_tree.heading("#0", text="شماره ردیف", anchor="center")
        self.accounts_tree.column("#0", anchor='center')

        self.accounts_tree.heading("#1", text="نام", anchor="center")
        self.accounts_tree.column("#1", anchor='center')

        self.accounts_tree.heading("#2", text="شماره حساب", anchor="center")
        self.accounts_tree.column("#2", anchor='center')

        self.accounts_tree.heading("#3", text="موجودی", anchor="center")
        self.accounts_tree.column("#3", anchor='center')

        for i in range(10):
            self.accounts_tree.insert("", tk.END, text=str(i), values=("حساب " + str(i + 1), "1234567890", "$1000"),
                                      tags=('center',))

        self.accounts_tree.tag_configure('center', anchor='center')

        self.accounts_tree.bind("<<TreeviewSelect>>", self.on_account_selected)
        self.accounts_tree.bind("<FocusOut>",
                                lambda event: self.accounts_tree.selection_remove(self.accounts_tree.selection()))

    def on_account_selected(self, event):
        selected_items = self.accounts_tree.selection()
        if selected_items:
            selected_item = selected_items[0]
            account_info = self.accounts_tree.item(selected_item, "values")
            print("Selected Bank Account:", account_info)


class SettingsTab(ttk.Frame):
    def __init__(self, parent, id: int, email: str, username: str, first_name: str, last_name: str):
        super().__init__(parent)
        self.id = id
        self.email = email
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

        self.create_user_info_section()
        self.create_change_password_section()

    def create_user_info_section(self):
        user_info_frame = ttk.Frame(self)
        user_info_frame.pack(fill=tk.BOTH, expand=True)

        user_id = self.id
        first_name = self.first_name
        last_name = self.last_name
        username = self.username
        email = self.email

        name_label = ttk.Label(user_info_frame, text=f"نام: {first_name}")
        name_label.pack()

        last_name_label = ttk.Label(user_info_frame, text=f"نام خانوادگی: {last_name}")
        last_name_label.pack()

        username_label = ttk.Label(user_info_frame, text=f"یوزر نیم: {username}")
        username_label.pack()

        email_label = ttk.Label(user_info_frame, text=f"ایمیل: {email}")
        email_label.pack()

    def create_change_password_section(self):
        change_password_frame = ttk.Frame(self)
        change_password_frame.pack(fill=tk.BOTH, expand=True)

        old_password_label = ttk.Label(change_password_frame, text="پسورد فعلی:")
        old_password_label.pack()

        self.old_password_entry = ttk.Entry(change_password_frame, show="*")
        self.old_password_entry.pack()

        new_password_label = ttk.Label(change_password_frame, text="پسورد جدید:")
        new_password_label.pack()

        self.new_password_entry = ttk.Entry(change_password_frame, show="*")
        self.new_password_entry.pack()

        self.show_password_var = tk.BooleanVar()
        show_password_checkbutton = ttk.Checkbutton(change_password_frame, text="نمایش پسورد",
                                                    variable=self.show_password_var,
                                                    command=self.toggle_show_password)
        show_password_checkbutton.pack()

        change_button = ttk.Button(change_password_frame, text="تغییر پسورد", command=self.change_password)
        change_button.pack()

    def toggle_show_password(self):
        if self.show_password_var.get():
            self.old_password_entry.config(show="")
            self.new_password_entry.config(show="")
        else:
            self.old_password_entry.config(show="*")
            self.new_password_entry.config(show="*")

    def change_password(self):
        old_password = self.old_password_entry.get()
        new_password = self.new_password_entry.get()
        # بررسی صحت پسوردها و اعمال تغییرات بر روی پسورد

        print("پسورد با موفقیت تغییر یافت.")


class MenuBar(tk.Menu):
    def __init__(self, master):
        super().__init__(master)

        # ایجاد منوی "فایل"
        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label="خروج", command=master.quit)

        # ایجاد منوی "تنظیمات"
        settings_menu = tk.Menu(self, tearoff=0)
        settings_menu.add_command(label="رفرش")

        # اضافه کردن منوها به منوبار
        self.add_cascade(label="فایل", menu=file_menu)
        self.add_cascade(label="آپدیت اطلاعات", menu=settings_menu)


class MainWindow:
    def __init__(self, id: int, email: str, username: str, first_name: str, last_name: str):
        self.root = tk.Tk()
        self.root.title("Bank Details")
        self.root.geometry("800x600")
        # self.id = id
        # self.email = email
        # self.username = username
        # self.first_name = first_name
        # self.last_name = last_name

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.loans_tab = LoansTab(self.notebook)
        self.notebook.add(self.loans_tab, text="وام‌ها")

        self.accounts_tab = AccountsTab(self.notebook)
        self.notebook.add(self.accounts_tab, text="حساب‌های بانکی")

        self.settings_tab = SettingsTab(self.notebook, id, email, username, first_name, last_name)
        self.notebook.add(self.settings_tab, text="تنظیمات")

        self.menu_bar = MenuBar(self.root)
        self.root.config(menu=self.menu_bar)

        self.root.mainloop()

# app = MainWindow()
