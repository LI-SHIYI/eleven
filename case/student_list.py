#  coding:utf-8
import requests
from common.ServiceUtil import Endpoint
from common import envs
from common.logger import Log
import json


class stu_list:

    def __init__(self, env):
        self.env = env
        self.endpoint = Endpoint(env)
        self.log = Log()

    def ready_list(self,studentid, current, pagesize, showstatus):
        """
        :param studentid:
        :param current:
        :param pagesize:
        :param showstatus:是否要展示1v1课程：1=是  2=否
        :return:
        """
        url = "%s/mp-business/public/period/student/ready/list" % self.env.http_base_url
        params = {
            "studentId": studentid,
            "current": current,
            "pageSize": pagesize,
            "showStatus": showstatus
        }
        headers = self.endpoint.http_headers(params)
        self.log.debug(headers)
        res = requests.get(url=url, params=params, headers=headers).content
        res_json = json.loads(res)
        return res_json


if __name__ == "__main__":
    l = stu_list(envs.QA)
    a = l.ready_list(5, 1, 20, 2)
    print(a)
