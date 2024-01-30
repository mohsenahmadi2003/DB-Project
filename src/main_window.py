from module import *


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


import tkinter as tk
from tkinter import ttk


class AccountsTab(ttk.Frame):
    def __init__(self, parent, id):
        super().__init__(parent)
        self.accounts: list = ORM.get_bank_accounts(id)
        self.create_layout()

    def create_layout(self):
        # ایجاد فریم برای نمایش لیست حساب‌های بانکی
        accounts_frame = ttk.Frame(self)
        accounts_frame.pack(fill=tk.BOTH, expand=True)

        accounts_label = ttk.Label(accounts_frame, text="لیست حساب‌های بانکی")
        accounts_label.pack()

        self.accounts_tree = ttk.Treeview(accounts_frame, columns=("شماره ردیف", "شماره حساب", "موجودی", "وضعیت حساب"),
                                          selectmode="browse")
        self.accounts_tree.pack(fill=tk.BOTH, expand=True)

        self.accounts_tree.heading("#0", text="شماره ردیف", anchor="center")
        self.accounts_tree.column("#0", anchor='center')

        self.accounts_tree.heading("#1", text="شماره حساب", anchor="center")
        self.accounts_tree.column("#1", anchor='center')

        self.accounts_tree.heading("#2", text="موجودی", anchor="center")
        self.accounts_tree.column("#2", anchor='center')

        self.accounts_tree.heading("#3", text="وضعیت حساب", anchor="center")
        self.accounts_tree.column("#3", anchor='center')

        for index, item in enumerate(self.accounts):
            self.accounts_tree.insert("", tk.END, text=str(index), values=(f"{item[2]}", f"{item[4]}", f"{item[8]}"),
                                      tags=('center',))

        self.accounts_tree.tag_configure('center', anchor='center')

        self.accounts_tree.bind("<<TreeviewSelect>>", self.on_account_selected)
        self.accounts_tree.bind("<FocusOut>",
                                lambda event: self.accounts_tree.selection_remove(self.accounts_tree.selection()))
        # ایجاد فریم برای نمایش لیست حساب‌های بانکی
        selected_account_frame = ttk.Frame(self)
        selected_account_frame.pack(fill=tk.BOTH, expand=True)

        # ایجاد ویجت‌های مربوط به اطلاعات حساب انتخاب شده
        self.selected_account_number_label = ttk.Label(selected_account_frame, text="شماره حساب:")
        self.selected_account_number_label.grid(row=0, column=1)

        self.selected_primary_password_label = ttk.Label(selected_account_frame, text="رمز اول حساب:")
        self.selected_primary_password_label.grid(row=1, column=1)

        self.selected_amount_label = ttk.Label(selected_account_frame, text="موجودی حساب:")
        self.selected_amount_label.grid(row=2, column=1)

        self.selected_rate_label = ttk.Label(selected_account_frame, text="امتیاز حساب:")
        self.selected_rate_label.grid(row=3, column=1)

        self.selected_date_opened_label = ttk.Label(selected_account_frame, text="تاریخ افتتاح حساب:")
        self.selected_date_opened_label.grid(row=4, column=1)

        self.selected_date_closed_label = ttk.Label(selected_account_frame, text="تاریخ بسته شدن حساب:")
        self.selected_date_closed_label.grid(row=5, column=1)

        # ایجاد فریم برای نمایش لیست حساب‌های بانکی
        selected_account_status_description_frame = ttk.Frame(self)
        selected_account_status_description_frame.pack(fill=tk.BOTH, expand=True)

        # ایجاد ویجت‌های مربوط به ویرایش توضیحات و مسدود کردن حساب
        self.selected_description_label = ttk.Label(selected_account_status_description_frame, text="توضیحات حساب:")
        self.selected_description_label.grid(row=6, column=1)

        self.selected_description_entry = ttk.Entry(selected_account_status_description_frame)
        self.selected_description_entry.grid(row=6, column=0)

        self.selected_account_status_var = tk.IntVar()
        self.selected_account_status_checkbutton = ttk.Checkbutton(selected_account_status_description_frame,
                                                                   text="مسدود شدن حساب",
                                                                   variable=self.selected_account_status_var)
        self.selected_account_status_checkbutton.grid(row=7, column=0)

        self.submit_button = ttk.Button(selected_account_status_description_frame, text="ثبت",
                                        command=self.submit_account_changes)
        self.submit_button.grid(row=8, column=0, columnspan=2)

    def submit_account_changes(self):
        description = self.selected_description_entry.get()
        is_account_blocked = self.selected_account_status_var.get()
        account_number = self.selected_account_number_label.cget("text")
        account_number = re.findall(r'\d+', account_number)[0]

        if is_account_blocked == 1:
            result = ORM.block_bank_account(account_number, description)[0]
            if bool(int(result[1])) == True:
                messagebox.showinfo("موفقیت", result[0])
            else:
                messagebox.showinfo("خطا", result[0])

    def on_account_selected(self, event):
        selected_items = self.accounts_tree.selection()
        if selected_items:
            selected_item = selected_items[0]
            account_info = self.accounts_tree.item(selected_item, "values")
            data = list(filter(lambda x: x[2] == str(account_info[0]), self.accounts))[0]
            self.selected_account_number_label.config(text=f"شماره حساب: {data[2]}")
            self.selected_primary_password_label.config(text=f"رمز اول حساب: {data[3]}", anchor='center')
            self.selected_amount_label.config(text=f"موجودی حساب: {data[4]}")
            self.selected_rate_label.config(text=f"امتیاز حساب: {data[5]}")
            self.selected_date_opened_label.config(text=f"تاریخ افتتاح حساب: {data[6]}")
            self.selected_date_closed_label.config(text=f"تاریخ بسته شدن حساب: {data[7]}")
            self.selected_description_entry.delete(0, tk.END)  # پاک کردن محتویات اولیه توضیحات
            self.selected_description_entry.insert(0, data[9])  # وارد کردن توضیحات از دیتابیس
            self.selected_account_status_var.set(data[8])  # تنظیم وضعیت مسدودی حساب


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
        old_password: str = hash_password(self.old_password_entry.get())
        new_password: str = hash_password(self.new_password_entry.get())
        # بررسی صحت پسوردها و اعمال تغییرات بر روی پسورد

        result = ORM.update_password(user_id=int(self.id), new_password=new_password, old_password=old_password)
        if result == False:
            messagebox.showinfo("خطا", "خطا در اتصال به پایگاه داده")
        else:
            print(result)
            msg = str(result[0])
            status = bool(int(result[1]))

            if status == True:
                messagebox.showinfo("موفقیت", msg)
                self.old_password_entry.delete(0, tk.END)
                self.new_password_entry.delete(0, tk.END)
            else:
                messagebox.showinfo("خطا", msg)


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


