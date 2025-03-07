import re
import socket
import ssl
from json import dumps
from time import sleep
from base64 import b64encode, urlsafe_b64decode
from json import loads
import socks


class MessagingSocket:
    HOST = 'smartfox.avkn.co'
    PORT = 9599

    def __init__(self, client, openai_client):
        self._client = client
        self._exclude = []
        self._openai_client = openai_client
        socket.socket = socks.socksocket
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        raw_socket.connect((self.HOST, self.PORT))
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_3
        self._socket = context.wrap_socket(raw_socket, server_hostname=self.HOST)
        self._room_id = None

    def send(self, data):
        return self._socket.sendall((data.strip() + "\x00").encode('utf-8'))

    def receive(self, t=1):
        response = self._socket.recv(4096).decode('utf-8', errors='ignore')
        sleep(t)
        return response

    def set_exclude(self, exclude):
        self._exclude = exclude

    def _login_data(self):
        self.send(f'''
            <msg t='sys'><body action='login' r='0'><login z='Life'><nick><![CDATA[{self._client.x_avkn_userid}]]></nick><pword><![CDATA[{self._client.x_avkn_sfs_token}]]></pword><mduid><![CDATA[0282]]></mduid><comp><![CDATA[2]]></comp><version><![CDATA[2.005.00]]></version></login></body></msg>
        ''')
        self.receive()

    def _room_list(self):
        self.send('''
        <msg t='sys'><body action='getRmList' r='-1'></body></msg>
        ''')
        self.receive()

    def _zero_room(self):
        self.send('''
        <msg t='sys'><body action='joinRoom' r='-1'><room id='1' pwd='' spec='0' leave='0' old='-1' /></body></msg>
        ''')
        self.receive()

    def _me(self):
        self.send('''
        {"t":"xt","b":{"x":"me","p":{},"c":"bv","r":1}}
        ''')
        self.receive()

    def _gold(self):
        self.send('''
        {"t":"xt","b":{"x":"me","p":{"os_class":"Android","db":"Publish_Heart_Talk_White_Gold","platform":"GooglePlay","d":false,"os":"GooglePlay","si":{"graphicsDeviceVersion":"OpenGL ES 3.2 V@0502.0 (GIT@428fbbc7d8, I593c16c433, 1632727329) (Date:09/27/21)","supportsMultisampleResolveDepth":false,"graphicsDeviceVendor":"Qualcomm","supportsRenderTextures":true,"supportsTextureWrapMirrorOnce":0,"maxComputeWorkGroupSizeZ":64,"supportsGeometryShaders":true,"supportsMultiview":true,"maxComputeBufferInputsGeometry":4,"usesLoadStoreActions":true,"hasMipMaxLevel":true,"OSVersion":"11","supportsRenderToCubemap":true,"maxTextureArraySlices":2048,"processorType":"ARM64","supportsAudio":true,"batteryLevel":0.84,"maxComputeBufferInputsVertex":4,"maxComputeWorkGroupSize":1024,"supportsMultisampled2DArrayTextures":true,"graphicsDeviceID":0,"supportsSparseTextures":false,"maxCubemapSize":16384,"supportsAnisotropicFilter":true,"supportedRenderTargetCount":8,"hasHiddenSurfaceRemovalOnGPU":true,"supportsShadows":true,"maxTextureSize":16384,"supportsAccelerometer":true,"screenWidth":1554,"maxComputeBufferInputsCompute":24,"supportsStencil":1,"processorCount":8,"supports32bitsIndexBuffer":true,"graphicsDeviceType":"OpenGLES3","supportsStoreAndResolveAction":true,"supportsImageEffects":true,"supportsMultisampledTextures":1,"supports3DRenderTextures":true,"graphicsDeviceVendorID":0,"renderingThreadingMode":"MultiThreaded","npotSupport":"Full","supportsGyroscope":true,"supportsCubemapArrayTextures":true,"screenHeight":720,"minConstantBufferOffsetAlignment":false,"maxComputeWorkGroupSizeY":1024,"supportsRenderTargetArrayIndexFromVertexShader":false,"batteryStatus":"Charging","supportsAsyncCompute":false,"supportsVibration":true,"supportsComputeShaders":true,"supportsTessellationShaders":true,"supportsMultisampleAutoResolve":true,"supportsInstancing":true,"deviceModel":"vivo V2180A","supportsMotionVectors":true,"supportsRayTracing":false,"systemMemorySize":7654,"maxGraphicsBufferSize":2147483648,"supportsCompressed3DTextures":true,"androidAPILevel":30,"supportedRandomWriteTargetCount":20,"constantBufferOffsetAlignment":32,"operatingSystemFamily":"Other","supportsMipStreaming":true,"supports2DArrayTextures":true,"copyTextureSupport":"RTToTexture, TextureToRT, DifferentTypes, Copy3D, Basic","graphicsPixelFillrate":-1,"maxComputeBufferInputsHull":4,"maxAnisotropyLevel":16,"supportsConservativeRaster":false,"operatingSystem":"Android OS 11 / API-30 (RP1A.200720.012/eng.compil.20220715.233728)","supportsAsyncGPUReadback":true,"supportsSetConstantBuffer":true,"graphicsMultiThreaded":true,"supportsGpuRecorder":false,"graphicsUVStartsAtTop":false,"supportsGPUFence":false,"androidOSVersion":"11","graphicsDeviceName":"Adreno (TM) 610","supportsVertexPrograms":true,"computeSubGroupSize":1,"deviceType":"Handheld","supportsLocationService":true,"graphicsShaderLevel":50,"supportsRawShadowDepthSampling":true,"maxTexture3DSize":2048,"graphicsMemorySize":2048,"hasDynamicUniformArrayIndexingInFragmentShaders":true,"hdrDisplaySupportFlags":"None","processorFrequency":4800,"supports3DTextures":true,"supportsHardwareQuadTopology":false,"maxComputeWorkGroupSizeX":1024,"usesReversedZBuffer":false,"maxComputeBufferInputsDomain":4,"supportsSeparatedRenderTargetsBlend":true,"maxComputeBufferInputsFragment":4,"supportsGraphicsFence":true},"cl":["en"],"lvs":{"GpuMemory":"VeryHigh","GpuLevel":"VeryHigh","TotalMemory":"VeryHigh","CpuMemory":"VeryHigh","IsUltraHigh":true,"AverageLevel":"VeryHigh"},"ft":{"avakin-interactions":3,"emojis":2,"shop":1,"homebrew":40,"more-avakins":1,"int-gift":2,"lkwd-bundle-format":1,"furniture-format":2,"avatar-actions":3,"lobby":3,"avatar_contour":1,"chat-reactions":1,"node-chat":1,"node-hashing":2,"jwt-avakin":1,"shader":1,"avatar_bodymorph":1,"badges":1,"netactor":101},"p":"Android","dl":"English","v":"1.095.00","vr":false,"i":false,"l":"en-US","m":false,"b":true},"c":"pld","r":1}}
        ''')
        self.receive()

    def _room_zero(self):
        for i in range(2):
            self.send('''
            {"t":"xt","b":{"x":"me","p":{"d":false,"fl":null,"o":0,"f":["1056102068"],"l":-1},"c":"rl","r":1}}
            ''')
            self.receive()

    def _room(self):
        self.send('''
            {"t":"xt","b":{"x":"me","p":{"d":false,"ri":0,"id":29939333,"f":null},"c":"rr","r":1}}
        ''')
        sleep(1)

    def _get_room_id(self):
        while True:
            content = self.receive().replace("\\", "").strip()
            self._room_id = re.search(r"<rm id='(\d+)'", content)
            if self._room_id:
                self._room_id = int(self._room_id.group(1))
                break

    def _big(self):
        self.send(dumps({"t": "xt", "b": {"x": "se", "p": {"d": self._client.x_avkn_username,
                                                           "c": "eNrNmG1v2jwUhv9KlU+bhKYkEKD71jSlsHZboC+0e5iQSRzqkhfmJFA0+t8f26EhTbKOE2VSP5S2tm/n8vGJuY9/S5b0Wfo9kVaYhiTwJ9LniaR8krWJ1JhIPvKwaDlZoQXxRZv1gCiyIkxFh4M95GJZSboC3yFz0Y4RDaeyrExnKCTWFm/wjAZr1qS2+D/8D3nrYBxNQzbx9gEROnUXa9sK4iimOKJkhnmj4rA+3w53wzCyxazBCrlbF8937R5TPbA5m81tFNAwKExlUxyGqrONfRvTNYNLuKYR8aOthxY4Xk49wn5vXJT8K2vbWWBvvIAu2cxsNEYiBoojlspJQostXaz2A4uYLDcynx+TUcS2sT9NnyoG95AbYtHNA2HjCBE3TKaRxQSFz48vo0UMD1ckYTl8vBW4LHps4H8sIVgshCRMN573iqau2jjS5MZRs9M4UjWWKs+NjIBvfU7ABomR+4+8Zre2vK7LBr/8lInygm6zcdTiZK0ygYMsvERsy6F4TEiQy/MRrGQpDtXMXRSGGBzDKnhco8JFvo0sq4qswqLA4eOvJlTDjxKoJkJRFARgWRhh3xLvI0yXvMw5VYfnepsNL813WiUlwsBawGPBT12oKHMsAkMhTmioisXPIfBXn/hzTH1UYcdmyFpUSd4qIfEx/Fns6zoKYvCjLlmCYFtnX44motF1xbcAfiyukQteIo19MBk8R4jtYrDGZxaK+SjhuSpIbeRb1R66DEKwcG+FDlH+bHCXY2EjdR6lhuKPxkTJGxNiJxnQu9XVQf9E0VFfkRVP9DnExalP5XMn1o4jxpSl2TSxqCl3/AcPw7r5dqxw1qSVGxsw+PVYMfXO7ZUyujaL0K+9ch60LMKvWa9pjN/yU4cbwB3u2dDrqtR13MFYG37Xf5UgZ/x8AThv2g6hrUg6f8QjY/GwMm+NC73fbpWSimKjsP95p/hXytfuEZwDRbRadjo1mGCgm7vOuTk0voyMdr8Il9ZmtVCmRgRM2doE3nr9aPbQ/Km9OB0USd+oHWtjV9/Vnu+dNJjIuNV72jdzcPN9OCwL5UupXQ/nixMHY/64O9FUs3evHp+WYWavAWohTf0/mPTMGGrK8O5c7za1Iml6RVELZaYEAJ+Uw1PLODeu4rNRyyly7i9Q8qCFCuOvlPtaABzMuLfuLY8795uzTTRotS6KoG9e79QS5NdVCXgJxxc/Wnfmjd7vdi+L+GX3T/Wkxr4kAiP/GqvjJ0Lbq8dvV6N4rJakR/kNWS3kaZX0bk7XbAn2XqDS+u69AGWLR/Bh9I+YclUKOFRPC/Pywll1HSM+uY8MWsR860q4Cj2vlJBPPMTrQLu8XOL+rqQQLta5xTK2pEoVj/zKl0D8eaZAyzbz2n63K8/S8//Vpfla",
                                                           "x": {"rightHandFree": "False",
                                                                 "appleMusic_track_name": None,
                                                                 "friend_request_from": 0,
                                                                 "hc": "FFFFFF", "IsRecording": None,
                                                                 "oc": self._client.outfit,
                                                                 "xp": self._client.x_avkn_xp,
                                                                 "bc": self._client.body, "subscription_public": True,
                                                                 "appleMusic_track_id": None, "subscription_tier": 0,
                                                                 "level": "0",
                                                                 "private_message": 1, "anim_state": "",
                                                                 "leftHandFree": "False",
                                                                 "avakin_busy": False, "mood_state": "0",
                                                                 "appleMusic_artist_name": None, "anim_loop": "",
                                                                 "ul": ["", None],
                                                                 "IsLiveBroadcast": False,
                                                                 "appleMusic_collection_name": None,
                                                                 "lock_interactions": False}}, "c": "ua",
                                          "r": self._room_id}}))
        sleep(1)

    def init(self):
        self.receive(t=0)
        self._login_data()
        self._room_list()
        self._zero_room()
        self._me()
        self._gold()
        self._room_zero()
        self._room()
        self._get_room_id()
        self._big()
        self.send(dumps({"t": "xt", "b": {"x": "ae", "p": {"e": 1, "a": [
            {"id": 1, "c": True, "a": "init", "uid": "1", "t": 2, "o": [-6.91, -0.01, 2.55], "r": [0, 180, 0]}]},
                                          "c": "pa",
                                          "r": self._room_id}}))
        self.send(dumps({"t": "xt", "b": {"x": "chat", "p": {}, "c": "ch", "r": self._room_id}}))
        self.send(dumps({"t": "xt", "b": {"x": "inter", "p": {}, "c": "inGD", "r": self._room_id}}))
        self.send(
            dumps({"t": "xt", "b": {"x": "me", "p": {"f": None, "a": 29939333}, "c": "gaad", "r": self._room_id}}))
        self.send(dumps(
            {"t": "xt", "b": {"x": "se", "p": {"x": {"lock_interactions": False}}, "c": "ua", "r": self._room_id}}))


    def encrypt_message(self, message):
        raw=f'''{{"n":"{self._client.x_avkn_username}","m":"{message}","h":-1,"c":-1,"cg":"","o":[-7.35,0.03,1.98],"r":[0,180,0]}}'''
        b64 = b64encode(raw.encode('utf-8'))
        b64=b64.decode('utf-8')
        message=f"<msg t='sys'><body action='pubMsg' r='{self._room_id}'><txt><![CDATA[{b64}]]></txt></body></msg>"
        return message

    def listen(self):
        print(f"[{self._client.x_avkn_username}:{self._client.x_avkn_userid}] Listening On [Room ID: {self._room_id}]")
        while True:
            try:
                content = self._socket.recv(4096).decode('utf-8', errors='ignore')
                message = re.findall(r"action='pubMsg'.*\[CDATA\[(.*)]]", content)
                if message:
                    message = loads(urlsafe_b64decode(message[0] + "==").decode('utf-8'))
                    if message['n'] in self._exclude:
                        continue
                    print(f"[{message['n']}]: {message['m']}")
                    response = self._openai_client.response(message['n'], message['m'])
                    print(f"[{self._client.x_avkn_username}:{self._client.x_avkn_userid}]: {response}")
                    self.send(self.encrypt_message(f"[{message['n']}], {response}"))
            except Exception as e:
                ...

    @property
    def room_id(self):
        return self.room_id
