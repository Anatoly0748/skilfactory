cd C:\Users\Admin\PycharmProjects\newsportal
rem python -m pip install django
python -m venv venv
venv\scripts\activate
rem pip install django
rem django-admin startproject NewsPortal
cd project
rem python manage.py createsuperuser
rem python manage.py startapp news
python manage.py makemigrations
python manage.py migrate
python manage.py shell
python manage.py runserver
cd ..\