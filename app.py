import logging
import app
import os
from logging import handlers

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "http://user-p2p-test.itheima.net"

DB_URL = "121.43.169.97"
DB_PORT = 3306
DB_USERNAME = "root"
DB_PWD="Itcast_p2p_20191228"
DB_MEMBER ="czbk_member"
DB_FINANCE ="czbk_finance"


def init_log_config():
    #创建日志初始化对象
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    #创建控制台日志处理器和文件日志处理器
    sh = logging.StreamHandler()
    log_path = BASE_DIR + os.sep + "log" + os.sep + "p2p{}.log".format("%Y%m%D %H%M%S")
    fh = logging.handlers.TimedRotatingFileHandler(log_path,when='M',interval=5,backupCount=5,encoding='UTF-8')
    #设置日志格式，创建格式化器
    fmt = '%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s'
    formatter = logging.Formatter(fmt)
    #将格式化器设置到日志器中
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)
    # 将日志处理器添加到日志对象
    logger.addHandler(sh)
    logger.addHandler(fh)



