# Description #

Project for reading and creating news and comments with authentication

### Stack ###

- python3.11, Django - backend
- Postgres - database

## Features ##

1. Authentication (rayapp/accounts)
    - django authentication
    - profile update
2. Main logic (rayapp/news)
    - full CRUD with filters and soring for news and comments
    - permissions are correctly configured to read/update/delete for all entities
3. Tests for whole CRUD of news and accounts apps (in tests.py files)
4. PyMemcacheCache is used for caching
5. django_cron is used for periodic tasks (db backup and API downloading)
6. asyncio is used for downloading data from API

## How to: ##

## Development local configuration ##

1) Create venv
    - `python -m venv venv`
2) Install dependencies
    - `pip install -r requirements.txt`
3) Run docker container for postgres
    - `docker-compose -f docker-compose.db.yaml up -d`
4) Make migrations
    - `manage.py makemigrations`
    - `manage.py migrate`
5) Run server
    - `manage.py runserver`
6) Createsuperuser
    - `manage.py createsuperuser`
7) Connect to admin panel at http://127.0.0.1:8000/admin/
8) Run tests from main folder
    - `python manage.py test`

## Development local configuration with docker-compose ##

1) Use docker-compose.dev.yaml from within deploy folder
    - `docker-compose -f docker-compose.yaml up -d`
2) The following would be done:
    - postgresql container would start
    - migrations would apply
    - api container would start
    - static files would be collected
    - news would be downloaded from API
    - superuser with credentials: "admin", "admin" would be created

## Project links

1) Admin - http://localhost:8000/admin
2) Swagger - http://localhost:8000/api/schema/swagger-ui
3) Postman - https://www.postman.com/universal-crater-955516/workspace/rayapp/overview