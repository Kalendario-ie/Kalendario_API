from django.views.generic import RedirectView


class PasswordResetRedirect(RedirectView):
    def get_redirect_url(self, uidb64, token, *args, **kwargs):
        base_url = super().get_redirect_url(*args, **kwargs)
        return base_url + f'password-reset/confirm/{uidb64}/{token}'


class AccountConfirmRedirect(RedirectView):
    def get_redirect_url(self, key, *args, **kwargs):
        base_url = super().get_redirect_url(*args, **kwargs)
        return base_url + f'account-confirm-email/{key}/'
