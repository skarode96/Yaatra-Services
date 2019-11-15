release: python ./backend/manage.py migrate
web: gunicorn --chdir backend/ service.wsgi --log-file -
