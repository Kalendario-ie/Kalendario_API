from django.conf.urls import url

from webhooks import views

urlpatterns = [
    url(r'^stripe/', views.my_webhook_view, name='stripe-webhook'),
]
