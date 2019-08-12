from django.contrib import admin
from core.models import User


class UserAdmin(admin.ModelAdmin):
    fieldset = [
        (None, {'fields': ['email']}),
    ]


admin.site.register(User, UserAdmin)
