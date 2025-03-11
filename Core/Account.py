from warnings import filterwarnings
from requests import Session
from json import loads
import jwt
from Core.MessagingSocket import MessagingSocket
from Core.PresenceSocket import PresenceSocket
from Core.Utils import Utils
from threading import Thread

filterwarnings('ignore')


class Account:
    JTAG_API_SECRET = "Si1932kjaS821klV1201n01i"
    JTAG_API = "https://jtag.avkngeeks.com/api/v1/jsq"
    AVKN_API_LOGIN = "https://api-sni.avkn.co/auth/1/auth/1/login"
    AVKN_API_GET_BODY = "https://api-sni.avkn.co/objects/1/objects/1/get"
    AVKN_API_GET_FRIENDS = "https://api-sni.avkn.co/relations/1/relations/1/list"
    AVKN_API_SESSION_TOKEN_REFRESH = "https://api-sni.avkn.co/auth/1/auth/1/sfstoken"
    SOCKET_HOST = 'smartfox.avkn.co'
    SOCKET_PORT = 9599

    def __init__(self, token, proxy=None, openai_client=None):
        self._token = token
        self._account_info = {}
        self._outfit = None
        self._body = None
        self._friends = []
        self._logged = False
        self._session = Session()
        self._openai_client = openai_client
        self._proxy = {
            'http': proxy,
            'https': proxy,
        } if proxy else None
        self._messaging_socket = MessagingSocket(self, self._openai_client)
        self._presence_socket = PresenceSocket(self)

    def __getattr__(self, name):
        if name.startswith('x_avkn'):
            return str(self._account_info[name])

    def __setattr__(self, key, value):
        if key.startswith('x_avkn'):
            self._account_info[key] = str(value)
            return
        self.__dict__[key] = value

    def request(self, method, url, **kwargs):
        kwargs['verify'] = False
        if url.startswith('https://api-sni.avkn.co'):
            kwargs['proxies'] = self._proxy

        response = self._session.request(method, url, **kwargs)
        for key, value in response.headers.items():
            key = key.replace('-', '_').lower()
            if key.lower().startswith('x_avkn'):
                self._account_info[key] = value

        if response.headers['content-type'] == 'application/json':
            for key, value in response.json().items():
                key = key.replace('-', '_').lower()
                if key.lower().startswith('x_avkn') and key not in self._account_info:
                    self._account_info[key] = value
        return response

    def login(self):
        if self._logged:
            return
        headers = self.request('GET', self.JTAG_API + "/start-chat",
                               headers={'api-key': self.JTAG_API_SECRET}).json()
        response = self.request('POST', self.AVKN_API_LOGIN, headers=headers, json={
            'type': 'token',
            'request': {
                'token': self._token,
            }
        })
        if response.status_code != 200:
            raise Exception("Login failed")

        self.x_avkn_userid = int(response.json().get('user_id'))
        if not all([self.x_avkn_chat_tag, self.x_avkn_jwtsession, self.x_avkn_session]):
            raise ValueError("Missing Required Response Data")

        response = self.request('POST', self.JTAG_API + "/journey-seq",
                                headers={
                                    'api-key': self.JTAG_API_SECRET,
                                },
                                json={
                                    'otherparty_public_hash': self.x_avkn_chat_tag,
                                    'jwt_session': self.x_avkn_jwtsession,
                                    'login_token': self.x_avkn_session,
                                    'user_id': self.x_avkn_userid,
                                })

        self._session.headers = {
            'content-type': 'application/json; charset=utf-8',
            'x-avkn-session': self.x_avkn_session, 'x-avkn-jwtsession': self.x_avkn_jwtsession,
            'x-avkn-userid': self.x_avkn_userid, 'x-avkn-apiversion': '15', 'x-avkn-clientos': 'GooglePlay',
            'x-avkn-clientplatform': 'GooglePlay', 'x-avkn-clientversion': self.x_avkn_clientversion,
            'x-avkn-clientversioncode': self.x_avkn_clientversioncode,
            'x-avkn-advertisingid': self.x_avkn_advertisingid,
            'x-avkn-gamesessionid': self.x_avkn_gamesessionid, 'x-avkn-vendorid': self.x_avkn_vendorid,
            'x-avkn-locale': 'en-US',
            'x-avkn-journey-seq': f'{self.x_avkn_journey_seq}', 'accept-encoding': 'gzip, identity',
            'user-agent': 'BestHTTP/2 v2.8.5'
        }
        self._logged = True
        return self._logged

    def get_outfit(self):
        if not self._logged:
            raise Exception("Login First To Fetch Outfit")
        response = self.request('POST', self.AVKN_API_GET_BODY, json={
            'type': 'outfit'
        })
        self._outfit = list(response.json()['objects'][0].values())[0]

    def get_body(self):
        if not self._logged:
            raise Exception("Login First To Fetch Body")

        response = self.request('POST', self.AVKN_API_GET_BODY, json={
            'type': 'avakinbody'
        })
        self._body = list(response.json()['objects'][0].values())[0]

    def get_friends(self):
        if not self._logged:
            raise Exception("Login First To Fetch Friends")
        response = self.request('POST', self.AVKN_API_GET_FRIENDS, json={
            'check_limits': True
        })
        if response.status_code == 200:
            response = response.json().get('relation' , [])
            for data in response:
                if data['status'] == 'friend':
                    self._friends.append(data['buddy_id'])

    def sfs_refresh(self):
        if not self._logged:
            raise Exception("Login First To Fetch Sfs Token Refresh")
        response = self.request('POST', self.AVKN_API_SESSION_TOKEN_REFRESH, data='null')
        self.x_avkn_sfs_token = response.json()['signature']
        data = jwt.decode(self.x_avkn_sfs_token, options={"verify_signature": False})
        self.x_avkn_username = data['username']
        self.x_avkn_xp = int(data['xp']['xp'])


    @property
    def body(self):
        return self._body

    @property
    def outfit(self):
        return self._outfit

    @property
    def friends(self):
        return self._friends

    def start_presence_socket(self):
        self.login()
        self.get_friends()
        self._presence_socket.init()

    def start_messaging_socket(self):
        self.login()
        self.get_body()
        self.get_outfit()
        self.sfs_refresh()
        self._messaging_socket.init()

    @property
    def presence_socket(self):
        return self._presence_socket

    @property
    def messaging_socket(self):
        return self._messaging_socket

