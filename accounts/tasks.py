from celery import shared_task
from accounts.services import AIService

@shared_task
def generate_summary_task(knowledge_id):
    from accounts.models import Knowledge # or use: apps.get_model('accounts', 'Knowledge')

    try:
        knowledge = Knowledge.objects.get(id=knowledge_id)
        ai_service = AIService()
        summary = ai_service.generate_summary(knowledge.text)

        if summary:
            knowledge.summary = summary
            knowledge.save(update_fields=["summary"], skip_summary_update=True)

    except Knowledge.DoesNotExist:
        pass
    except Exception as e:
        print(f"Error generating summary for {knowledge_id}: {e}")
