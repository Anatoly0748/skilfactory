cd C:\Users\Admin\PycharmProjects\Bulletinboard
python -m venv venv
venv\scripts\activate
cd project
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
python manage.py runserver
celery -A project worker -l INFO --pool=solo
celery -A project beat -l INFO
celery -A project purge
python manage.py shell
python manage.py runapscheduler
python manage.py createsuperuser
python manage.py changepassword admin
python manage.py collectstatic
python manage.py dumpdata --format=json > mydata.json
python manage.py dumpdata --format=xml > mydata.xml
python manage.py loaddata mydata.json
python manage.py dumpdata --format=xml sample_app > sampledata.xml
rem python manage.py flush
python manage.py  delpost Тема4
python manage.py makemessages -l ru
python manage.py compilemessages
python manage.py update_translation_fields

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
python -m pip install flake8
python -m pip install psycopg2-binary
python -m pip install django-modeltranslation
flake8 --exclude venv
python -m pip install django-richtextfield
rem django-admin startproject NewsPortal
cd project
python manage.py check --deploy
python manage.py startapp news
python manage.py startapp sign
python manage.py startapp protect