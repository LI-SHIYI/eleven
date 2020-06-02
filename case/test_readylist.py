#  coding:utf-8
from case.student_list import stu_list
from common import envs
import pytest
from common.logger import Log
from case.mp_login import Login


class Test_relist:
    log = Log()
    stu_list = stu_list(envs.QA)

    @pytest.mark.usefixtures('login')
    @pytest.mark.parametrize("studentid, current, pagesize, showstatus, err",[(5, 1, 20, 2, True)])
    def test_readylist(self, studentid, current, pagesize, showstatus, err):
        result = self.stu_list.ready_list(studentid, current, pagesize, showstatus)
        self.log.info("结果"+ str(result))

        if result["success"]:
            assert err == result["success"]
        else:
            assert err == result["error"]["code"]


if __name__ == "__main__":
    pytest.main(["-s", "test_readylist.py"])
