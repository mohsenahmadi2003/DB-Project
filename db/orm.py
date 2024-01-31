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

print(ORM.calculate_account_balance_with_date("12345678901234567891", '2027-01-05 00:00:00', '2025-05-05 00:00:00'))
