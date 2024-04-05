from email.mime.text import MIMEText
from smtplib import SMTP_SSL

from jinja2 import Template

from src.app.config.config import (
    MAIL_FROM, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
)

verificationCode = Template(open("src/app/email/templates/verification_code.html").read())
updatePassword = Template(open("src/app/email/templates/update_password.html").read())

class EmailSender:
    @staticmethod
    def send(email: str, subject: str, html_template) -> None:
        msg = MIMEText(html_template, "html")
        msg['Subject'] = subject
        msg['From'] = f'Sportacus <{MAIL_FROM}>'
        msg['To'] = email

        server = SMTP_SSL(MAIL_SERVER, MAIL_PORT)
        server.login(MAIL_USERNAME, MAIL_PASSWORD)

        # Send the email
        server.send_message(msg)
        server.quit()
    
    @staticmethod
    def send_verification_code(email: str, code: int) -> None:
        verificationCodeHTML = verificationCode.render(code=code)

        EmailSender.send(
            email, f"Код подтверждения для email: {code}", verificationCodeHTML    
        )

    @staticmethod
    def send_update_password(email, password_link) -> None:
        updatePasswordHTML = updatePassword.render(password_link=password_link)

        EmailSender.send(
            email, "Ссылка на изменение пароля", updatePasswordHTML
        )