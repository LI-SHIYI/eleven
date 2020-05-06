# coding:utf-8
import requests
import unittest
import HTMLTestRunner
from melot_planet import envs
from melot_planet.ServiceUtil import Endpoint
from common.db_operation import DataLoader
import json
import time
# import urllib.parse
import redis
import random


class TestCase(unittest.TestCase):
    endpoint = None
    dataloader = None

    @classmethod
    def tearDownClass(self):
        #  必须使用 @ classmethod装饰器, 所有test运行完后运行一次
        print('结束测试')

    @classmethod
    def setUpClass(self):
        #  必须使用@classmethod 装饰器,所有test运行前运行一次
        print('开始测试')

    def tearDown(self):
        print("pass")

    def setUp(self):
        TestCase.endpoint = Endpoint(envs.QA)
        TestCase.dataloader = DataLoader(envs.QA)
        print("go")

    def get_phone_number(self):
        """
        随机生成手机号

        :return:
        """
        pre_lst = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152", \
                   "153", "155", "156", "157", "158", "159", "186", "187", "188"]

        return random.choice(pre_lst) + '.join(random.randint(0, 10))'

        print(get_phone_number())

    def Verif_code(self, identity):
        """
        获取验证码
        :param identity: 手机号码
        :return:
        """
        url = "%s/mp-business/public/acl/product/list" % self.endpoint.env.http_base_url
        params = {
            "mobile": identity,
            "smsType": 1
        }
        headers = self.endpoint.http_headers(params)
        resp = requests.get(url=url, params=params, headers=headers).content
        # self.logger.debug("SMS: " + resp.text)
        resp_json = json.loads(resp)

        return resp_json

    def login(self, identity):
        """
        登录
        :param identity:
        :return:
        """
        _redis = redis.Redis(
            host=self.env.redis_host,
            port=self.env.redis_port,
            password=self.env.redis_cridential,
            db=self.env.redis_db
            )
        _code = _redis.get("planet:auth:sms::1_3_1_1_%s" % identity)
        _code = _code.decode('utf8')[1:-1]
        print(_code)

        url = "%s/mp-business/public/acl/product/list" % self.endpoint.env.http_base_url
        data = {
            "mobile": identity,
            "verifyCode": _code
        }
        headers = self.endpoint.http_headers(data)
        # print(headers)
        # print(data)
        resp = requests.post(url=url, params=params, headers=headers).content
        # self.logger.debug("LOGIN: " + resp.text)
        resp_json = json.loads(resp.text)
        # if resp_json['success']:
        #     self.uid = resp_json['data']['user']['id']
        #     self.http_token = resp_json['data']['token']
        # else:
        #     self.logger.error(resp.text)
        #     raise self.LoginError('Failed login for student %s' % identity)
        return resp_json

    def Productlist(self, terminal_type):
        """
        商品列表接口测试
        :param terminal_type: Terminal type, iOS: 1, Android: null
        :return:
        """
        url = "%s/mp-business/public/acl/product/list" % self.endpoint.env.http_base_url
        params = {"resource": terminal_type}  # self.data["terminal_type"]}
        headers = self.endpoint.http_headers(params)
        response = requests.get(url=url, params=params, headers=headers).content

        data = json.loads(response)
        # data=response
        print(data)
        return data

        get_list = (data['data'])['entries']
        length = len(get_list)
        print(length)

        # db = self.cur.execute("SELECT COUNT(id) FROM trade_product where product_status=1")
        db = self.dataloader.cur.execute("SELECT  COUNT (ID) FROM trade_product WHERE ID IN (SELECT DISTINCT ps.product_id FROM \
                             trade_product_sku ps LEFT JOIN trade_sku_config_map cm ON ps.ID=cm.sku_id \
                              WHERE ps.is_deleted=0 AND cm.config_id=1) AND product_status=1")
        dblen = self.dataloader.cur.fetchone()[0]
        print(dblen)

        try:
            assert data.get('success')
            print("接口调用成功")
            self.assertEqual(length, dblen)
            print("功能正确")
        except Exception:
            print("接口调用失败")

    def test_productdetails(self):  # productid, studentid, terminal_type):
        """
        商品详情
        :param productid: 商品id
        :param studentid: 学生id
        :param terminal_type:  来源 ios：1
        :return:
        """

        url = "%s/mp-business/public/acl/product/%d?" % (self.endpoint.env.http_base_url, self.data["productid"])
        params = {
            "studentId": self.data["studentid"],
            "resource": self.data["terminal_type"]
        }
        headers = self.endpoint.http_headers(params)
        response = requests.get(url=url, params=params, headers=headers).content
        data = json.loads(response)

        print(data)

        try:
            assert data.get('success')
            print("接口调用成功")
        except Exception:
            print("接口调用失败")

    def test_inclassroom(self):
        """
        进入教室
        :param studentid: 学生id
        :param periodid: 课程id
        :return:
        """
        url = "%s/mp-business/public/classroom/enter" % self.endpoint.env.http_base_url
        params = {
            "studentId": self.endpoint.uid,
            "periodId": self.data["periodid"]
        }
        headers = self.endpoint.http_headers(params)
        response = requests.get(url=url, params=params, headers=headers).content
        data = json.loads(response)
        print(data)
        try:
            assert data.get('success')
            print("接口调用成功")
        except Exception:
            print("接口调用失败")

    def test_Verifcode(self):
        """
        发送短信验证码

        :return:
        """
        result = self.Verif_code(self.get_phone_number())
        print(result)

        self.assertEqual(None, result['error'])

    def test_productlist(self):
        self.Productlist(1)


#
# if __name__ == '__main__':
#     test_obj = Test_Case(envs.QA)
#     # test_obj.productlist(1)
#     # test_obj.productdetails(80,1,"")
#     test_obj.login(13048052104)
#     test_obj.inclassroom(3258)


if __name__ == '__main__':
    # Test_Case.data = {
    #     "productid": 1,
    #     "studentid": 1,
    #     "terminal_type": 1,
    #     "periodid": 1
    # }
    # Test_Case.endpoint = Endpoint(envs.QA)
    # Test_Case.dataloader = DataLoader(envs.QA)
    # a = Test_Case()
    # a.test_Verifcode()

    test_suite = unittest.TestSuite()  # 创建一个测试集合
    test_suite.addTest(TestCase('test_Verifcode'))  # 测试套件中添加测试用例
    # test_suite.addTest(Test_Case('test_productdetails'))
    now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    fp = open(now + 'res.html', 'wb')  # 打开一个保存结果的html文件
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='api测试报告', description='测试情况')
    # 生成执行用例的对象
    runner.run(test_suite)
    # 执行测试套件
