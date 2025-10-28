from django.conf import settings
from openai import OpenAI

from library.singleton import SingletonMeta


class AIService(metaclass=SingletonMeta):
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_summary(self, text):
        try:
            response = self.client.responses.create(
                model="gpt-4o",
                instructions="write hello",
                input=text,
            )
            return response.output_text
        except Exception as e:
            print(f"Error generating summary: {e}")
            return ""
