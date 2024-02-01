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
    def cancel_transaction(transaction_id: int):
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
                                    [transaction_id])

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

# print(
#     ORM.create_transaction(source_account_number=12345678901234567891, destination_account_number=98765432101234567892,
#                            transfer_amount=600, description="Fake2"))
# print(ORM.get_amount_account(account_number='12345678901234567891'))
