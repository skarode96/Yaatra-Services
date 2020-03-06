# coding=utf-8
from django.conf import settings
from datetime import datetime
import socket, os


def test_connection_to_db(database_name):
    try:
        db_definition = getattr(settings, 'DATABASES')[database_name]
        s = socket.create_connection((db_definition['HOST'], db_definition['PORT']), 5)
        s.close()
        return True
    except Exception as e:
        return False


def available_db():
    with open(os.path.dirname(__file__) + '/dbha_last_check.txt', 'r') as f:
        f = f.read().splitlines()
        dbha_last_check = datetime.strptime(f[0], '%Y-%m-%d %H:%M:%S')
        last_db = f[1]
    if (datetime.now() - dbha_last_check).seconds > 10:
        lines_of_text = ""
        db = ""
        if  (test_connection_to_db(str(last_db))):
            db = str(last_db)
            lines_of_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n" + db
        if test_connection_to_db('default'):
            lines_of_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n" + 'default'
        elif test_connection_to_db('failover1'):
            db = 'failover1'
            lines_of_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n" + db
        elif test_connection_to_db('failover2'):
            db = 'failover2'
            lines_of_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n" + db
        else:
            db = last_db
            lines_of_text = str(dbha_last_check) + "\n" + db

        with open(os.path.dirname(__file__) + '/dbha_last_check.txt', 'w') as status_file:
            status_file.write(lines_of_text)
            status_file.close()

        return db

    return last_db
