# ----------------------- #
# encoding: utf8          #
#                         #
# Authorized access only  #
#    By Joseph Wang       #
#                         #
#   cnjowang@gmail.com    #
# ----------------------- #
import hashlib
# import json
import logging
import time
# import urllib.parse
# import redis
import requests


logging.getLogger("requests").setLevel(logging.WARN)


class DuplicatedTeacherError(Exception): pass


class DuplicatedStudentError(Exception): pass


class LoginError(Exception): pass


class GeneralClassError(Exception): pass


logger = logging.getLogger("sgt")
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a+')


class ServiceUtil:
    eto32Table = b"AB56DE3C8L2WF4UVM7JRSGPQYZTXK9HN"
    PRIVATE_KEY = "cc16be4b:346c51d"

    @classmethod
    def encode(cls, data, olen=26):
        s = 0
        ilen = len(data)
        result = list('\0' * olen)
        i = 0
        j = 0
        while i < ilen:
            b1 = ((data[i] << s) & 0xff) >> s
            b2 = data[i + 1] if i + 1 < ilen else 0
            if s >= 3:
                b1 = ((b1 & 0xff) << (s - 3)) | (((b2 & 0xff) >> (11 - s)) & 0xff)
                result[j] = cls.eto32Table[b1]
                j += 1
                s -= 3
            else:
                result[j] = cls.eto32Table[b1 >> (8 - s - 5)]
                j += 1
                s += 5
                i -= 1
            if j >= olen:
                break
            i += 1
        return bytes(result)

    @classmethod
    def sign(cls, *all_data):
        data = dict()
        for _data in all_data:
            data.update(_data)

        keys = list(data.keys())
        keys.sort()
        _s = []
        for _key in keys:
            _s.append("%s:%s" % (_key, data[_key]))
        _s.append(cls.PRIVATE_KEY)
        plain_text = ("".join(_s)).encode('utf8')
        digest = hashlib.md5(plain_text).digest()
        result = cls.encode(digest, 26)
        return result.decode('utf8')


class Endpoint:
    def __init__(self,env):
        self.env = env
        self.uid = None
        self.http_session = requests.session()
        self.http_token = None

    def http_headers(self, data):
        headers = {
            "c": "1",
            "a": "1",  # app:a=1 p=3 c=1   小程序：channel: 40107,appId: 9,platform: 1,
            "p": "3",
            "v": "v0.01",
            # "a": "RESERVED",
            "t": "%d" % int(time.time() * 1000),
        }
        if self.uid:
            headers['u'] = "%s" % self.uid
        if self.http_token:
            headers['token'] = self.http_token

        headers['s'] = ServiceUtil.sign(headers, data)
        return headers

#
#
#     def Verif_code(self, identity):
#         """
#         获取验证码
#         :param identity: 手机号码
#         :return:
#         """
#         url = "http://10.4.4.140:10099/mp-business/public/acl/student/sms"
#         data = {
#             "mobile": identity,
#             "smsType": 1
#         }
#         headers = self.http_headers(data)
#         resp = self.http_session.get(url + "?" + urllib.parse.urlencode(data), headers=headers)
#         logger.debug("SMS: " + resp.text)
#
#         _redis = redis.Redis(
#             host=self.env.redis_host,
#             port=self.env.redis_port,
#             password=self.env.redis_cridential,
#             db=self.env.redis_db
#             )
#         _code = _redis.get("planet:auth:sms::1_3_1_1_%s" % identity)
#         _code = _code.decode('utf8')[1:-1]
#         print(_code)
#         return _code
#
#     def login(self, identity):
#         """
#         登录
#         :param identity:
#         :return:
#         """
#         _code = self.Verif_code(identity)
#         url = "http://10.4.4.140:10099/mp-business/public/acl/student/mobile/login"
#         data = {
#             "mobile": identity,
#             "verifyCode": _code
#         }
#         headers = self.http_headers(data)
#         # print(headers)
#         # print(data)
#         resp = self.http_session.post(url, headers=headers, json=data)
#         logger.debug("LOGIN: " + resp.text)
#         resp_json = json.loads(resp.text)
#         if resp_json['success']:
#             self.uid = resp_json['data']['user']['id']
#             self.http_token = resp_json['data']['token']
#         else:
#             logger.error(resp.text)
#             raise LoginError('Failed login for student %s' % identity)
#
#
# if __name__ == "__main__":
#     test_case = Endpoint(envs.QA)
#     test_case.login(13048050000)