class TransactionsTab(ttk.Frame):
    def __init__(self, parent, id: int):
        super().__init__(parent)
        self.id = id
        self.create_layout()

    def create_layout(self):
        # ایجاد ویجت‌ها برای فیلتر تراکنش‌ها
        filter_frame = ttk.Frame(self)
        filter_frame.pack(fill="x", expand=False)

        filter_button = ttk.Button(filter_frame, text="اعمال", command=self.apply_filter)
        filter_button.grid(row=0, column=100, padx=5, pady=5)

        # ایجاد ویجت‌های انتخاب نوع فیلتر تراکنش‌ها
        filter_type_label = ttk.Label(filter_frame, text="نوع فیلتر:",
                                      wraplength=100)  # تنظیم wraplength برای افقی شدن متن
        filter_type_label.grid(row=0, column=0, padx=5, pady=5)

        self.filter_type_var = tk.StringVar()
        self.filter_type_var.set("تاریخ")  # تنظیم مقدار پیش‌فرض برای انتخاب
        filter_type_combobox = ttk.Combobox(filter_frame, textvariable=self.filter_type_var,
                                            values=["تاریخ", "تعداد تراکنش"], state="readonly", width=15)
        filter_type_combobox.grid(row=0, column=1, padx=5, pady=5)
        filter_type_combobox.bind("<<ComboboxSelected>>", self.on_filter_type_selected)

        # ایجاد ویجت‌های نمایش لیست تراکنش‌ها
        transactions_frame = ttk.Frame(self)
        transactions_frame.pack(fill="both", expand=True)

        transactions_label = ttk.Label(transactions_frame, text="لیست تراکنش‌ها")
        transactions_label.pack()

        self.transaction_tree = ttk.Treeview(transactions_frame, columns=(
        "شماره ردیف", "شماره حساب مبدا", "شماره حساب مقصد", "مقدار انتقال", 'تاریخ تراکنش', "وضعیت تراکنش",
        'توضیحات تراکنش'), selectmode="browse")
        self.transaction_tree.pack(fill="both", expand=True)

        self.transaction_tree.heading("#0", text="شماره ردیف", anchor="center")
        self.transaction_tree.column("#0", anchor='center')

        self.transaction_tree.heading("#1", text="شماره حساب مبدا", anchor="center")
        self.transaction_tree.column("#1", anchor='center')

        self.transaction_tree.heading("#2", text="شماره حساب مقصد", anchor="center")
        self.transaction_tree.column("#2", anchor='center')

        self.transaction_tree.heading("#3", text="مقدار انتقال", anchor="center")
        self.transaction_tree.column("#3", anchor='center')

        self.transaction_tree.heading("#4", text='تاریخ تراکنش', anchor="center")
        self.transaction_tree.column("#4", anchor='center')

        self.transaction_tree.heading("#5", text="وضعیت تراکنش", anchor="center")
        self.transaction_tree.column("#5", anchor='center')

        self.transaction_tree.heading("#6", text='توضیحات تراکنش', anchor="center")
        self.transaction_tree.column("#6", anchor='center')

        self.transaction_tree.bind("<<TreeviewSelect>>", self.on_transaction_selected)

        # اضافه کردن دو فیلد تاریخ
        self.start_date_label = ttk.Label(filter_frame, text="تاریخ شروع:",
                                          wraplength=80)  # تنظیم wraplength برای افقی شدن متن
        self.start_date_label.grid(row=2, column=0, padx=5, pady=5)
        self.start_date_entry = DateEntry(filter_frame)
        self.start_date_entry.grid(row=2, column=1, padx=5, pady=5)

        self.end_date_label = ttk.Label(filter_frame, text="تاریخ پایان:",
                                        wraplength=80)  # تنظیم wraplength برای افقی شدن متن
        self.end_date_label.grid(row=3, column=0, padx=5, pady=5)
        self.end_date_entry = DateEntry(filter_frame)
        self.end_date_entry.grid(row=3, column=1, padx=5, pady=5)

        # ایجاد ویجت‌های فیلتر تعداد تراکنش
        self.transaction_count_label = ttk.Label(filter_frame, text="تعداد تراکنش:",
                                                 wraplength=80)  # تنظیم wraplength برای افقی شدن متن
        self.transaction_count_label.grid(row=2, column=0, padx=5, pady=5)
        self.transaction_count_entry = ttk.Entry(filter_frame)
        self.transaction_count_entry.grid(row=2, column=1, padx=5, pady=5)
        self.transaction_count_label.grid_remove()
        self.transaction_count_entry.grid_remove()

        # افزودن اسکرولبار به صفحه
        scroll_vertical = ttk.Scrollbar(transactions_frame, orient="vertical", command=self.transaction_tree.yview)
        scroll_vertical.pack(side="right", fill="y")
        self.transaction_tree.configure(yscrollcommand=scroll_vertical.set)

        scroll_horizontal = ttk.Scrollbar(transactions_frame, orient="horizontal", command=self.transaction_tree.xview)
        scroll_horizontal.pack(side="bottom", fill="x")
        self.transaction_tree.configure(xscrollcommand=scroll_horizontal.set)

    def on_filter_type_selected(self, event):
        selected_filter_type = self.filter_type_var.get()
        if selected_filter_type == "تاریخ":
            self.start_date_label.grid(row=2, column=0, padx=5, pady=5)
            self.start_date_entry.grid(row=2, column=1, padx=5, pady=5)
            self.end_date_label.grid(row=3, column=0, padx=5, pady=5)
            self.end_date_entry.grid(row=3, column=1, padx=5, pady=5)
            self.transaction_count_label.grid_remove()
            self.transaction_count_entry.grid_remove()
        elif selected_filter_type == "تعداد تراکنش":
            self.start_date_label.grid_remove()
            self.start_date_entry.grid_remove()
            self.end_date_label.grid_remove()
            self.end_date_entry.grid_remove()
            self.transaction_count_label.grid(row=2, column=0, padx=5, pady=5)
            self.transaction_count_entry.grid(row=2, column=1, padx=5, pady=5)

    def apply_filter(self):
        # Implement filtering logic based on the entry widget value and selected filter type
        filter_value = self.filter_type_var.get()
        filter_type = self.filter_type_var.get()
        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()
        transaction_count = self.transaction_count_entry.get()
        # Apply filter based on filter_value, filter_type, start_date, end_date, and transaction_count
        pass

    def on_transaction_selected(self, event):
        # Implement action when a transaction is selected
        pass



class MainWindow:
    def __init__(self, id: int, email: str, username: str, first_name: str, last_name: str):
        self.root = tk.Tk()
        self.root.title("Bank Details")
        self.root.geometry("800x600")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.loans_tab = LoansTab(self.notebook)
        self.notebook.add(self.loans_tab, text="وام‌ها")

        self.accounts_tab = AccountsTab(self.notebook, id)
        self.notebook.add(self.accounts_tab, text="حساب‌های بانکی")

        self.transaction_tab = TransactionsTab(self.notebook, id)
        self.notebook.add(self.transaction_tab, text="تراکنش ها")

        self.settings_tab = SettingsTab(self.notebook, id, email, username, first_name, last_name)
        self.notebook.add(self.settings_tab, text="تنظیمات")

        self.menu_bar = MenuBar(self.root)
        self.root.config(menu=self.menu_bar)

        self.root.mainloop()

# app = MainWindow()
