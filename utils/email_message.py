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
    def secondary_password(password):
        current_time = JalaliDatetime.now().strftime("%Y-%m-%d %H:%M:%S")  # تاریخ و زمان حال به فرمت مناسب
        message = f"""
            <div dir="rtl" style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #333333; text-align: center;">{password}: رمز دوم</h2>
                <hr style="border: 0; border-top: 1px solid #eee;">
                <p style="color: #666666; font-size: 16px; text-align: center;">کاربر گرامی، رمز دوم تا یک دقیقه بعد بیشتر اعتبار ندارد</p>
                <p style="color: #666666; font-size: 16px; text-align: center;">زمان: <span style="color: #0066cc;">{current_time}</span></p>
            </div>
        """

        return message

    @staticmethod
    def deposite(amount: str, deposite_amount: str, account_number: str):
        current_time = JalaliDatetime.now().strftime("%Y-%m-%d %H:%M:%S")  # تاریخ و زمان حال به فرمت مناسب
        message = f"""
            <div dir="rtl" style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #333333; text-align: center;">بانک</h2>
                <hr style="border: 0; border-top: 1px solid #eee;">
                <p style="color: #666666; font-size: 16px;">کارت</p>
                <p style="color: #666666; font-size: 16px;">واریز به {account_number}</p>
                <p style="color: #666666; font-size: 16px;">مبلغ {deposite_amount}</p>
                <p style="color: #666666; font-size: 16px;">موجودی {amount}</p>
                <p style="color: #666666; font-size: 16px;">زمان تراکنش: <span style="color: #0066cc;">{current_time}</span></p>
            </div>
        """

        return message

    @staticmethod
    def withdraw(amount: str, withdraw_amount: str, account_number: str):
        current_time = JalaliDatetime.now().strftime("%Y-%m-%d %H:%M:%S")  # تاریخ و زمان حال به فرمت مناسب
        message = f"""
            <div dir="rtl" style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #333333; text-align: center;">بانک</h2>
                <hr style="border: 0; border-top: 1px solid #eee;">
                <p style="color: #666666; font-size: 16px;">کارت</p>
                <p style="color: #666666; font-size: 16px;">برداشت از {account_number}</p>
                <p style="color: #666666; font-size: 16px;">مبلغ {withdraw_amount}</p>
                <p style="color: #666666; font-size: 16px;">موجودی {amount}</p>
                <p style="color: #666666; font-size: 16px;">زمان تراکنش: <span style="color: #0066cc;">{current_time}</span></p>
            </div>
        """

        return message
