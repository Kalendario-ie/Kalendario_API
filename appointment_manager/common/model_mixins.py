from django.db import models


class CleanSaveMixin:
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.clean()
        models.Model.save(self, force_insert, force_update, using, update_fields)