if __name__ == "__main__":
    account = Account(
        token="eyJhbGciOiJSU0EtT0FFUC0yNTYiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIn0.EvYlbzQiKsJmV4QbS0Y7xCSqeRlSqkRD21hU-VemjjBPycY7l46hsLvN2sfmZKrWwhlNLu8G2TTDqpMOrs-WMTSNRRDAtI0BTyFOtLWkwOQUTXhpkQ-yrxdaWsHyPfD8XjJgcsPoPfdn4XSRvb83bHfCltw91gyQoUKHngkPXLlCYHHHLjaLSRwZQJZcgx1rSnSWad-P7dwJV225J3JMPPrwXaC2JPa0G0gjOXTJF7FGsHLF4FG0qWXVEWUZt09ix32PZprN5AgRBdcq_soI3QaGkvATTTtyH0PheyyfhZDbPRWeh5Zgk-ejs_TFEOTpqgBArl5H-lCS4Gk_YKXorg.bBz3b3qq7fPYlLBkTnqlfA.VWr3nHRFsZvFYCAGN9ZYfnqd2T8ejqgUCbV4b0Lu7DTh_Ky3DbKB3UEWh89RR5i7XTSKK3_hi7Q6FKaHX0x5oigMdUDGtXgRKBUjsRG0JQWJIWS4-jUzN42Pxin6wMRTVxfcMgjvZviBc6txCSEoBEgnQDmgnFHl0yMmCD5e6kI.ZixRtSr-KutagkOJWKZtyzFmd5EALFz0aEoCOF_rh00", proxy="http://amgd00_XXrIt:jbk6M29Z+Hrpd4e@dc.oxylabs.io:8000")
    account.serv()