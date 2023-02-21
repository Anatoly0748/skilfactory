rem cd C:\Users\Admin\PycharmProjects\newsportal06
python -m venv venv
venv\scripts\activate
cd project
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
celery -A project worker -l INFO --pool=solo
celery -A project beat -l INFO
celery -A project beat -l INFO --loglevel=debug
celery -A project worker --pool=solo --loglevel=debug
celery -A project purge
python manage.py shell
python manage.py runapscheduler
python manage.py createsuperuser

python -m pip install django
python -m pip install django-filter
python -m pip install django-allauth
python -m pip install django-apscheduler
python -m pip uninstall celery
python -m pip install django-celery-beat
python -m pip install redis
python -m pip install -U "celery[redis]"
python -m pip install gevent
python -m pip install eventlet

rem django-admin startproject NewsPortal
cd project
python manage.py startapp news
python manage.py startapp sign
python manage.py startapp protect