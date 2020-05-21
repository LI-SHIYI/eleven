# coding:utf-8

import unittest
from case.mp_login import Login
from common.logger import Log
from common import envs
from parameterized import parameterized, param
import pytest


class Test_Login(unittest.TestCase):
    log = Log()
    L = Login(envs.QA)


    def setUp(self):
        """
        每条用例执行之前都会执行的操作放在此处
        定义一些变量
        打开文件
        连接数据库
        前置数据等操作
        """
        pass
        return

    def tearDown(self):
        """
        每条用例执行完之后都会执行的操作放在此处
        数据清理
        关闭文件或者数据库连接等
        """
        pass
        return

    @classmethod
    def setUpClass(cls):
        """
        这个只有在开始和结束的时候执行一次，即执行第一个用例之前
        """
        print('-----')
        return

    @classmethod
    def tearDownClass(cls):
        """
        这个只有在开始和结束的时候执行一次，即执行最后一个用例之后
        """
        print('=====')
        return

    number = L.get_phone_number()

    case_data1 = [
        #  手机号码为空
        ("", 111111, 20001),    # 手机号为空,验证码不为空 ，验证码格式正确 手机号为必填项
        ("", '!@##.,', 20001),  # 手机号为空,验证码不为空,验证码格式不正确  手机号为必填项
        ("", 11111, 20001),     # 手机号为空,验证码不为空，验证码格式不正确  手机号为必填项
        ("", "      ", 20001),  # 手机号为空,验证码不为空，验证码格式不正确  手机号为必填项
        ("", "", 20001),        # 手机号为空,验证码为空  手机号为必填项
        # 手机号码格式不正确
        (1304805219, "", 20001),        # 手机号不为空,手机号格式不正确，验证码为空    验证码是必填项
        (1304805219, 11111, 31001),     # 手机号不为空,手机号格式不正确，验证码不为空 ，验证码格式不正确
        (1304805219, '!@##.,', 31001),  # 手机号不为空,手机号格式不正确，验证码不为空 ，验证码格式不正确
        (1304805219, "      ", 31001),  # 手机号不为空,手机号格式不正确，验证码不为空 ，验证码格式不正确
        (1304805219, 111111, 31001),    # 手机号不为空,手机号格式不正确，验证码不为空 ，验证码格式正确
        # 手机号码不合法
        (11111111111, "", 20001),                # 手机号不为空,手机号格式正确，手机号码不合法，验证码为空
        ("           ", "", 20001),              # 手机号不为空,手机号格式正确，手机号码不合法，验证码为空
        (",,,,,,,,,,,", "", 20001),              # 手机号不为空,手机号格式正确，手机号码不合法，验证码为空
        ("11111111111", "      ", 31001),        # 手机号不为空,手机号格式正确，手机号码不合法，验证码不为空，验证码格式不正确
        ("11111111111", "，，，，，，", 31001),  # 手机号不为空,手机号格式正确，手机号码不合法，验证码不为空，验证码格式不正确
        ("11111111111", "11111", 31001),         # 手机号不为空,手机号格式正确，手机号码不合法，验证码不为空，验证码格式不正确
        ("11111111111", "111111", 31001),        # 手机号不为空,手机号格式正确，手机号码不合法，验证码不为空，验证码格式正确
    ]

    case_data2 = [
        # 手机号码合法
        (number, "", 20001),        # 手机号合法，验证码为空
        (number, "      ", 31002),  # 手机号合法，验证码不为空，验证码格式不正确
        (number, 11111, 31002),     # 手机号合法，验证码不为空，验证码格式不正确
        (number, ",,,,,,", 31002),  # 手机号合法，验证码不为空，验证码格式不正确
        (number, "111111", 31002),  # 手机号合法，验证码不为空，验证码格式正确,验证码错误
    ]

    def test_login_01(self):
        """
        登录成功

        :param mobile:
        :param _code:
        :return:
        """
        # mobile = self.L.get_phone_number()
        mobile = 13048052194
        set_code = self.L.Verif_code(mobile)  # 获取验证码
        print(set_code)
        _code = self.L.get_code(mobile)
        print(mobile)
        self.log.info("---------开始测试----------")
        result = self.L.login(mobile, _code)
        self.log.info("登录结果：" + str(result))
        self.log.info("登录是否成功：" + str(result['success']))
        self.assertEqual(True, result['success'])

    @parameterized.expand(case_data1)
    def test_login_02(self, mobile, _code, err):
        """
        手机号为空
        :param mobile:
        :param _code:
        :return:
        """
        print(mobile)
        print(_code)
        # a = self.L.Verif_code(mobile)
        self.log.info("---------开始测试----------")
        result = self.L.login(mobile, _code)
        self.log.info("登录结果：" + str(result))
        self.log.info("登录是否成功：" + str(result['success']))
        # self.assertEqual(True, result['success'])
        self.assertEqual(err, result['error']['code'])

    @parameterized.expand(case_data2)
    def test_login_03(self, mobile, _code, err):
        """
        验证码错误
        :param mobile:
        :param _code:
        :return:
        """
        print(mobile)
        print(_code)

        _redis = self.L.data_oper.redis_conn

        _code1 = _redis.get("planet:auth:sms:lock::1_3_1_1_%s" % mobile)
        if _code1:
            _code1 = _code1.decode('utf8')[1:-1]
        else:
            a = self.L.Verif_code(mobile)
            print(a)

        self.log.info("---------开始测试----------")
        result = self.L.login(mobile, _code)
        self.log.info("登录结果：" + str(result))
        self.log.info("登录是否成功：" + str(result['success']))
        # self.assertEqual(True, result['success'])
        self.assertEqual(err, result['error']['code'])

if __name__ == "__main__":
    # a = Test_Login()
    # a.test_login()
    # unittest.main()
    pytest.main(["-v", "test_login.py::Test_Login::test_login_01"])
