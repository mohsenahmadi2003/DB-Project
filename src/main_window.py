from module import *


class LoansTab(ttk.Frame):
    def __init__(self, parent, id):
        super().__init__(parent)
        self.id = id
        self.create_loans_table()

    def create_loans_table(self):
        loans_label = ttk.Label(self, text="وام ‌های من")
        loans_label.pack()

        filter_frame = ttk.Frame(self)
        filter_frame.pack(fill="y", expand=False)

        update_date_button = ttk.Button(filter_frame, text="آپدیت اطلاعات", command=self.update_date)
        update_date_button.grid(row=0, column=120, padx=5, pady=5)

        self.user_accounts_combo = ttk.Combobox(filter_frame, state="readonly", width=25)
        self.user_accounts_combo.grid(row=0, column=1, padx=5, pady=5)
        self.user_accounts_combo.bind("<<ComboboxSelected>>", self.on_user_account_selected)

        loan_list_frame = ttk.Frame(self)
        loan_list_frame.pack(fill="y", expand=True)

        self.loans_tree = ttk.Treeview(loan_list_frame, columns=(
            'ردیف', "شماره حساب", "مبلغ وام", "تاریخ شروع", 'تاریخ پایان', "وضعیت وام"),
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

        self.loans_tree.heading("#4", text="تاریخ پایان", anchor="center")
        self.loans_tree.column("#4", anchor='center')

        self.loans_tree.heading("#5", text="وضعیت وام", anchor="center")
        self.loans_tree.column("#5", anchor='center')

        self.loans_tree.tag_configure('center', anchor='center')

        # ایجاد یک اسکرول‌بار افقی
        x_scrollbar = ttk.Scrollbar(loan_list_frame, orient="horizontal", command=self.loans_tree.xview)
        x_scrollbar.pack(side="bottom", fill="x")

        # متصل کردن اسکرول‌بار به Treeview
        self.loans_tree.configure(xscrollcommand=x_scrollbar.set)

        self.update_date()

    def update_date(self):
        self.user_accounts_combo.delete(0, 'end')  # پاک کردن تمامی گزینه‌ها

        user_accounts = ORM.get_bank_accounts(self.id)
        print(user_accounts)
        self.user_accounts_combo['values'] = [f"{account[2]}" for account in
                                              user_accounts if account[7] == 0]

        for item in self.loans_tree.get_children():
            self.loans_tree.delete(item)

    def on_user_account_selected(self, event):
        print("11")
        for item in self.loans_tree.get_children():
            self.loans_tree.delete(item)

        selected_value = event.widget.get()
        loans = ORM.get_account_loans(selected_value)
        print(loans)
        for index, item in enumerate(loans):
            self.loans_tree.insert("", tk.END, text=str(index + 1),
                                   values=(f"{item[2]}", f"{item[3]}", f"{item[4]}", f"{item[5]}",
                                           f"{'فعال' if int(item[6]) == 1 else 'اتمام'}"),
                                   tags=('center',))


class LoansOfferTab(ttk.Frame):
    def __init__(self, parent, id):
        super().__init__(parent)
        self.id = id
        self.row_data = None
        self.create_loans_table()

    def create_loans_table(self):
        loans_label = ttk.Label(self, text="وام ‌های پیشنهادی من")
        loans_label.pack()

        filter_frame = ttk.Frame(self)
        filter_frame.pack(fill="y", expand=False)

        update_date_button = ttk.Button(filter_frame, text="آپدیت اطلاعات", command=self.update_date)
        update_date_button.grid(row=0, column=120, padx=5, pady=5)

        self.user_accounts_combo = ttk.Combobox(filter_frame, state="readonly", width=25)
        self.user_accounts_combo.grid(row=0, column=1, padx=5, pady=5)
        self.user_accounts_combo.bind("<<ComboboxSelected>>", self.on_user_account_selected)

        loan_list_frame = ttk.Frame(self)
        loan_list_frame.pack(fill="y", expand=True)

        self.loans_tree = ttk.Treeview(loan_list_frame,
                                       columns=('ردیف', "مبلغ دریافتی", "مبلغ پرداختی", 'پرداختی ماهانه', "تاریخ شروع",
                                                'تاریخ پایان', "نوع وام"),
                                       selectmode="browse")
        self.loans_tree.pack(fill=tk.BOTH, expand=True)

        self.loans_tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.loans_tree.heading("#0", text="شماره ردیف", anchor="center")
        self.loans_tree.column("#0", anchor='center')

        self.loans_tree.heading("#1", text="مبلغ دریافتی", anchor="center")
        self.loans_tree.column("#1", anchor='center')

        self.loans_tree.heading("#2", text="مبلغ پرداختی", anchor="center")
        self.loans_tree.column("#2", anchor='center')

        self.loans_tree.heading("#3", text='پرداختی ماهانه', anchor="center")
        self.loans_tree.column("#3", anchor='center')

        self.loans_tree.heading("#4", text="تاریخ شروع", anchor="center")
        self.loans_tree.column("#4", anchor='center')

        self.loans_tree.heading("#5", text="تاریخ پایان", anchor="center")
        self.loans_tree.column("#5", anchor='center')

        self.loans_tree.heading("#6", text="نوع وام", anchor="center")
        self.loans_tree.column("#6", anchor='center')

        self.loans_tree.tag_configure('center', anchor='center')

        # ایجاد یک اسکرول‌بار افقی
        x_scrollbar = ttk.Scrollbar(loan_list_frame, orient="horizontal", command=self.loans_tree.xview)
        x_scrollbar.pack(side="bottom", fill="x")

        # متصل کردن اسکرول‌بار به Treeview
        self.loans_tree.configure(xscrollcommand=x_scrollbar.set)

        request_frame = ttk.Frame(self)
        request_frame.pack(fill="y", expand=False)

        update_date_button = ttk.Button(request_frame, text="درخواست وام", command=self.request_loan)
        update_date_button.grid(row=0, column=120, padx=5, pady=5)

        self.update_date()

    def on_tree_select(self, event):
        selected_row = self.loans_tree.focus()  # دریافت ردیف انتخاب شده
        if selected_row:  # اگر ردیفی انتخاب شده باشد
            row_data = self.loans_tree.item(selected_row, 'values')  # دریافت داده‌های مربوط به ردیف انتخاب شده
            print("Selected Row Data:", row_data)
            self.row_data = row_data

    def request_loan(self):
        account_number = self.user_accounts_combo.get()  # دسترسی به مقدار انتخاب شده از Combobox

        if self.row_data == None:
            messagebox.showerror("خطا", "هیچ ردیفی انتخاب نشده است")
            return

        check_loan_active = ORM.get_active_loan_id(account_number)
        if check_loan_active == False:
            messagebox.showerror("خطا", 'خطا در اتصال به پایگاه داده')
            return
        elif int(check_loan_active) != 0:
            messagebox.showinfo("نتیحه", "شما وام فعال برای این حساب دارید")
            return
        else:
            output = ORM.insert_loan_and_payments(self.id, account_number, self.row_data[0])
            if output == False:
                messagebox.showerror("خطا", 'خطا در اتصال به پایگاه داده')
            if int(output) == 1:
                messagebox.showinfo("نتیحه", "وام واریز گردید")
            else:
                messagebox.showerror("خطا", 'خطا در واریز وام ')

    def update_date(self):
        self.user_accounts_combo.delete(0, 'end')  # پاک کردن تمامی گزینه‌ها

        user_accounts = ORM.get_bank_accounts(self.id)
        print(user_accounts)
        self.user_accounts_combo['values'] = [f"{account[2]}" for account in
                                              user_accounts if account[7] == 0]

        for item in self.loans_tree.get_children():
            self.loans_tree.delete(item)

    def on_user_account_selected(self, event):

        for item in self.loans_tree.get_children():
            self.loans_tree.delete(item)

        selected_value = event.widget.get()

        min_balance_two_month_ago = ORM.get_min_balance_by_account_number(selected_value)
        print(min_balance_two_month_ago)
        result: list = ORM.generate_loan_proposals(min_balance_two_month_ago)
        loan_type = None
        for index, item in enumerate(result):
            if index == 0:
                loan_type = "اصلی"
            else:
                loan_type = "پیشنهادی"
            self.loans_tree.insert("", tk.END, text=str(index + 1),
                                   values=(f"{item[0]}", f"{item[1]}", f"{item[2]}", f"{item[3]}",
                                           f"{item[4]}", loan_type),
                                   tags=('center',))


class AccountsTab(ttk.Frame):
    def __init__(self, parent, id):
        super().__init__(parent)
        self.id = id
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

        self.update_data_accounts()

        self.accounts_tree.tag_configure('center', anchor='center')

        self.accounts_tree.bind("<<TreeviewSelect>>", self.on_account_selected)
        self.accounts_tree.bind("<FocusOut>",
                                lambda event: self.accounts_tree.selection_remove(self.accounts_tree.selection()))

        # ایجاد فریم برای نمایش لیست حساب‌های بانکی
        selected_account_frame = ttk.Frame(self)
        selected_account_frame.pack()

        # ایجاد ویجت‌های مربوط به اطلاعات حساب انتخاب شده
        self.selected_account_number_label = ttk.Label(selected_account_frame, text="شماره حساب:")
        self.selected_account_number_label.grid(row=0, column=1)

        self.selected_primary_password_label = ttk.Label(selected_account_frame, text="رمز اول حساب:")
        self.selected_primary_password_label.grid(row=1, column=1)

        self.selected_amount_label = ttk.Label(selected_account_frame, text="موجودی حساب:")
        self.selected_amount_label.grid(row=2, column=1)

        self.selected_date_opened_label = ttk.Label(selected_account_frame, text="تاریخ افتتاح حساب:")
        self.selected_date_opened_label.grid(row=3, column=1)

        self.selected_date_closed_label = ttk.Label(selected_account_frame, text="تاریخ بسته شدن حساب:")
        self.selected_date_closed_label.grid(row=4, column=1)

        # ایجاد فریم برای نمایش لیست حساب‌های بانکی
        selected_account_status_description_frame = ttk.Frame(self)
        selected_account_status_description_frame.pack()

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

        # ایجاد ویجت آپدیت
        self.update_button = ttk.Button(selected_account_status_description_frame, text="آپدیت اطلاعات",
                                        command=self.update_data_accounts)
        self.update_button.grid(row=9, column=0, columnspan=2)

    def update_data_accounts(self):
        # پاک کردن اطلاعات قبلی
        for item in self.accounts_tree.get_children():
            self.accounts_tree.delete(item)

        # دریافت اطلاعات جدید از دیتابیس
        self.accounts = ORM.get_bank_accounts(self.id)

        for index, item in enumerate(self.accounts):
            self.accounts_tree.insert("", tk.END, text=str(index),
                                      values=(f"{item[2]}", f"{item[4]}", f"{'باز' if item[7] == 0 else 'مسدود'}"),
                                      tags=('center',))

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
            self.selected_date_opened_label.config(text=f"تاریخ افتتاح حساب: {data[5]}")
            self.selected_date_closed_label.config(text=f"تاریخ بسته شدن حساب: {data[6]}")
            self.selected_description_entry.delete(0, tk.END)  # پاک کردن محتویات اولیه توضیحات
            self.selected_description_entry.insert(0, data[8])  # وارد کردن توضیحات از دیتابیس
            print(data)
            if bool(data[7]) == True:
                self.selected_description_entry.config(state='disabled')
                self.selected_account_status_checkbutton.config(state='disabled')
                self.submit_button.config(state='disabled')
            else:
                self.selected_description_entry.config(state='normal')
                self.selected_account_status_checkbutton.config(state='normal')
                self.submit_button.config(state='normal')


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
        # settings_menu = tk.Menu(self, tearoff=0)
        # settings_menu.add_command(label="رفرش", comm)

        # اضافه کردن منوها به منوبار
        self.add_cascade(label="فایل", menu=file_menu)
        # self.add_cascade(label="آپدیت اطلاعات", menu=settings_menu)


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

        # ایجاد ویجت‌های انتخاب حساب کاربر
        user_accounts_label = ttk.Label(filter_frame, text="انتخاب حساب:")
        user_accounts_label.grid(row=1, column=0, padx=5, pady=5)

        self.user_accounts_combo = ttk.Combobox(filter_frame, state="readonly", width=25)
        self.user_accounts_combo.grid(row=1, column=1, padx=5, pady=5)
        self.user_accounts_combo.bind("<<ComboboxSelected>>", self.on_user_account_selected)

        # افزودن حساب‌های کاربر به Combobox
        update_date_button = ttk.Button(filter_frame, text="آپدیت اطلاعات", command=self.update_date)
        update_date_button.grid(row=0, column=120, padx=5, pady=5)

        self.update_date()
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
            "شماره ردیف", 'واریز / برداشت', "شماره حساب مبدا", "شماره حساب مقصد", "مقدار انتقال", 'تاریخ تراکنش',
            "وضعیت تراکنش",
            'توضیحات تراکنش', 'موجودی حساب تا این تراکنش'), selectmode="browse")
        self.transaction_tree.pack(fill="both", expand=True)

        self.transaction_tree.heading("#0", text="شماره ردیف", anchor="center")
        self.transaction_tree.column("#0", anchor='center')

        self.transaction_tree.heading("#1", text='واریز / برداشت', anchor="center")
        self.transaction_tree.column("#1", anchor='center')

        self.transaction_tree.heading("#2", text="شماره حساب مبدا", anchor="center")
        self.transaction_tree.column("#2", anchor='center')

        self.transaction_tree.heading("#3", text="شماره حساب مقصد", anchor="center")
        self.transaction_tree.column("#3", anchor='center')

        self.transaction_tree.heading("#4", text="مقدار انتقال", anchor="center")
        self.transaction_tree.column("#4", anchor='center')

        self.transaction_tree.heading("#5", text='تاریخ تراکنش', anchor="center")
        self.transaction_tree.column("#5", anchor='center')

        self.transaction_tree.heading("#6", text="وضعیت تراکنش", anchor="center")
        self.transaction_tree.column("#6", anchor='center')

        self.transaction_tree.heading("#7", text='توضیحات تراکنش', anchor="center")
        self.transaction_tree.column("#7", anchor='center')

        self.transaction_tree.heading("#8", text='موجودی حساب تا این تراکنش', anchor="center")
        self.transaction_tree.column("#8", anchor='center')

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
        self.transaction_count_entry.insert(0, "1")
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

    def update_date(self):
        print("update")
        self.user_accounts_combo.delete(0, 'end')  # پاک کردن تمامی گزینه‌ها

        user_accounts = ORM.get_bank_accounts(self.id)

        self.user_accounts_combo['values'] = [f"{account[2]}" for account in
                                              user_accounts if account[7] == 0]

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
        filter_type: str = self.filter_type_var.get()
        account_number: str = self.user_accounts_combo.get()
        self.transaction_tree.delete(*self.transaction_tree.get_children())
        if filter_type == "تعداد تراکنش":
            transaction_count = self.transaction_count_entry.get()
            if transaction_count.isdigit() and int(transaction_count) != 0:
                transaction_count = int(transaction_count)
                result: list = ORM.get_recent_transactions_by_user(account_number, transaction_count)
                print(result)
                if result == False:
                    messagebox.showerror("خطا", 'خطا در اتصال به پایگاه داده')
                elif result == []:
                    messagebox.showerror("خطا", "تراکنشی یافت نشد!")
                elif bool(int(result[0][0])) == False:
                    messagebox.showerror("خطا", "اطلاعاتی یافت نشد")
                else:
                    for index, transaction in enumerate(result, start=1):
                        self.transaction_tree.insert("", tk.END, text=str(index),
                                                     values=('برداشت' if transaction[8] == 'Withdraw' else 'واریز',
                                                             transaction[2], transaction[3], transaction[4],
                                                             transaction[5],
                                                             'موفق' if transaction[6] == 'Completed' else 'ناموفق',
                                                             transaction[7], "----"))
            else:
                messagebox.showerror("خطا", "تعداد باید یک عدد مثبت باشد")
        elif filter_type == "تاریخ":
            start_date = self.start_date_entry.get_date()
            end_date = self.end_date_entry.get_date()
            print(start_date, end_date)
            result: list = ORM.calculate_account_balance_with_date(account_number, start_date, end_date)
            print(result)
            if result == False:
                messagebox.showerror("خطا", "خطا در اتصال به پایگاه داده")
            elif result == []:
                messagebox.showerror("خطا", "تراکنشی یافت نشد!")
            elif bool(int(result[0][0])) == False:
                messagebox.showerror("خطا", "تاریخ ها اشتباه وارد شده اند")
            else:
                for index, transaction in enumerate(result, start=1):
                    transaction = list(transaction)
                    self.transaction_tree.insert("", tk.END, text=str(index),
                                                 values=('برداشت' if transaction[8] == 'Withdraw' else 'واریز',
                                                         transaction[1], transaction[2], transaction[3], transaction[4],
                                                         'موفق' if transaction[5] == 'Completed' else 'ناموفق',
                                                         transaction[6], transaction[7]))

    def on_transaction_selected(self, event):
        # Implement action when a transaction is selected
        pass

    def on_user_account_selected(self, event):
        # Implement action when a user account is selected
        pass


