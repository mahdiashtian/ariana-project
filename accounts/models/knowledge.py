from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import models
from rest_framework import serializers

from accounts.tasks import generate_summary_task


class Knowledge(models.Model):
    text = models.TextField(

    )
    summary = models.TextField(blank=True, null=True)

    _skip_summary_update = False

    def save(self, *args, **kwargs):
        skip_summary_update = kwargs.pop("skip_summary_update", False)
        self._skip_summary_update = skip_summary_update

        super().save(*args, **kwargs)
        # channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)(
        #     f"online_users",
        #     {
        #         "type": "send_message",
        #         "data": type('TmpSerializer', (serializers.ModelSerializer,), {'Meta': type('Meta', (), {'model': Knowledge, 'fields': '__all__'})})(self).data
        #
        #     }
        # )
        # if not self._skip_summary_update:
        #     generate_summary_task.delay(self.id)

    def __str__(self):
        return f"Knowledge #{self.pk}"
