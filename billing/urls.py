from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'accounts', views.AccountViewSet, 'billing-account')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'stripe/', views.stripe_hook, name='stripe-webhook'),
    path(r'payment/', views.get_payment_intent, name='stripe-webhook'),
]
