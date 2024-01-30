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
