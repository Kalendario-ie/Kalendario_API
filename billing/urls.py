from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'accounts', views.AccountViewSet, 'billing-account')
router.register(r'payment', views.PaymentIntentView, 'payment')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'connected-account-hooks/', views.ConnectedAccountHookView.as_view(), name='connected-webhook'),
    path(r'account-hooks/', views.AccountHookView.as_view(), name='account-webhook'),
]
