from decouple import config


APP_DATABASE_LINK = config("APP_DATABASE_LINK")
MODERATOR_KEY = config("MODERATOR_KEY")
PROJECT_NAME="Sportacus"

REVIEW = "REVIEW"
PLACE = "PLACE"

MAIL_FROM = config("MAIL_FROM")
MAIL_SERVER = config("MAIL_SERVER")
MAIL_PORT = config("MAIL_PORT")
MAIL_USERNAME = config("MAIL_USERNAME")
MAIL_PASSWORD = config("MAIL_PASSWORD")

VERIFY_ENDPOINT = config("VERIFY_ENDPOINT")

VERIFICATION_CODE_HTML = open("src/app/templates/verification_code.html").read()
UPDATE_PASSWORD_HTML = open("src/app/templates/update_password.html").read()