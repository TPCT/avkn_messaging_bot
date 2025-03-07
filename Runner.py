import time
from threading import Thread
from Core.Chatbot import Chatbot
from Core.Account import Account


OPEN_AI_SECRET = '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'
OPEN_AI_MODEL_ID = 'ft:gpt-3.5-turbo-0125:personal::B7issDw8'
openai_client = Chatbot(OPEN_AI_SECRET, OPEN_AI_MODEL_ID)

excludes = []

def thread(_token, proxy):
    _account = Account(_token, proxy, openai_client)
    _account.start_presence_socket()
    presence_thread = Thread(target=_account.presence_socket.keepalive, daemon=True)
    presence_thread.start()

    _account.start_messaging_socket()
    excludes.append(_account.x_avkn_username)
    _account.messaging_socket.set_exclude(excludes)
    messaging_thread = Thread(target=_account.messaging_socket.listen, daemon=True)
    messaging_thread.start()


if __name__ == '__main__':
    proxies = []
    tokens = []

    with open('proxies', 'r') as f:
        for line in f:
            if not line.strip():
                continue
            proxies.append(line.strip())


    with open('tokens', 'r') as f:
        for line in f:
            if not line.strip():
                continue
            tokens.append(line.strip())

    for i, token in enumerate(tokens):
        thread(token, proxies[i % len(proxies)] if proxies else None)

    input()