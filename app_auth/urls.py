from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('rest_auth.registration.urls')),
    path("email/", views.ResendEmail.as_view(), name="account_email"),
    path(r'accounts/', views.views.SocialAccountListView.as_view(), name='social_account_list'),
    path(r'facebook/', views.FacebookLogin.as_view(), name='fb_login'),
    path(r'facebook/connect/', views.FacebookConnect.as_view(), name='fb_connect'),
]
