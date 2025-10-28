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
# @receiver(post_save, sender=Knowledge)
# def handle_knowledge_save(sender, instance, **kwargs):
#     if getattr(instance, "_skip_summary_update", False):
#             return
#     generate_summary_task.delay(instance.id)
