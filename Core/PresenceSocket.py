import socket
from json import dumps
from time import sleep
import socks

# from Core.Account import Account


class PresenceSocket:
    HOST = '54.217.195.155'
    PORT = 8080

    def __init__(self, client):
        self._client = client
        socket.socket = socks.socksocket
        self._presence_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._presence_socket.connect((self.HOST, self.PORT))
        self._killed = False

    def send(self, data):
        data = (data.strip() + '\x1a').encode('utf-8')
        self._presence_socket.sendall(data)

    def kill(self):
        self._killed = True

    def init(self):
        ...

    def keepalive(self):
        self.send(dumps(
            {"msg":"register","data":{"ID":self._client.x_avkn_userid,"version":"v1.1","token":self._client.x_avkn_session,"friends":self._client.friends}}, separators=(',', ':'))
        )
        sleep(20)
        while not self._killed:
            self.send('''{"msg":"keepAlive","data":""}''')
            sleep(20)

# if __name__ == "__main__":
#     account = Account(token="eyJhbGciOiJSU0EtT0FFUC0yNTYiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIn0.fYmbWsl0yH94DuiGKx6kFh3ERgqG1xBrTPbL4tnNmeQKgUDZz2txl-a-bLM1SNoNnutc8YxBO7-CUuS0HtW_w2f-pDVZkLwoLKO6S-oX9chNdAG1soiPRUTx2J9VBnUXz_jlvVp81NiR70x4Bco4ZWy70Yf5nAN7eLp38JRntbS2zDI-eOQ0zLc2DLm3g9_vxxVngHQEQlWVD3XdWEB6vZUeaGFIUd9Ex83QokBFAMhYo5FmdDc96FOJ_NCR70qTHXpy39Wt9kRAQRXkhnhKA-X0MhvRhbz875xbcYZ3Dn_V-PaEceyzAnzg6nJn5974usWNMnZSPoNhysqIdkB0WA.NAr3jZVJlIwPyANvfmY5fw.LHpqEidxNPj8E_kGeqQtiQx1KS8ae4jalGwh3aupnr4epE5Ec5R7vrwCWQWgaOTDt7Uj5qZMF8O7RwcoQ7bMnKvuvY03CBJ7k8e8I57RAq7Lre3R2mgpEN6e9uI_wvf4kpiVUL6q1UQVsJyx0LWiU2G0sv7UJZs_LrmsHp7y3-0.Dj_kWgHRRk9h2m29lhHHHS_EHMxG1CsW1bay6s7Qll4")
#     account.login()
#     account.get_friends()
#     presence = PresenceSocket(account)
#     presence.keepalive()