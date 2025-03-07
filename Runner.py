from threading import Thread
from Core.Chatbot import Chatbot
from Core.Account import Account
from Core.PresenceSocket import PresenceSocket
from Core.MessagingSocket import MessagingSocket

OPEN_AI_SECRET = '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'
OPEN_AI_MODEL_ID = 'ft:gpt-3.5-turbo-0125:personal::B7issDw8'
openai_client = Chatbot(OPEN_AI_SECRET, OPEN_AI_MODEL_ID)


def thread(token, proxy):
    account = Account(token, proxy, openai_client)
    presence_socket = PresenceSocket(account)
    messaging_socket = MessagingSocket(account, openai_client)
    account.initialize()
    presence_thread = Thread(target=presence_socket.keepalive, daemon=True)
    presence_thread.start()
    messaging_socket.init()
    messaging_socket.listen()


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