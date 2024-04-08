# Backend
Backend-server for Spartacus. [Documentation for use](https://petite-keeper-162.notion.site/Backend-69daae844b2d4c5987755d83ffc4c662?pvs=4)
## For running
### If you use poetry
```
poetry install 
poetry run uvicorn src.app.app:app
```
### Else if you use pip
```
pip install -r requirements.txt
uvicorn src.app.app:app
```


### ENV 
```
APP_DATABASE_LINK="mongodb_link"
MODERATOR_KEY="MODERATOR_KEY"
JWT_SECRET_KEY="SECRET KEY"

MAIL_FROM="example@mail.com"
MAIL_SERVER="smtp.mail.com"
MAIL_PORT="465"
MAIL_USERNAME="example@mail.com"
MAIL_PASSWORD="password"

VERIFY_ENDPOINT="https://site/verify_email/"
```
