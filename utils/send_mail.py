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
