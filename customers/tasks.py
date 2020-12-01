from celery import shared_task
from appointment_manager.common.mail import send_mail


@shared_task
def send_test_mail():
    send_mail('celery mail', 'did this work', ['gustavo.francelino@gmail.com'], True)
