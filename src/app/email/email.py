from aiosmtplib import SMTP
from email.mime.text import MIMEText
from jinja2 import Template


from src.app.config.config import (
    MAIL_FROM, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD,
    VERIFICATION_CODE_HTML, UPDATE_PASSWORD_HTML
)

verificationCode = Template(VERIFICATION_CODE_HTML, enable_async=True)
updatePassword = Template(UPDATE_PASSWORD_HTML, enable_async=True)

class EmailSender:
    client = SMTP(hostname=MAIL_SERVER, port=MAIL_PORT, use_tls=True, validate_certs=False, username=MAIL_USERNAME, password=MAIL_PASSWORD)

    @staticmethod
    async def send(email: str, subject: str, html_template) -> None:
        msg = MIMEText(html_template, "html")
        msg['Subject'] = subject
        msg['From'] = f'Sportacus <{MAIL_FROM}>'
        msg['To'] = email

        async with EmailSender.client:
            await EmailSender.client.send_message(msg)

    @staticmethod  
    async def send_verification_code(email: str, code: int) -> None:
        verificationCodeHTML = await verificationCode.render_async(code=code)

        await EmailSender.send(
            email, f"Код подтверждения для email: {code}", verificationCodeHTML    
        )

    @staticmethod
    async def send_update_password(email: str, password_link: str) -> None:
        updatePasswordHTML = await updatePassword.render_async(password_link=password_link)

        await EmailSender.send(
            email, "Ссылка на изменение пароля", updatePasswordHTML
        )