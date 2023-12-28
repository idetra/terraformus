# Terra Formus
## Collaborative tool to form an ABCS (Abundance Based Circular System)

### Establish blueprints with sustainable operation and upscale

The platform internalizes concepts such as UN's 17 sustainable development goals (SDGs), cradle-to-cradle, 
circular economy, life cycle assessment (LCA) and zero waste to establish premises for proposed blueprints, locking how 
solutions are implemented, processed, expanded, upgraded and discarded.

### Characteristics
- Django web application
- Nginx for web load balancing
- Docker

# Development setup
## Requirements
### Install in your computer (if not already installed)
- pyhon >= 3.9 https://www.python.org/downloads/
- Docker https://docs.docker.com/engine/install/
- Git https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
- PostgresQL https://www.postgresql.org/download/
  - Alternatively, manage postgres with pgAdmin4 https://www.pgadmin.org/download/
- If you delete the variable DATABASE_URL from .env, you can ignore all steps below related to PostgresQL
    - This will make the application use SQLite3 instead of PostgresQL - ONLY USE THIS FOR LOCAL DEVELOPMENT
- If you want to use Postgres:
  - Create a database with a user that has admin access to it.
  - These credentials will go into the .env file (see below)
- core_data.json fixture file containing base and sensitive initial data (ask admin for it)

## Clone repository and setup local environment
*IMPORTANT: Adjust `python` commands to `python3` if necessary*
- Clone this repo
- copy .env file to project folder (main project folder)
- Change the SECRET_KEY variable on .env file
  - You can generate a Django secret key here: https://djecrety.ir/
- insert core_data.json fixture file into app_name>app_name>core>fixtures folder (create if necessary)
- Insert postgresql credentials on .env file (DB_USER and DB_PASSWORD)
- Optional: open project on your IDE of choice (VSCode, Pycharm, etc.)

## Run application
### Option 1: Run the application using virtual environment:
on project folder:

- create virtual environment with python `python -m venv .venv`
- activate .venv `source .venv/bin/activate` (for windows: `.\.venv\Scripts\activate`)
- upgrade pip `python -m pip install --upgrade pip`
- install dependencies `pip install -r requirements-dev.txt`

on the same folder of manage.py file:

- run migrate `python manage.py migrate`
- create superuser `python manage.py createsuperuser`
- load minimal data from fixtures `python manage.py loaddata ./terraformus/core/fixtures/core_data.json`
- run collect static `python manage.py collectstatic`
- run tests `pytest`
- run server `python manage.py runserver`
- go to http://localhost:8000/ on your browser to access the application

### Option 2: Run the application using Docker:
- change DB_HOST variable on .env from `localhost` to `host.docker.internal`

on the same folder of docker-compose.yml file:

- start docker app on your machine
- create the tables in the database `docker-compose run web python manage.py migrate`
- build and spin up the application: `docker-compose up --build`
- stop the application: `Ctrl + C`
- create superuser: `docker-compose run web python manage.py createsuperuser`
- load minimal data from fixtures: `docker-compose run web python manage.py loaddata terraformus/core/fixtures/core_data.json`
- collect static files (css/js): `docker-compose run web python manage.py collectstatic`
- run tests `docker-compose run web pytest`
- go to http://localhost/ on your browser to access the application
- to shut down application: `docker-compose down`

# Development
*IMPORTANT: Adjust python/Django commands with `docker-compose run web` at their start if using Docker*

## Before development
1. activate .venv on terminal under app folder unless using Docker `source .venv/bin/activate` (for windows: `.\.venv\Scripts\activate`)
2. verify branch and changes `git status`
3. pull all new deployed changes `git pull`
4. run migrate `python manage.py migrate`
5. run tests `pytest`
6. checkout into working branch `git checkout branch_name` or create and checkout into new one `git checkout -b new_branch`

## After development
1. run makemigrations `python manage.py makemigrations` (NEVER run this on server side)
2. run migrate `python manage.py migrate`
3. create / update tests
4. insert new installed libraries into requirements.txt manually (don't use `pip freeze > requirements.txt`)
5. verify branch and changes `git status`
6. update .gitignore if necessary
7. update README.md and CHANGELOG.md if necessary
8. stage changes `git add .`
9. verify changes `git status`
10. commit changes `git commit -m "short description of changes made"`
11. verify commit `git status`
12. push branch `git push` (if this is a new branch, `git push –set-upstream origin new_branch`)
13. open a pull request on GitHub
14. Delete branch once merged with main
