# coding:utf-8
"""
数据库配置
"""
import psycopg2
# from common import envs
import redis


class DataLoader:
    # env = envs.QA
    def __init__(self, env):
        self.env = env
        """

        :param env:
        """

        # 连接数据库
        self.sql_conn = psycopg2.connect(
            "dbname='%s' user='%s' host='%s' password='%s'" % (self.env.pg_user, self.env.pg_user, self.env.pg_host, self.env.pg_password))
        # 使用cursor()方法获取操作游标
        self.cur = self.sql_conn.cursor()
        # # 提交修改
        # com = sql_conn.commit()
        # # 回滚
        # roll = sql_conn.rollback()
        # # 关闭连接
        # clo = sql_conn.close()

        # 连接redis
        self.redis_conn = redis.Redis(
            host=self.env.redis_host,
            port=self.env.redis_port,
            password=self.env.redis_cridential,
            db=self.env.redis_db)


