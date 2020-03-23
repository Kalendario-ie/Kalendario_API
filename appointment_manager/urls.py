from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_auth.urls')),
    path('api/auth/registration/', include('rest_auth.registration.urls')),
    url(r'^account-confirm-email/(?P<key>[-:\w]+)/$', TemplateView.as_view(),
        name='account_confirm_email'),
    # path('api/accounts/', include('allauth.urls')),
    path('api/', include('core.urls')),
    path('api/', include('scheduling.urls')),
    url(r'^.*', TemplateView.as_view(template_name="home.html"), name="home")
]
