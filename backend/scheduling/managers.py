import datetime
from django.core.exceptions import ValidationError
from django.db import models
from safedelete.models import SafeDeleteManager
from django.db.models import Q


class AppointmentManager(SafeDeleteManager):
    def create(self, ignore_availability=False, **kwargs):
        start = kwargs['start'] = kwargs['start'].replace(second=0, microsecond=0)

        if start <= datetime.datetime.now():
            raise ValidationError('Date can\'t be on the past')

        obj = self.model(**kwargs)
        self._for_write = True
        obj.save(force_insert=True, ignore_availability=ignore_availability, using=self.db)
        return obj

    def accepted(self):
        return self.get_queryset().filter(status='A')

    def requests(self):
        return self.get_queryset().filter(status='P')

    def active(self):
        return self.get_queryset().filter(~Q(status='R'))

    def overlapping(self, start, end, exclude_id=None, **kwargs):
        """
        Given a start and end date this method will appointments that overlaps with the date range
        - appointments that have their start date between this range
        - appointments that have their end date between this range
        - Appointments that have their start before this start and end after the end
        """
        query = self.active().filter(Q(start__gte=start, start__lt=end) |  # starts between
                                     Q(end__gt=start, end__lte=end) |  # ends between
                                     Q(start__lte=start, end__gte=end))  # starts before and ends after
        if exclude_id:
            query = query.filter(~Q(id=exclude_id))
        return query.filter(**kwargs)


class RequestManager(models.Manager):
    def get_current(self, owner_id, user_id):
        """
        returns the first request that's not complete from the database or create a new request
        """
        current = self.get_queryset().filter(owner_id=owner_id, user_id=user_id, complete=False).first()
        return current if current else self.create(owner_id=owner_id, user_id=user_id,
                                                   scheduled_date=datetime.date.today())

    def get_by_payment_intent_id(self, intend_id):
        return self.get_queryset().get(_stripe_payment_intent_id=intend_id)

    def get_idle(self):
        return self.get_queryset().filter(complete=False,
                                          last_updated__lte=(datetime.datetime.now() - datetime.timedelta(minutes=20)))


class CompanyManager(models.Manager):
    def get_by_stripe_id(self, stripe_id):
        return self.get_queryset().get(stripe_id=stripe_id)

    def get_public(self):
        return self.get_queryset().filter(_is_viewable=True)
