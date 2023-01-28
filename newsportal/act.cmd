python -m venv venv
venv\scripts\activate
pip install django
django-admin startproject NewsPortal
cd NewsPortal
python manage.py startapp news
python manage.py makemigrations
python manage.py migrate
python manage.py shell
python manage.py runserver
cd ..\