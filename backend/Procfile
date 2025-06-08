release: python manage.py migrate
web: gunicorn kalendario.wsgi --log-file -
worker: celery -A kalendario worker -l INFO
beatworker: celery -A kalendario beat -l INFO
