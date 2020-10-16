from django.db import models
from django.contrib.postgres.fields import JSONField


class StripeEvent(models.Model):
    event_id = models.CharField(max_length=255)
    object_id = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    live_mode = models.BooleanField()
    event_type = models.CharField(max_length=100)
    event_obj = JSONField()
    metadata = JSONField()


    @staticmethod
    def from_event(event):
        return StripeEvent.objects.create(
            event_id=event.stripe_id,
            object_id=event.data.object.stripe_id,
            live_mode=event.livemode,
            event_type=event.type,
            event_obj=event.data.object,
            metadata=event.data.object.metadata
        )
