# -------------------------------------------------------------
# Signal for automatically generating AI summary after save
#
# Currently commented out because we are using the overridden
# `save()` method in the Knowledge model to trigger the Celery
# task instead. This avoids circular imports and makes the flow
# of summary generation more explicit and testable.
#
# If you want to revert to using signals instead of save() overrides:
# 1. Uncomment this signal block.
# 2. Comment out or remove the Celery call in Knowledge.save().
# -------------------------------------------------------------
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import serializers

from accounts.models import Knowledge
from accounts.tasks import generate_summary_task


@receiver(post_save, sender=Knowledge)
def handle_knowledge_save(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"online_users",
        {
            "type": "send_message",
            "skip_summary_update": instance._skip_summary_update,
            "data": type('TmpSerializer', (serializers.ModelSerializer,),
                         {'Meta': type('Meta', (), {'model': Knowledge, 'fields': '__all__'})})(instance).data

        }
    )
    if not instance._skip_summary_update:
        generate_summary_task.delay(instance.id)
