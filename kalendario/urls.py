from django.urls import path, include
from django.conf.urls import url
from django.views.generic import RedirectView
from django.conf import settings

from kalendario.views import PasswordResetRedirect, AccountConfirmRedirect

SPA_URL = getattr(settings, 'SPA_BASE_URL', '')

urlpatterns = [
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetRedirect.as_view(url=SPA_URL),
        name='password_reset_confirm'),

    url(r'account-confirm-email/', RedirectView.as_view(url=SPA_URL + 'account-confirm-email/'),
        name='account_email_verification_sent'),

    path('api/auth/', include('app_auth.urls')),
    path('api/admin/', include('scheduling.urls')),
    path('api/billing/', include('billing.urls')),
    path('api/core/', include('core.urls')),
    path('api/', include('customers.urls')),
    url(r'^.*', RedirectView.as_view(url=SPA_URL), name='go-to-spa'),

    url(r'^account-confirm-email/(?P<key>[-:\w]+)/$',
        AccountConfirmRedirect.as_view(url=SPA_URL),
        name='account_confirm_email'),
]
