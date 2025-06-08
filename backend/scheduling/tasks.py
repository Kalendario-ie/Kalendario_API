from celery import shared_task
from .models import Request

@shared_task
def delete_idle_requests():
    requests = Request.objects.get_idle()
    print(len(requests), 'requests to be deleted')
    for request in requests:
        print('deleting request', request.id)
        request.delete()
