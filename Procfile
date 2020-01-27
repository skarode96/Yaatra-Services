release: python manage.py makemigrations API && python manage.py migrate
web: gunicorn service.wsgi --log-file -
