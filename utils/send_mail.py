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
