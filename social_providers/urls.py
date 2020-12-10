from django.urls import path
from . import views

urlpatterns = [
    path(r'facebook/', views.FacebookLogin.as_view(), name='fb_login'),
    path(r'facebook/connect/', views.FacebookConnect.as_view(), name='fb_connect'),
]
