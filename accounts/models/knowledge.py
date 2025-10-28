from django.db import models


class Knowledge(models.Model):
    text = models.TextField(

    )
    summary = models.TextField(blank=True, null=True, editable=False)

    _skip_summary_update = False

    def save(self, *args, **kwargs):
        skip_summary_update = kwargs.pop("skip_summary_update", False)
        self._skip_summary_update = skip_summary_update

        super().save(*args, **kwargs)

        # ------------------------------------------------------------
        # Note:
        # 1. It is possible to perform summary update directly inside the model.
        #    If you decide to uncomment this inline section, make sure to comment
        #    out the post_save signal that handles summary generation to avoid duplicate execution.
        #
        # 2. Instead of serializing the full object with a temporary ModelSerializer,
        #    you can use a simpler approach, e.g., sending only {"id": self.id} to the channel
        #    and let the consumer fetch and serialize the object if needed.
        # ------------------------------------------------------------

        # channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)(
        #     "online_users",
        #     {
        #         "type": "send_message",
        #         "data": type('TmpSerializer', (serializers.ModelSerializer,), {'Meta': type('Meta', (), {'model': Knowledge, 'fields': '__all__'})})(self).data
        #     }
        # )
        # if not self._skip_summary_update:
        #     generate_summary_task.delay(self.id)

    def __str__(self):
        return f"Knowledge #{self.pk}"
