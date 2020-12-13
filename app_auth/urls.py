from django.urls import path, include
from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', include('rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),

    path(r'accounts/', views.views.SocialAccountListView.as_view(), name='social_account_list'),
    path(r'facebook/', views.FacebookLogin.as_view(), name='fb_login'),
    path(r'facebook/connect/', views.FacebookConnect.as_view(), name='fb_connect'),
]
