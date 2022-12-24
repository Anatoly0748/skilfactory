cd C:\Users\Admin\PycharmProjects
python -m venv flatpages
flatpages\scripts\activate
cd  project_dir\project
python manage.py migrate
python manage.py runserver
