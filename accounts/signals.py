from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Knowledge
from accounts.tasks import generate_summary_task

@receiver(post_save, sender=Knowledge)
def handle_knowledge_save(sender, instance, **kwargs):
    generate_summary_task.delay(instance.id)
