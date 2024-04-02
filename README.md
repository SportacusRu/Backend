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
APP_DATABASE_LINK = "mongodb_link"
MODERATOR_KEY = "MODERATOR KEY"
```
