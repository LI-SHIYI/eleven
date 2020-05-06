# coding:utf-8

import unittest
from common import envs
from common.logger import Log
from case.mp_login import Login
from parameterized import parameterized, param


class Getcode(unittest.TestCase):
    log = Log()
    L = Login(envs.QA)

    def setUp(self):
        pass
    def tearDown(self):
        pass

    case_data = [
        ("",31004),#  手机号为空
        (1111111111,31015),#  手机号不为空，手机号格式错误
        ("           ",31015), # 手机号不为空，手机号格式正确,手机号不合法
        (11111111111,31015) , # 手机号不为空，手机号格式正确,手机号不合法
        (",,,,,,,,,,,",31015),  # 手机号不为空，手机号格式正确,手机号不合法
        (13048052194,True)# 手机号不为空，手机号格式正确,手机号合法
    ]

    # @parameterized.expand("")
    @parameterized.expand(case_data)
    def test_getcode(self,mobile,err):
        self.log.info("------开始测试-------")
        self.log.info("-------手机号码为是------"+str(mobile))
        result = self.L.Verif_code(mobile)
        self.log.debug(result)
        if result["success"]:
            self.assertEqual(err,result['success'])
        else:
            self.assertEqual(err,result["error"]["code"])
        self.log.logger.info("------结束测试-------")

if __name__ =="__main__":
    unittest.main()
