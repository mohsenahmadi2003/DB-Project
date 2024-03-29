# وارد کردن ماژول‌های مورد نیاز
import mysql.connector
import configparser
from db_connection import DatabaseFactory
import os
from time import sleep

BASEDIR = os.path.dirname(os.path.abspath(__file__))

# خواندن اطلاعات از فایل پیکربندی
config = configparser.ConfigParser()
config.read(BASEDIR + '\config.ini')

# خواندن اطلاعات مورد نیاز از فایل پیکربندی
host = config.get("database", "host")
database = config.get('database', 'database')
db_username = config.get('database', 'user')
db_password = config.get('database', 'password')


# تعریف کلاس ORM برای ارتباط با پایگاه داده
class ORM:
    @staticmethod
    def login(username: str, password: str):
        result = None
        try:
            # ایجاد اتصال به پایگاه داده
            db = DatabaseFactory.create_connection(host, database, db_username, db_password)

            # اگر اتصال برقرار بود
            if db.is_connected():
                # ایجاد یک cursor برای اجرای کوئری‌ها
                cursor = db.cursor()

                # ساخت کوئری برای ایجاد تابع در پایگاه داده
                query = f"""
                        CALL LoginUser('{username}', '{password}');
                """

                # اجرای کوئری
                cursor.execute(query)
                result = cursor.fetchone()

        except mysql.connector.Error as error:
            print("خطا در اتصال به پایگاه داده MySQL:", error)
            return False

        finally:
            # بستن اتصال
            if db.is_connected():
                cursor.close()
                db.close()
                print("اتصال MySQL بسته شد.")

        return result

    @staticmethod
    def update_password(user_id: int, old_password: str, new_password: str):
        result = None
        try:
            # ایجاد اتصال به پایگاه داده
            db = DatabaseFactory.create_connection(host, database, db_username, db_password)

            # اگر اتصال برقرار بود
            if db.is_connected():
                # ایجاد یک cursor برای اجرای کوئری‌ها
                cursor = db.cursor()

                # ساخت کوئری برای فراخوانی فرآیند در پایگاه داده
                cursor.callproc("UpdatePassword", [user_id, old_password, new_password])

                for data in cursor.stored_results():
                    rows = data.fetchall()
                    result = rows[0]
                    break

                db.commit()

        except mysql.connector.Error as error:
            print("خطا در اتصال به پایگاه داده MySQL:", error)
            return False

        finally:
            # بستن اتصال
            if db.is_connected():
                cursor.close()
                db.close()
                print("اتصال MySQL بسته شد.")

        return result

    @staticmethod
    def get_bank_accounts(user_id: int):
        result = []
        try:
            # ایجاد اتصال به پایگاه داده
            db = DatabaseFactory.create_connection(host, database, db_username, db_password)

            # اگر اتصال برقرار بود
            if db.is_connected():
                # ایجاد یک cursor برای اجرای کوئری‌ها
                cursor = db.cursor()

                cursor.callproc("GetUserBankAccounts", [user_id])

                # اجرای کوئری با ورودی‌های مورد نیاز تابع
                for data in cursor.stored_results():
                    rows = data.fetchall()
                    for row in rows:
                        result.append(row)


        except mysql.connector.Error as error:
            print("خطا در اتصال به پایگاه داده MySQL:", error)
            return False

        finally:
            # بستن اتصال
            if db.is_connected():
                cursor.close()
                db.close()
                print("اتصال MySQL بسته شد.")

        return result

    @staticmethod
    def block_bank_account(account_number: str, description: str):
        result = []
        try:
            # ایجاد اتصال به پایگاه داده
            db = DatabaseFactory.create_connection(host, database, db_username, db_password)

            # اگر اتصال برقرار بود
            if db.is_connected():
                # ایجاد یک cursor برای اجرای کوئری‌ها
                cursor = db.cursor()

                cursor.callproc("BlockBankAccount", [account_number, description])

                # اجرای کوئری با ورودی‌های مورد نیاز تابع
                for data in cursor.stored_results():
                    rows = data.fetchall()
                    for row in rows:
                        result.append(row)

                db.commit()
        except mysql.connector.Error as error:
            print("خطا در اتصال به پایگاه داده MySQL:", error)
            return False

        finally:
            # بستن اتصال
            if db.is_connected():
                cursor.close()
                db.close()
                print("اتصال MySQL بسته شد.")

        return result

    @staticmethod
    def get_recent_transactions_by_user(account_number: str, limit: int):
        result = []
        try:
            # ایجاد اتصال به پایگاه داده
            db = DatabaseFactory.create_connection(host, database, db_username, db_password)

            # اگر اتصال برقرار بود
            if db.is_connected():
                # ایجاد یک cursor برای اجرای کوئری‌ها
                cursor = db.cursor()

                cursor.callproc("GetRecentTransactionsByUser", [account_number, limit])

                # اجرای کوئری با ورودی‌های مورد نیاز تابع
                for data in cursor.stored_results():
                    rows = data.fetchall()
                    for row in rows:
                        result.append(row)

        except mysql.connector.Error as error:
            print("خطا در اتصال به پایگاه داده MySQL:", error)
            return False

        finally:
            # بستن اتصال
            if db.is_connected():
                cursor.close()
                db.close()
                print("اتصال MySQL بسته شد.")

        return result

    @staticmethod
    def transfer_funds(source_account_number: str, destination_account_number: str, transfer_amount: str,
                       transaction_id: int):
        result = None
        db = None
        cursor = None
        try:
            # ایجاد اتصال به پایگاه داده
            db = DatabaseFactory.create_connection(host, database, db_username, db_password)

            # اگر اتصال برقرار بود
            if db.is_connected():
                # ایجاد یک cursor برای اجرای کوئری‌ها
                cursor = db.cursor()

                cursor.callproc("TransferFunds",
                                [source_account_number, destination_account_number, transfer_amount, transaction_id])

                # اجرای کوئری با ورودی‌های مورد نیاز تابع
                for date in cursor.stored_results():
                    result = date.fetchone()

        except mysql.connector.Error as error:
            print("خطا در اتصال به پایگاه داده MySQL:", error)
            return False

        finally:
            # بستن اتصال
            if db.is_connected():
                cursor.close()
                db.close()
                print("اتصال MySQL بسته شد.")

        return result

    @staticmethod
    def calculate_account_balance_with_date(account_number: str, start_date: str, end_date: str):
        result = []
        try:
            # ایجاد اتصال به پایگاه داده
            db = DatabaseFactory.create_connection(host, database, db_username, db_password)

            # اگر اتصال برقرار بود
            if db.is_connected():
                # ایجاد یک cursor برای اجرای کوئری‌ها
                cursor = db.cursor()

                cursor.callproc("CalculateAccountBalance", [account_number, start_date, end_date])
                # اجرای کوئری با ورودی‌های مورد نیاز تابع
                for data in cursor.stored_results():
                    rows = data.fetchall()
                    for row in rows:
                        if len(list(row)) == 9 or len(list(row)) == 2:
                            result.append(row)

        except mysql.connector.Error as error:
            print("خطا در اتصال به پایگاه داده MySQL:", error)
            return False

        finally:
            # بستن اتصال
            if db.is_connected():
                cursor.close()
                db.close()
                print("اتصال MySQL بسته شد.")

        return result

    @staticmethod
    def create_transaction(source_account_number: str, destination_account_number: str, transfer_amount: str,
                           description: str):
        """
        برای ساخت یک ترنس اکشن داخل جدول مورد نظر
        :param source_account_number:
        :param destination_account_number:
        :param transfer_amount:
        :param description:
        :return:
        0 or 1
        """
        result = None
        db = None
        cursor = None
        try:
            # ایجاد اتصال به پایگاه داده
            db = DatabaseFactory.create_connection(host, database, db_username, db_password)

            # اگر اتصال برقرار بود
            if db.is_connected():
                # ایجاد یک cursor برای اجرای کوئری‌ها
                cursor = db.cursor()

                try:
                    cursor.callproc("Process_Transaction",
                                    [source_account_number, destination_account_number, transfer_amount, description])

                    for date in cursor.stored_results():
                        result = date.fetchone()

                    db.commit()


                except mysql.connector.Error as error:
                    # Rollback تراکنش در صورت بروز خطا
                    db.rollback()

                    # بررسی خطای حجم کافی موجودی در حساب مبدا
                    if error.errno == 45000:
                        print("Insufficient balance in the source account")
                    else:
                        print("Error:", error)


        except mysql.connector.Error as error:
            print("خطا در اتصال به پایگاه داده MySQL:", error)
            return False

        finally:
            # بستن اتصال
            if db.is_connected():
                cursor.close()
                db.close()
                print("اتصال MySQL بسته شد.")

        return result

    @staticmethod
    def cancel_transaction(transaction_id: int, source_account_number, destination_account_number):
        """
        برای کسنل کردن ترنس اکشن و به حالت falid در آمدن ترنس اکشن
        :param transaction_id:
        :return:
        """
        result = None
        db = None
        cursor = None
        try:
            # ایجاد اتصال به پایگاه داده
            db = DatabaseFactory.create_connection(host, database, db_username, db_password)

            # اگر اتصال برقرار بود
            if db.is_connected():
                # ایجاد یک cursor برای اجرای کوئری‌ها
                cursor = db.cursor()

                try:
                    cursor.callproc("Cancel_Process_Transaction",
                                    [transaction_id, source_account_number, destination_account_number])

                    for date in cursor.stored_results():
                        result = date.fetchone()

                    db.commit()


                except mysql.connector.Error as error:
                    # Rollback تراکنش در صورت بروز خطا
                    db.rollback()

                    # بررسی خطای حجم کافی موجودی در حساب مبدا
                    if error.errno == 45000:
                        print("Insufficient balance in the source account")
                    else:
                        print("Error:", error)


        except mysql.connector.Error as error:
            print("خطا در اتصال به پایگاه داده MySQL:", error)
            return False

        finally:
            # بستن اتصال
            if db.is_connected():
                cursor.close()
                db.close()
                print("اتصال MySQL بسته شد.")

        return result

    @staticmethod
    def check_destination_account(account_number: str):
        result = None
        db = None
        cursor = None
        try:
            # ایجاد اتصال به پایگاه داده
            db = DatabaseFactory.create_connection(host, database, db_username, db_password)

            # اگر اتصال برقرار بود
            if db.is_connected():
                # ایجاد یک cursor برای اجرای کوئری‌ها
                cursor = db.cursor()

                # ساخت کوئری برای ایجاد تابع در پایگاه داده
                cursor.execute(F"SELECT GetAccountOwnerNameFunction({account_number})")
                result = cursor.fetchone()

        except mysql.connector.Error as error:
            print("خطا در اتصال به پایگاه داده MySQL:", error)
            return False

        finally:
            # بستن اتصال
            if db.is_connected():
                cursor.close()
                db.close()
                print("اتصال MySQL بسته شد.")

        return result[0]

    @staticmethod
    def check_secondary_password(transaction_id: int, secondary_password: str):
        result = None
        db = None
        cursor = None
        try:
            # ایجاد اتصال به پایگاه داده
            db = DatabaseFactory.create_connection(host, database, db_username, db_password)

            # اگر اتصال برقرار بود
            if db.is_connected():
                # ایجاد یک cursor برای اجرای کوئری‌ها
                cursor = db.cursor()

                # ساخت کوئری برای ایجاد تابع در پایگاه داده
                cursor.execute(F"SELECT CheckSecondaryPassword({transaction_id}, {secondary_password})")
                print("CheckSecondaryPassword = ", result := cursor.fetchall()[0])
                # result = cursor.fetchone()

        except mysql.connector.Error as error:
            print("خطا در اتصال به پایگاه داده MySQL:", error)
            return False

        finally:
            # بستن اتصال
            if db.is_connected():
                cursor.close()
                db.close()
                print("اتصال MySQL بسته شد.")

        return result[0]

    @staticmethod
    def secondary_password(transaction_id: int, source_account_number: str):
        result = None
        db = None
        cursor = None
        try:
            # ایجاد اتصال به پایگاه داده
            db = DatabaseFactory.create_connection(host, database, db_username, db_password)

            # اگر اتصال برقرار بود
            if db.is_connected():
                # ایجاد یک cursor برای اجرای کوئری‌ها
                cursor = db.cursor()

                cursor.callproc("SecondaryPassword",
                                [transaction_id, source_account_number])

                for date in cursor.stored_results():
                    result = date.fetchall()
                print(result)
                db.commit()


        except mysql.connector.Error as error:
            print("خطا در اتصال به پایگاه داده MySQL:", error)
            return False

        finally:
            # بستن اتصال
            if db.is_connected():
                cursor.close()
                db.close()
                print("اتصال MySQL بسته شد.")

        return result[0]

    @staticmethod
    def validate_transaction_amount(amount: float):
        result = None
        db = None
        cursor = None
        try:
            # ایجاد اتصال به پایگاه داده
            db = DatabaseFactory.create_connection(host, database, db_username, db_password)

            # اگر اتصال برقرار بود
            if db.is_connected():
                # ایجاد یک cursor برای اجرای کوئری‌ها
                cursor = db.cursor()

                # ساخت کوئری برای ایجاد تابع در پایگاه داده
                cursor.execute(F"SELECT ValidateTransactionAmount({amount})")
                result = cursor.fetchone()

        except mysql.connector.Error as error:
            print("خطا در اتصال به پایگاه داده MySQL:", error)
            return False

        finally:
            # بستن اتصال
            if db.is_connected():
                cursor.close()
                db.close()
                print("اتصال MySQL بسته شد.")

        return result[0]

    @staticmethod
    def get_email_with_account_number(account_number: str):
        result = None
        db = None
        cursor = None
        try:
            # ایجاد اتصال به پایگاه داده
            db = DatabaseFactory.create_connection(host, database, db_username, db_password)

            # اگر اتصال برقرار بود
            if db.is_connected():
                # ایجاد یک cursor برای اجرای کوئری‌ها
                cursor = db.cursor()

                # ساخت کوئری برای ایجاد تابع در پایگاه داده
                cursor.execute(F"SELECT GetEmailWithAccountNumber({account_number})")
                result = cursor.fetchone()

        except mysql.connector.Error as error:
            print("خطا در اتصال به پایگاه داده MySQL:", error)
            return False

        finally:
            # بستن اتصال
            if db.is_connected():
                cursor.close()
                db.close()
                print("اتصال MySQL بسته شد.")

        return result[0]

    @staticmethod
    def get_amount_account(account_number: str):
        result = None
        db = None
        cursor = None
        try:
            # ایجاد اتصال به پایگاه داده
            db = DatabaseFactory.create_connection(host, database, db_username, db_password)

            # اگر اتصال برقرار بود
            if db.is_connected():
                # ایجاد یک cursor برای اجرای کوئری‌ها
                cursor = db.cursor()

                # ساخت کوئری برای ایجاد تابع در پایگاه داده
                cursor.execute(F"SELECT GetAmountAccount({account_number})")
                result = cursor.fetchone()

        except mysql.connector.Error as error:
            print("خطا در اتصال به پایگاه داده MySQL:", error)
            return False

        finally:
            # بستن اتصال
            if db.is_connected():
                cursor.close()
                db.close()
                print("اتصال MySQL بسته شد.")

        return result[0]

    @staticmethod
    def insert_loan_and_payments(input_user_id: int, input_account_number: str, input_loan_amount: str):
        """
        completed
        محاسبه سود وام
        ایجاد وام
        ایجاد قسط های وام
        بصورت ترنس اکشن

        :param account_number:
        :return:
        موفقیت = 1
        نا موفق = 0
        """
        result = None
        db = None
        cursor = None
        try:
            # ایجاد اتصال به پایگاه داده
            db = DatabaseFactory.create_connection(host, database, db_username, db_password)

            # اگر اتصال برقرار بود
            if db.is_connected():
                # ایجاد یک cursor برای اجرای کوئری‌ها
                cursor = db.cursor()

                try:
                    cursor.callproc("InsertLoanAndPayments",
                                    [input_user_id, input_account_number, input_loan_amount])

                    for date in cursor.stored_results():
                        result = date.fetchone()
                    print(result)
                    db.commit()

                except mysql.connector.Error as error:
                    # Rollback تراکنش در صورت بروز خطا
                    db.rollback()

                    print("Error:", error)



        except mysql.connector.Error as error:
            print("خطا در اتصال به پایگاه داده MySQL:", error)
            return False

        finally:
            # بستن اتصال
            if db.is_connected():
                cursor.close()
                db.close()
                print("اتصال MySQL بسته شد.")

        return str(result[0])  # '1' or '0'

    @staticmethod
    def get_account_loans(input_account_number: str):
        """
        تمام وام های شماره حساب ورودی را بدست می آورد
        :param input_account_number:
        :return:
        یک جدول از وام های این حساب
        یک لیست که هر عضو آن یک تاپل هست
        """

        result = None
        db = None
        cursor = None
        try:
            # ایجاد اتصال به پایگاه داده
            db = DatabaseFactory.create_connection(host, database, db_username, db_password)

            # اگر اتصال برقرار بود
            if db.is_connected():
                # ایجاد یک cursor برای اجرای کوئری‌ها
                cursor = db.cursor()

                cursor.callproc("GetAccountLoans",
                                [input_account_number])

                for date in cursor.stored_results():
                    result = date.fetchall()


        except mysql.connector.Error as error:
            print("خطا در اتصال به پایگاه داده MySQL:", error)
            return False

        finally:
            # بستن اتصال
            if db.is_connected():
                cursor.close()
                db.close()
                print("اتصال MySQL بسته شد.")

        return result

    @staticmethod
    def get_loan_installments(loan_id_input: int):
        """
        تمام قسط های یک وام را بر میگرداند
        وروی هم ایدی یک وام را میگیرد
        :param loan_id_input:
        :return:
        یک لیست که هر عضو آن یک تاپل هست
        """

        result = None
        db = None
        cursor = None
        try:
            # ایجاد اتصال به پایگاه داده
            db = DatabaseFactory.create_connection(host, database, db_username, db_password)

            # اگر اتصال برقرار بود
            if db.is_connected():
                # ایجاد یک cursor برای اجرای کوئری‌ها
                cursor = db.cursor()

                try:
                    cursor.callproc("GetLoanInstallments",
                                    [loan_id_input])

                    for date in cursor.stored_results():
                        result = date.fetchall()
                    print(result)
                except mysql.connector.Error as error:

                    print("Error:", error)


        except mysql.connector.Error as error:
            print("خطا در اتصال به پایگاه داده MySQL:", error)
            return False

        finally:
            # بستن اتصال
            if db.is_connected():
                cursor.close()
                db.close()
                print("اتصال MySQL بسته شد.")

        return result

    @staticmethod
    def get_loan_payment_status(loan_id_input: int):
        """
        بدست آوردن مبلغ پرداخت شده و باقی ماند وام
        ورودی هم ایدی وام را میگیرد
        :param loan_id_input:
        :return:
        یک رکورد با دو ستون اولی مبلغ پرداخت شده و دومی مبلغ باقی مانده

        (0, total_loan_amount)
        یعنی هیچ قسطی پرداخت نشده
        """
        result = None
        db = None
        cursor = None
        try:
            # ایجاد اتصال به پایگاه داده
            db = DatabaseFactory.create_connection(host, database, db_username, db_password)

            # اگر اتصال برقرار بود
            if db.is_connected():
                # ایجاد یک cursor برای اجرای کوئری‌ها
                cursor = db.cursor()

                try:
                    cursor.callproc("GetLoanPaymentStatus",
                                    [loan_id_input])

                    for date in cursor.stored_results():
                        result = date.fetchone()

                except mysql.connector.Error as error:

                    print("Error:", error)


        except mysql.connector.Error as error:
            print("خطا در اتصال به پایگاه داده MySQL:", error)
            return False

        finally:
            # بستن اتصال
            if db.is_connected():
                cursor.close()
                db.close()
                print("اتصال MySQL بسته شد.")

        return result

    @staticmethod
    def pay_loan_installment(account_number_input: str, amount_to_pay: str, loan_id_input: int,
                             installment_id_input: int, transaction_id):
        """
        پرداخت قسط های وام
        ورودی:
        شماره حساب - مقدار قابل پرداخت - ایدی وام - ایدی قسط
        :param account_number_input:
        :param amount_to_pay:
        :param loan_id_input:
        :param installment_id_input:
        :return:
        خروجی
        0 یا 1
        """
        result = None
        db = None
        cursor = None
        try:
            # ایجاد اتصال به پایگاه داده
            db = DatabaseFactory.create_connection(host, database, db_username, db_password)

            # اگر اتصال برقرار بود
            if db.is_connected():
                # ایجاد یک cursor برای اجرای کوئری‌ها
                cursor = db.cursor()

                try:
                    cursor.callproc("PayLoanInstallment",
                                    [account_number_input, amount_to_pay, loan_id_input, installment_id_input,
                                     transaction_id])

                    for date in cursor.stored_results():
                        result = date.fetchone()

                        print(result)

                except mysql.connector.Error as error:

                    print("Error:", error)


        except mysql.connector.Error as error:
            print("خطا در اتصال به پایگاه داده MySQL:", error)
            return False

        finally:
            # بستن اتصال
            if db.is_connected():
                cursor.close()
                db.close()
                print("اتصال MySQL بسته شد.")

        return result

    @staticmethod
    def get_smallest_unpaid_installment(loan_id_input: int):
        """
        ایدی آخرین قسطی که باید پرداخت شود برگردانده می شود
        ورودی هم ایدی وام هست
        :param loan_id_input:
        :return:
        یک عدد خروجی هست
        """
        result = None
        db = None
        cursor = None
        try:
            # ایجاد اتصال به پایگاه داده
            db = DatabaseFactory.create_connection(host, database, db_username, db_password)

            # اگر اتصال برقرار بود
            if db.is_connected():
                # ایجاد یک cursor برای اجرای کوئری‌ها
                cursor = db.cursor()

                # ساخت کوئری برای ایجاد تابع در پایگاه داده
                cursor.execute(F"SELECT GetSmallestUnpaidInstallment({loan_id_input})")
                result = cursor.fetchone()

        except mysql.connector.Error as error:
            print("خطا در اتصال به پایگاه داده MySQL:", error)
            return False

        finally:
            # بستن اتصال
            if db.is_connected():
                cursor.close()
                db.close()
                print("اتصال MySQL بسته شد.")

        return result[0]

    @staticmethod
    def get_active_loan_id(account_number_input: str):
        """
        برای بررسی وجود وام فعال برای یک حساب
        ورودی : شماره حساب
        :param account_number_input:
        :return:
        خروجی: ایدی وام یا صفر
        """
        result = None
        db = None
        cursor = None
        try:
            # ایجاد اتصال به پایگاه داده
            db = DatabaseFactory.create_connection(host, database, db_username, db_password)

            # اگر اتصال برقرار بود
            if db.is_connected():
                # ایجاد یک cursor برای اجرای کوئری‌ها
                cursor = db.cursor()

                # ساخت کوئری برای ایجاد تابع در پایگاه داده
                cursor.execute(F"SELECT GetActiveLoanId({account_number_input})")
                result = cursor.fetchone()

        except mysql.connector.Error as error:
            print("خطا در اتصال به پایگاه داده MySQL:", error)
            return False

        finally:
            # بستن اتصال
            if db.is_connected():
                cursor.close()
                db.close()
                print("اتصال MySQL بسته شد.")

        return str(result[0])

    @staticmethod
    def generate_loan_proposals(input_loan_amount: str):
        """
        برای ایجاد وام های پیشنهادی هست. البته وام اصلی کاربر هم داخلش هیت و به عنوان اولین رکورد هست
        :param input_loan_amount:
        :return:
        [['600.00', '720.00', '60.00', '2024-02-02', '2025-02-02'],
         ['500.00', '600.00', '50.00', '2024-02-02', '2025-02-02']]
        """
        result = None
        db = None
        cursor = None
        try:
            # ایجاد اتصال به پایگاه داده
            db = DatabaseFactory.create_connection(host, database, db_username, db_password)

            # اگر اتصال برقرار بود
            if db.is_connected():
                # ایجاد یک cursor برای اجرای کوئری‌ها
                cursor = db.cursor()

                try:
                    cursor.callproc("GenerateLoanProposals",
                                    [input_loan_amount])

                    for date in cursor.stored_results():
                        result = date.fetchone()
                    print(result)
                except mysql.connector.Error as error:

                    print("Error:", error)


        except mysql.connector.Error as error:
            print("خطا در اتصال به پایگاه داده MySQL:", error)
            return False

        finally:
            # بستن اتصال
            if db.is_connected():
                cursor.close()
                db.close()
                print("اتصال MySQL بسته شد.")

        # تقسیم رشته بر اساس خطوط
        lines = result[0].split('\n')

        # فیلتر کردن خطوط با استفاده از شرط مورد نظر
        filtered_lines = filter(lambda line: line, lines)

        # تبدیل خطوط فیلتر شده به لیست
        result = [line.split() for line in filtered_lines]

        return result

    @staticmethod
    def get_min_balance_by_account_number(account_number: str):
        """
        پیدا کردن min موجودی 2 ماه اخیر
        :param account_number:
        :return:
        یک عدد
        """

        result = None
        db = None
        cursor = None
        try:
            # ایجاد اتصال به پایگاه داده
            db = DatabaseFactory.create_connection(host, database, db_username, db_password)

            # اگر اتصال برقرار بود
            if db.is_connected():
                # ایجاد یک cursor برای اجرای کوئری‌ها
                cursor = db.cursor()

                # ساخت کوئری برای ایجاد تابع در پایگاه داده
                cursor.execute(F"SELECT GetMinBalanceByAccountNumber({account_number})")
                result = cursor.fetchone()
                print(result)

        except mysql.connector.Error as error:
            print("خطا در اتصال به پایگاه داده MySQL:", error)
            return False

        finally:
            # بستن اتصال
            if db.is_connected():
                cursor.close()
                db.close()
                print("اتصال MySQL بسته شد.")

        return result[0]

    @staticmethod
    def change_loan_status(input_loan_amount: str):
        result = None
        db = None
        cursor = None
        try:
            # ایجاد اتصال به پایگاه داده
            db = DatabaseFactory.create_connection(host, database, db_username, db_password)

            # اگر اتصال برقرار بود
            if db.is_connected():
                # ایجاد یک cursor برای اجرای کوئری‌ها
                cursor = db.cursor()

                try:
                    cursor.callproc("ChangeLoanStatus",
                                    [input_loan_amount])

                    for date in cursor.stored_results():
                        result = date.fetchone()
                    print(result)
                except mysql.connector.Error as error:

                    print("Error:", error)


        except mysql.connector.Error as error:
            print("خطا در اتصال به پایگاه داده MySQL:", error)
            return False

        finally:
            # بستن اتصال
            if db.is_connected():
                cursor.close()
                db.close()
                print("اتصال MySQL بسته شد.")

        return result


# print(
#     ORM.create_transaction(source_account_number=12345678901234567891, destination_account_number=98765432101234567892,
#                            transfer_amount=600, description="Fake2"))
# print(ORM.insert_loan_and_payments(1, '77773333666633338888', "600.00"))
# print(ORM.get_account_loans('77773333666633338888'))
# print(ORM.get_loan_installments('3'))
# print(ORM.get_loan_payment_status('3'))
# print(ORM.pay_loan_installment('77773333666633338888','250.00', '3', '25'))
# print(ORM.pay_loan_installment('77773333666633338888', '20.00', 9, 97))
# print(ORM.generate_loan_proposals('1000.00'))
# print(ORM.get_min_balance_by_account_number('77773333666633338888'))
