import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import configparser
import os


class EmailSender:
    def __init__(self):
        self.BASEDIR = os.path.dirname(os.path.abspath(__file__))
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(self.BASEDIR, 'mail.ini'))
        self.smtp_server = str(self.config.get('email', 'smtpServer'))
        self.port = int(self.config.get('email', 'port'))
        self.sender_email = str(self.config.get('email', 'senderEmail'))
        self.password = str(self.config.get('email', 'password'))
        self.context = ssl.create_default_context()
        self.server = None

    def connect_email(self):
        try:
            print("Connecting mail")
            self.server = smtplib.SMTP(self.smtp_server, self.port)
            self.server.starttls(context=self.context)
            self.server.login(self.sender_email, self.password)
            return True
        except Exception as e:
            print(f"Error in connecting mail: {e}")
            return False

    def send_mail(self, receiver, subject="", html_body=""):
        try:
            if not self.server or self.server.noop()[0] != 250:
                print("Mail server disconnected. Reconnecting.")
                self.connect_email()
            else:
                logging.info(f"Mail server already connected: {self.server.noop()[0]}")

            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg["To"] = receiver

            part1 = MIMEText(html_body, 'html')
            msg.attach(part1)

            self.server.sendmail(self.sender_email, receiver, msg.as_string())
            print(f"Email sent successfully to {receiver} with subject: {subject}")
        except Exception as e:
            logging.info(f"Error in sending mail. Error message: {e}")

    def close_connection(self):
        if self.server:
            self.server.quit()


# Example usage:

# email_sender = EmailSender()
# email_sender.connect_email()
#
# receiver_email = "ahmadimohsen138262@gmail.com"
# email_subject = "Temp Subject"
# email_html_body = """
#     <div dir="rtl">
#     <h2>فعالسازی حساب کاربری</h2>
#     <hr>
#     <p>کاربر گرامی ، جهت فعالسازی حساب کاربری خود روی لینک زیر کلیک کنید</p>
#     <p>
#         <a href="https://howsam.org/">فعالسازی
#             حساب کاربری</a>
#     </p>
#     </div>
#     """
#
# email_sender.send_mail(receiver_email, email_subject, email_html_body)
# email_sender.close_connection()

