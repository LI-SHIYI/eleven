#  coding:utf-8
import time
import os
import HTMLTestRunner
import unittest
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from config import readConfig

cur_path = os.path.dirname(os.path.realpath(__file__))


def add_case(caseName="case", rule="test*.py"):
    """
    加载所有测试用例
    :param caseName:
    :param rule:
    :return:
    """
    case_path = os.path.join(cur_path, caseName)
    #  如果不存在这个case文件夹，就自动创建
    if not os.path.exists(case_path): os.mkdir(case_path)
    print("test case path:%s" % case_path)
    #  定义discover方法的参数
    discover = unittest.defaultTestLoader.discover(case_path, pattern=rule, top_level_dir=None)
    print(discover)
    return discover


def run_case(all_case, reportName="report"):
    '''
    执行所有的用例，并把结果写入HTML测试报告
    :param all_case:
    :param reportName:
    :return:
    '''
    now = time.strftime("%Y_%m_%d_%H_%M_%S")
    report_path = os.path.join(cur_path, reportName)
    if not os.path.exists(report_path): os.mkdir(report_path)
    report_adspath = os.path.join(report_path, now + "result.html")
    print("report path:%s" % report_adspath)
    fp = open(report_adspath, "wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'自动化测试报告', description=u'用例执行情况')
    runner.run(all_case)
    fp.close()


def get_report_file(report_path):
    """
    获取最新的测试报告
    :param report_path:
    :return:
    """
    lists = os.listdir(report_path)
    lists.sort(key=lambda fn: os.path.getmtime(os.path.join(report_path, fn)))
    print(u'最新生成的测试报告：' + lists[-1])
    #  找到最新生成的测试报告
    report_file = os.path.join(report_path, lists[-1])
    return report_file


def send_mail(sender, psw, receiver, smtpserver, report_file, port):
    """
    发送报告内容
    :param sender:
    :param psw:
    :param receiver:
    :param smtpserver:
    :param report_file:
    :param port:
    :return:
    """

    with open(report_file, "rb")as f:
        mail_body = f.read()
    # 定义邮件内容
    msg = MIMEMultipart()
    body = MIMEText(mail_body, _subtype='html', _charset='utf-8')
    msg['Subject'] = u"自动化测试报告"
    msg["from"] = sender
    msg["to"] = receiver
    msg.attach(body)
    # 添加附件
    att = MIMEText(open(report_file, "rb").read(), "base64", "utf-8")
    att["Content-Type"] = "application/octet_stream"
    att["Content-Disposition"] = 'attachment;filename="report.html"'
    msg.attach(att)
    try:
        smtp = smtplib.SMTP_SSL(smtpserver, port)
    except:
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver, port)
    #  用户名密码
    smtp.login(sender, psw)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    print('test report email has send out!')


if __name__ == "__main__":
    all_case = add_case()  # 加载用例
    #  生成测试报告路径
    run_case(all_case)  # 执行用例
    #  获取最新的测试报告文件
    report_path = os.path.join(cur_path, "report")  # 用例文件夹
    report_file = get_report_file(report_path)  # 获取最新测试报告
    # 邮箱配置
    sender = readConfig.sender
    psw = readConfig.psw
    smtp_server = readConfig.smtp_server
    port = readConfig.port
    receiver = readConfig.receiver
    send_mail(sender, psw, receiver, smtp_server, report_file, port)  # 发送报告
