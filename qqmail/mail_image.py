from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
import os

try:
    from config import *
except ImportError:
    from .config import *


def mail_image(img_path):
    message = MIMEMultipart()
    mail_body = MIMEText('Test-Image，\n附件的邮件。', 'plain', 'utf-8')
    message.attach(mail_body)
    message['Subject'] = Header('Sub-Test-Head', 'utf-8')  # 主题
    message['From'] = Header(from_title, 'utf-8')
    message['To'] = Header(to_title, 'utf-8')
    baseName = os.path.basename(img_path)
    att = MIMEApplication(open(img_path, 'rb').read())
    att.add_header('Content-Disposition', 'attachment', filename=baseName)
    message.attach(att)
    try:
        smtpObj = smtplib.SMTP_SSL("smtp.qq.com", 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(from_address, to_address, message.as_string())
        smtpObj.quit()
        print("发送邮件成功")
    except smtplib.SMTPException:
        print("Error: 发送邮件失败")


if __name__ == '__main__':
    img_path = '_image/test_image.png'
    mail_image(img_path)
