from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_auth.urls')),
    path('api/auth/registration/', include('rest_auth.registration.urls')),
    path(r'account-confirm-email/', TemplateView.as_view(template_name='home.html'),
         name='account_email_verification_sent'),
    path('account-confirm-email/<str:key>/', TemplateView.as_view(template_name='home.html'),
         name='account_confirm_email'),
    path('api/accounts/', include('allauth.urls')),
    path('api/', include('customers.urls')),
    path('api/admin/', include('scheduling.urls')),
    path('api/core/', include('core.urls')),
    path('api/social/', include('social_providers.urls')),
    path('webhooks/', include('webhooks.urls')),
    url(r'^ngsw-worker.js', (TemplateView.as_view(
        template_name="ngsw-worker.js",
        content_type='application/javascript',
    )), name='ngsw-worker.js'),
    url(r'^.*', TemplateView.as_view(template_name="home.html"), name="home"),
]
