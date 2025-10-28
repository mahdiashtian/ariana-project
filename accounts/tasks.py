from celery import shared_task

from accounts.services import AIService
from accounts.models import Knowledge


@shared_task
def generate_summary_task(knowledge_id):
    try:
        knowledge = Knowledge.objects.get(id=knowledge_id)
        ai_service = AIService()
        summary = ai_service.generate_summary(knowledge.text)

        if summary:
            knowledge.summary = summary
            knowledge.save(update_fields=["summary"])
    except Knowledge.DoesNotExist:
        print(f"Knowledge with ID {knowledge_id} does not exist.")
    except Exception as e:
        print(f"Error generating summary for {knowledge_id}: {e}")
