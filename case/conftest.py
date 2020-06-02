#  coding:utf-8
from case.mp_login import Login
from common import envs
from common.db_operation import DataLoader
import pytest

@pytest.fixture(scope="session")
def get_mobile(studentid):
    data = DataLoader(envs.QA)
    cur = data.cur
    db = cur.execute("SELECT login_name FROM user_account WHERE id = %d"%studentid)
    mobile = data.cur.fetchone()[0]
    print(mobile)
    return mobile






@pytest.fixture(scope="session",params="mobile")
def login(get_mobile):
    L = Login(envs.QA)
    # mobile = 13048052194
    _code = L.get_code(get_mobile)
    res = L.login(get_mobile, _code)
    return res

if __name__ =="__main__":
    login()

