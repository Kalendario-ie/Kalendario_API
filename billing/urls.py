from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'accounts', views.AccountViewSet, 'billing-account')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'connected-account-hooks/', views.ConnectedAccountHookView.as_view(), name='connected-webhook'),
    path(r'account-hooks/', views.AccountHookView.as_view(), name='account-webhook'),
    path(r'payment/', views.payment_intent, name='stripe-payment'),
]
