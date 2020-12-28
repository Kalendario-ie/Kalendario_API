from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth.models import Permission

from scheduling.models import Person


class MyAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit)
        # if not user.person:
        #     person = Person(user=user, email=user.email, first_name=user.first_name, last_name=user.last_name)
        #     person.save()
        #     user.person_id = person.id
        user.user_permissions.add(Permission.objects.filter(codename='add_company').first())
        user.save()
        return user

    def send_mail(self, template_prefix, email, context):
        msg = self.render_mail(template_prefix, email, context)
        msg.send(fail_silently=True)

