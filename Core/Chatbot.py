from openai import OpenAI
from random import choice

class Chatbot:
    def __init__(self, api_key, model_id):
        self._client = OpenAI(api_key=api_key)
        self._model_id = model_id

    def response(self, message):
        return self._client.chat.completions.create(model=self._model_id,
                                                    messages=[
                                                        {"role": "system",
                                                         "content": "You're a real Avakin player, not a bot. You talk like a normal player, cracking jokes, being sarcastic, and sometimes just talking nonsense. You NEVER sound formal, robotic, or structured. Keep it short, messy, real, and unpredictable—like an actual person typing fast in chat."},
                                                        {"role": "user", "content": message}
                                                    ],
                                                    max_tokens=20
                                                    ).choices[0].message.content
