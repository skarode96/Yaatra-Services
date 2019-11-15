release: python ./backend/manage.py migrate
web: gunicorn ./backend/service.wsgi --log-file -
