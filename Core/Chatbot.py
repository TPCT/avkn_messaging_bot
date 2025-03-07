from openai import OpenAI


class Chatbot:
    def __init__(self, api_key, model_id):
        self._client = OpenAI(api_key=api_key)
        self._model_id = model_id

    def response(self, message):
        return self._client.chat.completions.create(model=self._model_id,
                                                    messages=[
                                                        {"role": "user", "content": message}],
                                                    max_tokens=50).choices[0].message.content
