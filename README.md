# Django Quickstart

(Original script @ https://github.com/henriquebastos/django-quickstart )

Adjusted to better fit my own initial setup

This template includes:

- Easy settings setup with <a href="https://github.com/henriquebastos/python-decouple">Decouple</a>
- Support to pytest and pytest-django
- Use of URL's to manage database access
- Static assets serving with dj-static with a WSGI server
- <a href="https://django-jazzmin.readthedocs.io/">Jazzmin</a> for django admin template
- <a href="https://django-extensions.readthedocs.io/en/latest/">Django extensions</a> for the cool `python manage.py shell_plus` environment 

## One liner:

0. Before doing anything, install and login into <a href="https://devcenter.heroku.com/articles/heroku-cli">heroku-cli</a>
1. Copy and paste the code below in your terminal
2. Hit 'Enter'
3. Type in your project's name (no spaces or funny chars)
4. Hit 'Enter'


```
read PROJECT_NAME && \
mkdir $PROJECT_NAME && \
cd $PROJECT_NAME && \
python3 -m venv .venv && \
source .venv/bin/activate && \
python3 -m pip install --upgrade pip && \
python3 -m pip install django && \
django-admin startproject --template https://github.com/GuiFV/django-quickstart/archive/master.zip --name=Procfile,.env,pytest.ini $PROJECT_NAME . && \
pip3 install --prefer-binary -r requirements-dev.txt && \
git init && \
git add . && \
git commit -m 'Initial import' && \
heroku create $PROJECT_NAME && \
heroku config:set DEBUG=True SECRET_KEY=`cat .env | grep SECRET_KEY | cut -d = -f 2` ALLOWED_HOSTS=".herokuapp.com" && \
git push heroku master
```
## Afterwards:

5. Don't forget to change the SECRET_KEY for something more secure both in .env locally and on heroku ( `heroku config:set SECRET_KEY='secret_key_here'` )
6. Create a repo
7. Set it up locally using `git remote add origin https://github.com/YOURNAME/REPO_CREATED/`


