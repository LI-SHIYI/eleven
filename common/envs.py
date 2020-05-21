class Env:
    """
    环境配置
    """
    http_base_url = ""
    redis_host = ""
    redis_port = 6379
    redis_cridential = "kktalkee"
    redis_db = 7
    pg_host = ""
    pg_user = "planet"
    pg_password = "planet/melotplanet"


class QA(Env):
    http_base_url = "http://10.4.4.140:10099"
    # http_base_url = "http://10.4.4.140:8905"
    redis_host = "10.4.4.176"
    pg_host = "10.4.4.219"
    pg_port = 5432


class Dev(Env):
    http_base_url = "http://10.4.3.232:10099"
    redis_host = ""
    redis_cridential = ""
    pg_schema = ""


class Beta(Env):
    http_base_url = "http://10.4.5.92:10099"
    redis_host = "10.4.5.139"
    pg_host = "10.4.5.58"
    pg_port = 6531
