from django.urls import path, include
from rest_framework import routers
from . import views, webhooks

router = routers.DefaultRouter()
router.register(r'stripe-connected-accounts', views.StripeViewSet, 'company-stripe')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'stripe/hook', webhooks.stripe_hook, name='stripe-webhook'),
]
