cd C:\Users\Admin\PycharmProjects\newsportal05
rem python -m pip install django
python -m venv venv
venv\scripts\activate
rem pip install django
rem django-admin startproject NewsPortal
rem cd project
rem python manage.py createsuperuser
rem python manage.py startapp news
cd project
python manage.py startapp sign
python manage.py startapp protect
python manage.py makemigrations
python manage.py migrate
python manage.py shell
python -m pip install django-filter
python -m pip install django-allauth
python -m pip install django-apscheduler
python manage.py runserver
python manage.py runapscheduler
cd ..\