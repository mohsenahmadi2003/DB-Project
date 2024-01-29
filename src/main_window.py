import tkinter as tk
from tkinter import ttk

accounts_tree = None
loans_tree = None
notebook = None


def on_account_selected(event):
    global accounts_tree
    selected_items = accounts_tree.selection()
    if selected_items:
        selected_item = selected_items[0]
        account_info = accounts_tree.item(selected_item, "values")
        print("Selected Bank Account:", account_info)


def on_loan_selected(event):
    global loans_tree
    selected_items = loans_tree.selection()
    if selected_items:
        selected_item = selected_items[0]
        loan_info = loans_tree.item(selected_item, "values")
        print("Selected Loan:", loan_info)


def create_accounts_table(parent):
    global accounts_tree
    accounts_frame = ttk.Frame(parent)
    accounts_frame.pack(fill=tk.BOTH, expand=True)

    accounts_label = ttk.Label(accounts_frame, text="لیست حساب‌های بانکی")
    accounts_label.pack()

    accounts_tree = ttk.Treeview(accounts_frame, columns=("شماره ردیف", "نام", "شماره حساب", "موجودی"),
                                 selectmode="browse")
    accounts_tree.pack(fill=tk.BOTH, expand=True)

    accounts_tree.heading("#0", text="شماره ردیف", anchor="center")
    accounts_tree.column("#0", anchor='center')

    accounts_tree.heading("#1", text="نام", anchor="center")
    accounts_tree.column("#1", anchor='center')

    accounts_tree.heading("#2", text="شماره حساب", anchor="center")
    accounts_tree.column("#2", anchor='center')

    accounts_tree.heading("#3", text="موجودی", anchor="center")
    accounts_tree.column("#3", anchor='center')

    for i in range(10):
        accounts_tree.insert("", tk.END, text=str(i), values=("حساب " + str(i + 1), "1234567890", "$1000"),
                             tags=('center',))

    accounts_tree.tag_configure('center', anchor='center')

    accounts_tree.bind("<<TreeviewSelect>>", on_account_selected)
    accounts_tree.bind("<FocusOut>", lambda event: accounts_tree.selection_remove(accounts_tree.selection()))


def create_loans_table(parent):
    global loans_tree
    loans_frame = ttk.Frame(parent)
    loans_frame.pack(fill=tk.BOTH, expand=True)

    loans_label = ttk.Label(loans_frame, text="لیست وام‌ها")
    loans_label.pack()

    loans_tree = ttk.Treeview(loans_frame, columns=('ردیف', "شماره حساب", "مبلغ وام", "تاریخ شروع"),
                              selectmode="browse")
    loans_tree.pack(fill=tk.BOTH, expand=True)

    loans_tree.heading("#0", text="شماره ردیف", anchor="center")
    loans_tree.column("#0", anchor='center')

    loans_tree.heading("#1", text="شماره حساب", anchor="center")
    loans_tree.column("#1", anchor='center')

    loans_tree.heading("#2", text="مبلغ وام", anchor="center")
    loans_tree.column("#2", anchor='center')

    loans_tree.heading("#3", text="تاریخ شروع", anchor="center")
    loans_tree.column("#3", anchor='center')

    for i in range(15):
        loans_tree.insert("", tk.END, text=str(i), values=("1234567890", "$5000", "2024-01-01"), tags=('center',))

    loans_tree.tag_configure('center', anchor='center')

    loans_tree.bind("<<TreeviewSelect>>", on_loan_selected)
    loans_tree.bind("<FocusOut>", lambda event: loans_tree.selection_remove(loans_tree.selection()))


def create_user_info_tab(parent):
    user_info_tab = ttk.Frame(parent)
    parent.add(user_info_tab, text="اطلاعات کاربر")

    name_label = ttk.Label(user_info_tab, text="نام: John")
    name_label.pack()

    last_name_label = ttk.Label(user_info_tab, text="نام خانوادگی: Doe")
    last_name_label.pack()

    username_label = ttk.Label(user_info_tab, text="یوزر نیم: johndoe")
    username_label.pack()

    email_label = ttk.Label(user_info_tab, text="ایمیل: johndoe@example.com")
    email_label.pack()

class ChangePasswordTab:
    def __init__(self, parent):
        self.change_password_tab = ttk.Frame(parent)
        parent.add(self.change_password_tab, text="تغییر پسورد")

        old_password_label = ttk.Label(self.change_password_tab, text="پسورد قدیمی:")
        old_password_label.pack()

        self.old_password_entry = ttk.Entry(self.change_password_tab, show="*")
        self.old_password_entry.pack()

        new_password_label = ttk.Label(self.change_password_tab, text="پسورد جدید:")
        new_password_label.pack()

        self.new_password_entry = ttk.Entry(self.change_password_tab, show="*")
        self.new_password_entry.pack()

        confirm_password_label = ttk.Label(self.change_password_tab, text="تایید پسورد جدید:")
        confirm_password_label.pack()

        self.confirm_password_entry = ttk.Entry(self.change_password_tab, show="*")
        self.confirm_password_entry.pack()

        self.show_password_var = tk.BooleanVar()
        show_password_checkbutton = ttk.Checkbutton(self.change_password_tab, text="نمایش پسورد",
                                                    variable=self.show_password_var,
                                                    command=self.toggle_show_password)
        show_password_checkbutton.pack()

        change_button = ttk.Button(self.change_password_tab, text="تغییر پسورد", command=self.change_password)
        change_button.pack()

    def toggle_show_password(self):
        if self.show_password_var.get():
            self.old_password_entry.config(show="")
            self.new_password_entry.config(show="")
            self.confirm_password_entry.config(show="")
        else:
            self.old_password_entry.config(show="*")
            self.new_password_entry.config(show="*")
            self.confirm_password_entry.config(show="*")

    def change_password(self):
        old_password = self.old_password_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # بررسی صحت پسوردها و اعمال تغییرات بر روی پسورد

        print("پسورد با موفقیت تغییر یافت.")

root = tk.Tk()
root.title("Bank Details")
root.geometry("800x600")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

loans_tab = ttk.Frame(notebook)
notebook.add(loans_tab, text="وام‌ها")
create_loans_table(loans_tab)

accounts_tab = ttk.Frame(notebook)
notebook.add(accounts_tab, text="حساب‌های بانکی")
create_accounts_table(accounts_tab)

create_user_info_tab(notebook)

# اضافه کردن تب تغییر پسورد به نوت‌بوک
change_password_tab = ChangePasswordTab(notebook)

if __name__ == '__main__':
    root.mainloop()
