# coding:utf-8
# import pytest
# import pytest_html
import os
import time

now = time.strftime("%Y_%m_%d_%H_%M_%S")
name = now+"report.html"


if __name__ == '__main__':
    os.system('pytest --html=./report/now+"report.html"')
    # os.system('pytest --reruns1 test_user.py --html =../ reports / test_user.html')
