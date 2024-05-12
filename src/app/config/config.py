from decouple import config

APP_DATABASE_LINK = config("APP_DATABASE_LINK")
MODERATOR_KEY = config("MODERATOR_KEY")
ALGORITHM = "HS256"
PROJECT_NAME = "Sportacus"

JWT_SECRET_KEY = config("JWT_SECRET_KEY")

REVIEW = "REVIEW"
PLACE = "PLACE"

MAIL_FROM = config("MAIL_FROM")
MAIL_SERVER = config("MAIL_SERVER")
MAIL_PORT = config("MAIL_PORT")
MAIL_USERNAME = config("MAIL_USERNAME")
MAIL_PASSWORD = config("MAIL_PASSWORD")

VERIFY_ENDPOINT = config("VERIFY_ENDPOINT")

VERIFICATION_CODE_HTML = open("src/app/templates/verification_code.html", encoding='utf-8').read()
UPDATE_PASSWORD_HTML = open("src/app/templates/update_password.html", encoding='utf-8').read()

USER_PHOTO_PATH = "src/app/assets/user.jpg"

PLACES_FILTERS = (
    "турники", "брусья", "велотренажер", "шагомер",
    "степпер", "маятник", "лыжный тренажер", "твистер", "беговые дорожки", 
    "баскетбольное кольцо", "теннисный стол", "площадка для большого тенниса",
    "футбольные ворота", "хоккейный корт", "жим сидя от груди",
    "жим ногами", "гребля", "сгибание ног", "волейбольная сетка",
    "вертикальная тяга", "гиперэкстензия", "лыжная трасса", "каток"
)

PLACE_CATEGORIES = (
    "уличные тренажеры", "спортивные игры",
    "воркаут", "бег", "зимние виды спорта",
)