class TransferFundsTab(ttk.Frame):
    def __init__(self, parent, id, email):
        super().__init__(parent)
        self.id = id
        self.email = email
        self.tranaction_id = None
        self.user_accounts = ORM.get_bank_accounts(id)
        self.create_layout()

    def create_layout(self):
        frame = ttk.Frame(self)
        frame.pack(expand=True, fill="both", padx=20, pady=20)  # ابعاد بزرگ و فاصله از لبه‌ها

        title_label = ttk.Label(frame, text="انتقال وجه", font=("Helvetica", 24))
        title_label.grid(row=0, column=0, columnspan=3, pady=(20, 30))  # پایین و بالا

        self.check_button = ttk.Button(frame, text="آپدیت اطلاعات", command=self.update_date,
                                       width=20)
        self.check_button.grid(row=1, column=2, sticky=tk.W, pady=10)

        self.source_account_label = ttk.Label(frame, text="انتخاب حساب مبدا:", font=("Helvetica", 16))
        self.source_account_label.grid(row=1, column=0, sticky=tk.W, pady=10)

        self.source_account_combobox = ttk.Combobox(frame, font=("Helvetica", 16), width=30)  # ابعاد زیادتر
        self.source_account_combobox.grid(row=1, column=1, sticky=tk.W, pady=10)
        print(self.user_accounts)
        self.source_account_combobox['values'] = [f"{account[2]}" for account in
                                                  self.user_accounts if account[8] == 0]

        self.source_account_combobox.set(self.user_accounts[0][2])

        self.destination_account_label = ttk.Label(frame, text="شماره حساب مقصد:", font=("Helvetica", 16))
        self.destination_account_label.grid(row=2, column=0, sticky=tk.W, pady=10)

        self.destination_account_entry = ttk.Entry(frame, font=("Helvetica", 16), width=30)  # ابعاد زیادتر
        self.destination_account_entry.grid(row=2, column=1, sticky=tk.W, pady=10)

        self.check_button = ttk.Button(frame, text="بررسی شماره حساب مقصد", command=self.check_destination_account,
                                       width=20)
        self.check_button.grid(row=2, column=2, sticky=tk.W, pady=10)

        self.transfer_amount_label = ttk.Label(frame, text="مقدار انتقال:", font=("Helvetica", 16))
        self.transfer_amount_label.grid(row=3, column=0, sticky=tk.W, pady=10)

        self.transfer_amount_entry = ttk.Entry(frame, font=("Helvetica", 16), width=30)  # ابعاد زیادتر
        self.transfer_amount_entry.grid(row=3, column=1, sticky=tk.W, pady=10)

        self.description_label = ttk.Label(frame, text="توضیحات:", font=("Helvetica", 16))
        self.description_label.grid(row=4, column=0, sticky=tk.W, pady=10)

        self.description_entry = ttk.Entry(frame, font=("Helvetica", 16), width=30)  # ابعاد زیادتر
        self.description_entry.grid(row=4, column=1, sticky=tk.W, pady=10, columnspan=2)

        self.transfer_button = ttk.Button(frame, text="انتقال وجه", command=self.create_transaction, width=30)
        self.transfer_button.grid(row=5, column=0, columnspan=3, pady=20)  # ردیف بعدی

        self.cancel_button = ttk.Button(frame, text="لغو تراکنش", command=self.cancel_transaction, width=30)
        self.cancel_button.grid(row=6, column=0, columnspan=3, pady=20)  # ردیف بعدی
        self.cancel_button.config(state="disabled")

        password_frame = ttk.Frame(self)
        password_frame.pack(fill="y", expand=False, padx=20, pady=(0, 20))  # بالا و پایین
        # password_frame.grid(row=3, column=3)

        password_frame = ttk.Frame(self)
        password_frame.pack(fill="y", expand=False, padx=20, pady=(0, 20))  # بالا و پایین

        self.password_label = ttk.Label(password_frame, text="رمز دوم:", font=("Helvetica", 16))
        self.password_label.grid(row=0, column=0, sticky=tk.W)

        self.password_entry = ttk.Entry(password_frame, show="*", font=("Helvetica", 16), width=30)  # ابعاد زیادتر
        self.password_entry.grid(row=0, column=1, sticky=tk.W)

        self.toggle_password_button = ttk.Button(password_frame, text="پنهان کردن رمز",
                                                 command=self.toggle_password_visibility,
                                                 cursor="hand2",
                                                 style="TButton")  # تغییر اندازه فونت و دکمه‌ها

        self.toggle_password_button.grid(row=0, column=2, padx=5, pady=5)

        self.confirm_button = ttk.Button(password_frame, text="تأیید", command=self.confirm_transfer, width=20)
        self.confirm_button.grid(row=1, column=1, sticky=tk.W)  # سمت راست

        self.request_secondary_password_button = ttk.Button(password_frame, text="درخواست رمز دوم",
                                                            command=self.request_secondary_password, width=20)
        self.request_secondary_password_button.grid(row=1, column=2, sticky=tk.W)

        self.password_label.grid_forget()
        self.password_entry.grid_forget()
        self.confirm_button.grid_forget()
        self.request_secondary_password_button.grid_forget()
        self.toggle_password_button.grid_forget()

        self.source_account_combobox.config(state="readonly")
        self.cancel_button.grid_forget()

        self.update_date()

    def update_date(self):
        print("update")
        self.source_account_combobox.delete(0, 'end')  # پاک کردن تمامی گزینه‌ها

        user_accounts = ORM.get_bank_accounts(self.id)

        self.source_account_combobox['values'] = [f"{account[2]}" for account in
                                                  user_accounts if account[7] == 0]

    def toggle_password_visibility(self):
        if self.password_entry.cget("show") == "":
            self.password_entry.config(show="*")
            self.toggle_password_button.config(text="نمایش رمز")
        else:
            self.password_entry.config(show="")
            self.toggle_password_button.config(text="پنهان کردن رمز")

    def disable_button(self):
        self.request_secondary_password_button.config(state=tk.DISABLED)

    def enable_button(self):
        self.request_secondary_password_button.config(state=tk.NORMAL)

    def clicked(self):
        self.disable_button()
        self.after(60000, self.enable_button)  # 60000 میلی ثانیه معادل 1 دقیقه است

    def request_secondary_password(self):
        source_account_number: str = self.source_account_combobox.get()
        result = ORM.secondary_password(self.tranaction_id, source_account_number)
        print(result)
        if result == False:
            tk.messagebox.showerror("خطا",
                                    "خطا در اتصال به پایگاه داده")
            return
        elif int(result[0]) == 1:
            self.clicked()
            tk.messagebox.showinfo("نتیجه",
                                   "رمز دوم برای شما ارسال شد. توجه داشته باشد این رمز تا یک دقیقه بیشتر اعتبار ندارد.")

            email_sender = EmailSender()
            email_sender.connect_email()

            email_sender.send_mail(receiver=self.email, subject="رمز دوم",
                                   html_body=EmailNotification.secondary_password(result[1]))
            email_sender.close_connection()
            print("رمز ارسال شد")

        else:
            tk.messagebox.showerror("خطا",
                                    "خطا در ثبت و ارسال رمز دوم")

    def cancel_transaction(self):
        confirm_cancel = tk.messagebox.askyesno("تایید لغو تراکنش",
                                                "آیا مطمئن هستید که می‌خواهید این تراکنش را لغو کنید؟")
        if confirm_cancel:

            result = ORM.cancel_transaction(self.tranaction_id)
            if result == False:
                tk.messagebox.showerror("خطا",
                                        "خطا در اتصال به پایگاه داده")
                return
            elif (int(result[0])) == 1:
                self.enable_fields()
                self.clear_fields()
                self.password_label.grid_remove()
                self.password_entry.grid_forget()
                self.password_entry.delete(0, tk.END)
                self.confirm_button.grid_forget()  # حذف دکمه لغو تراکنش از نمایش
                self.cancel_button.config(state="disabled")
                self.source_account_combobox.config(state="readonly")
                self.cancel_button.grid_forget()
                self.request_secondary_password_button.grid_forget()
                self.source_account_combobox.set(self.user_accounts[0][2])
                self.toggle_password_button.grid_forget()

                tk.messagebox.showinfo("نتیجه",
                                       "تراکنش با موفقیت لغو شد")
            elif (int(result[0])) == 0:
                tk.messagebox.showerror("خطا",
                                        "تراکنش لغو نشد")

    def clear_fields(self):
        self.source_account_combobox.set("")
        self.destination_account_entry.delete(0, tk.END)
        self.transfer_amount_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

    def enable_fields(self):
        self.source_account_combobox.config(state="readonly")
        self.destination_account_entry.config(state="normal")
        self.transfer_button.config(state="normal")
        self.transfer_amount_entry.config(state="normal")
        self.description_entry.config(state="normal")

    def create_transaction(self):
        # ایجاد یک بخش برای ورود رمز دوم

        source_account_number: str = self.source_account_combobox.get()
        transfer_amount: str = self.transfer_amount_entry.get()
        description: str = self.description_entry.get()
        destination_account_number: str = self.destination_account_entry.get()

        validate_amount = ORM.validate_transaction_amount(amount=transfer_amount)

        if self.is_valid_destination_account(destination_account_number) == False:
            tk.messagebox.showerror("خطا",
                                    f"نام شماره حساب مقصد نا معتبر")
        elif validate_amount == False:
            tk.messagebox.showerror("خطا",
                                    "مبلغ قابل انتقال نا معتبر هست")
        else:

            result = ORM.create_transaction(source_account_number, destination_account_number, transfer_amount,
                                            description)
            if result == False:
                tk.messagebox.showerror("خطا",
                                        "خطا در اتصال به پایگاه داده")
                return
            else:
                if bool(int(result[0])) == True:

                    self.tranaction_id = result[1]

                    self.password_label.grid()
                    self.password_entry.grid()

                    self.confirm_button.grid()  # نمایش

                    # قفل کردن ورودی‌ها پس از کلیک بر روی دکمه انتقال وجه
                    self.source_account_combobox.config(state="disabled")
                    self.destination_account_entry.config(state="disabled")
                    self.transfer_amount_entry.config(state="disabled")
                    self.description_entry.config(state="disabled")
                    self.transfer_button.config(state="disabled")
                    self.cancel_button.config(state="normal")
                    self.cancel_button.grid()
                    self.request_secondary_password_button.config(state="normal")
                    self.request_secondary_password_button.grid()
                    self.toggle_password_button.config(state="normal")
                    self.toggle_password_button.grid()

                else:
                    tk.messagebox.showerror("خطا",
                                            "خطا ثبت تراکنش")

    def check_destination_account(self):
        # کد بررسی شماره حساب مقصد
        destination_account_number: str = self.destination_account_entry.get()

        # اگر شماره حساب مقصد معتبر است
        if name := self.is_valid_destination_account(destination_account_number):
            # نمایش نام شماره حساب مقصد به کاربر
            tk.messagebox.showinfo("نتیجه",
                                   f"نام شماره حساب مقصد: {name}")
            # self.destination_account_entry.config(state="readonly")

        else:
            tk.messagebox.showerror("خطا", "شماره حساب مقصد نامعتبر است!")

    def is_valid_destination_account(self, account_number):
        result: str = ORM.check_destination_account(account_number)
        if result != 'Not found':
            return result
        return False

    def confirm_transfer(self):
        second_password = self.password_entry.get()
        print(f"{second_password=}")
        result = ORM.check_secondary_password(self.tranaction_id, second_password)
        print('result - check_secondary_password', result)
        if result == 0:
            tk.messagebox.showerror("خطا", "رمز دوم نا معتبر هست!")
            return
            # بررسی رمز دوم
        elif int(result) == 1:
            source_account_number: str = self.source_account_combobox.get()
            transfer_amount: int = int(self.transfer_amount_entry.get())
            destination_account_number: str = self.destination_account_entry.get()

            output = ORM.transfer_funds(source_account_number=source_account_number,
                                        destination_account_number=destination_account_number,
                                        transfer_amount=transfer_amount,
                                        transaction_id=int(self.tranaction_id))
            print('output = ', output)
            if output == False:
                tk.messagebox.showerror("خطا",
                                        "خطا در اتصال به پایگاه داده")
                return
            elif int(output[0]) == 1:
                tk.messagebox.showinfo("موفقیت",
                                       "تراکنش با موفقیت انجام شد")

                email_sender = EmailSender()
                email_sender.connect_email()

                send_amount = ORM.get_amount_account(source_account_number)

                email_sender.send_mail(receiver=self.email, subject="ّبرداشت",
                                       html_body=EmailNotification.withdraw(send_amount, transfer_amount,
                                                                            source_account_number))

                recive_amount = ORM.get_amount_account(destination_account_number)
                recive_email = ORM.get_email_with_account_number(destination_account_number)

                email_sender.send_mail(receiver=recive_email, subject="واریز",
                                       html_body=EmailNotification.deposite(recive_amount, transfer_amount,
                                                                            destination_account_number))
                email_sender.close_connection()

                self.enable_fields()
                self.clear_fields()
                self.password_label.grid_forget()
                self.password_entry.grid_forget()
                self.password_entry.delete(0, tk.END)

                self.confirm_button.grid_forget()  # حذف دکمه لغو تراکنش از نمایش
                self.cancel_button.config(state="disabled")
                self.source_account_combobox.config(state="readonly")
                self.cancel_button.grid_forget()
                self.request_secondary_password_button.grid_forget()
                self.source_account_combobox.set(self.user_accounts[0][2])
                self.toggle_password_button.grid_forget()


            else:
                tk.messagebox.showerror("خطا", "موجودی حساب کافی نیست!")
        else:
            tk.messagebox.showerror("خطا",
                                    "خطا در اتصال به پایگاه داده")


class MainWindow:
    def __init__(self, id: int, email: str, username: str, first_name: str, last_name: str):
        self.root = tk.Tk()
        self.root.title("Bank Details")
        self.root.geometry("800x600")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.loans_tab = LoansTab(self.notebook, id)
        self.notebook.add(self.loans_tab, text="وام ‌های من")

        self.loans_offer_tab = LoansOfferTab(self.notebook, id)
        self.notebook.add(self.loans_offer_tab, text="وام ‌های پیشنهادی من")

        self.accounts_tab = AccountsTab(self.notebook, id)
        self.notebook.add(self.accounts_tab, text="حساب‌های بانکی")

        self.transaction_tab = TransactionsTab(self.notebook, id)
        self.notebook.add(self.transaction_tab, text="تراکنش ها")

        self.transfer_funds_tab = TransferFundsTab(self.notebook, id, email)
        self.notebook.add(self.transfer_funds_tab, text="انتقال وجه")

        self.settings_tab = SettingsTab(self.notebook, id, email, username, first_name, last_name)
        self.notebook.add(self.settings_tab, text="تنظیمات")

        self.menu_bar = MenuBar(self.root)
        self.root.config(menu=self.menu_bar)

        self.root.mainloop()

# app = MainWindow()
