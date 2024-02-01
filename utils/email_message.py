from khayyam import JalaliDatetime


class EmailNotification:

    @staticmethod
    def login_message():
        current_time = JalaliDatetime.now().strftime("%Y-%m-%d %H:%M:%S")  # تاریخ و زمان حال به فرمت مناسب
        message = """
            <div dir="rtl" style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #333333; text-align: center;">ورود به حساب کاربری</h2>
                <hr style="border: 0; border-top: 1px solid #eee;">
                <p style="color: #666666; font-size: 16px;">کاربر گرامی، شما به اکانت خود وارد شده اید</p>
                <p style="color: #666666; font-size: 16px;">زمان ورود شما: <span style="color: #0066cc;">{login_time}</span></p>
            </div>
        """.format(login_time=current_time)

        return message

    @staticmethod
    def secondary_password(password: int):
        current_time = JalaliDatetime.now().strftime("%Y-%m-%d %H:%M:%S")  # تاریخ و زمان حال به فرمت مناسب
        message = f"""
            <div dir="rtl" style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #333333; text-align: center;">{password}: رمز دوم</h2>
                <hr style="border: 0; border-top: 1px solid #eee;">
                <p style="color: #666666; font-size: 16px; text-align: center;">کاربر گرامی، رمز دوم تا دو دقیقه بعد بیشتر اعتبار ندارد</p>
                <p style="color: #666666; font-size: 16px; text-align: center;">زمان: <span style="color: #0066cc;">{current_time}</span></p>
            </div>
        """

        return message
