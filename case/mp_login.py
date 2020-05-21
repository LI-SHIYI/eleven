# coding:utf-8

import requests
import json
from common.ServiceUtil import Endpoint
from common import envs
from common.logger import Log
from common.db_operation import DataLoader
import random
import pytest

class Login:

    def __init__(self, env):
        self.env = env

        self.log = Log()
        # env = envs.QA
        self.endpoint = Endpoint(env)
        self.data_oper = DataLoader(env)

    def get_phone_number(self):
        """
        随机生成手机号

        :return:
        """
        # pre_lst = ["13", "14", "15", "17", "18"]
        pre_lst = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152", \
                   "153", "155", "157", "158", "159", "187", "188"]

        mobile = random.choice(pre_lst) + "".join(str(random.randint(00000000, 99999999)))

        self.log.info("手机号码:" + mobile)
        return mobile

    def Verif_code(self, mobile):
        """
        发送验证码
        :param mobile: 手机号码
        :return:
        """
        # mobile = self.get_phone_number()
        url = "%s/mp-business/public/acl/student/sms" % self.env.http_base_url
        params = {
            "mobile": mobile,
            "smsType": 1
        }
        headers = self.endpoint.http_headers(params)
        resp = requests.get(url=url, params=params, headers=headers).content
        resp_json = json.loads(resp)
        # self.log.debug("SMS: ",resp_json)
        print(resp_json)

        # _redis = redis.Redis(
        #     host=self.env.redis_host,
        #     port=self.env.redis_port,
        #     password=self.env.redis_cridential,
        #     db=self.env.redis_db
        # )
        return resp_json


    def get_code(self,mobile):
        """
        获取验证码
        :param mobile:
        :return:
        """
        _redis = self.data_oper.redis_conn

        _code = _redis.get("planet:auth:sms:lock::1_3_1_1_%s" % mobile)
        if _code:
            _code = _code.decode('utf8')[1:-1]
        else:
            _code = None

        print(_code)
        # self.log.debug("SMS: " + _code)
        return _code


    def login(self, mobile, _code):
        """
        :param mobile: 手机号
        :param verifyCode: 验证码
        :param identifier: 设备识别号
        :param channelId: 渠道ID
        :param recommendAcctId: 转介绍人ID
        :return: 
        """
        # mobile = self.get_phone_number()

        # _code = self.Verif_code(mobile)  # 获取验证码

        url = "%s/mp-business/public/acl/student/mobile/login" % self.env.http_base_url
        params = {
            "mobile": mobile,
            "verifyCode": _code,
            "identifier":"6628653bea28fba7e1de26381976d9f9a98e5c9270bfc3cd4be720fb3dc95ba4"
            # "channelId": channelId,
            # "recommendAcctId": recommendAcctId
        }
        print (params["mobile"],params["verifyCode"])
        headers = self.endpoint.http_headers(params)
        resp = requests.post(url=url, json=params, headers=headers).content
        resp_json = json.loads(resp)
        self.log.debug(resp_json)
        return resp_json


if __name__ == "__main__":
    a = Login(envs.QA)
    c = a.Verif_code(13048052195)
    a.login(13048052195,c)
