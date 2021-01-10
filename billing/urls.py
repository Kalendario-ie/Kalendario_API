from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'stripe-connected-accounts', views.StripeViewSet, 'company-stripe')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'stripe/', views.stripe_hook, name='stripe-webhook'),
]
