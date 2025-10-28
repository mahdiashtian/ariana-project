from django.db import models

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

        if not self._skip_summary_update:
            generate_summary_task.delay(self.id)

    def __str__(self):
        return f"Knowledge #{self.pk}"
