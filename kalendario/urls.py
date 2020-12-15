from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        TemplateView.as_view(template_name="home.html"),
        name='password_reset_confirm'),

    path(r'account-confirm-email/', TemplateView.as_view(template_name='home.html'),
         name='account_email_verification_sent'),

    path('admin/', admin.site.urls),
    path('api/auth/', include('app_auth.urls')),
    path('api/admin/', include('scheduling.urls')),
    path('api/core/', include('core.urls')),
    path('api/', include('customers.urls')),
    path('webhooks/', include('webhooks.urls')),
    url(r'^.*', TemplateView.as_view(template_name='home.html'), name="home"),

    url(r'^account-confirm-email/(?P<key>[-:\w]+)/$', TemplateView.as_view(template_name='home.html'),
        name='account_confirm_email'),
]
