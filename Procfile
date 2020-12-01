release: python manage.py migrate
web: gunicorn appointment_manager.wsgi --log-file -
worker: celery -A appointment_manager worker -l INFO
beatworker: celery -A appointment_manager beat -l INFO
