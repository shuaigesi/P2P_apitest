import random

from utils import assert_utils
from utils import decode_third_request
import unittest
import logging
import requests
from api.loginAPI import loginAPI
from api.trustAPI import trustAPI
from bs4 import BeautifulSoup

class trust(unittest.TestCase):
    def setUp(self):
        self.login_api = loginAPI()
        self.trust_api = trustAPI()
        self.session = requests.session()
    def tearDown(self):
        self.session.close()

    #开户请求
    def test01_trust_request(self):
        #登录
        response = self.login_api.login(self.session)
        logging.info("登录 = {}".format(response.json()))
        assert_utils(self,response,200,200,"登录成功")
        #发送开户请求
        response = self.trust_api.trust_register(self.session)
        logging.info("发送开户请求 = {}".format(response.json()))
        self.assertEquals(200,response.status_code)
        self.assertEquals(200,response.json().get("status"))
        #发送第三方的开户请求
        form_data = response.json().get("description").get("form")
        logging.info("form_data = {}".format(form_data))
        #发送第三方开户请求
        response = decode_third_request(form_data)
        self.assertEquals(200,response.status_code)
        self.assertEquals("UserRegister OK",response.text)

    def test02_recharge_request(self):
        #登录
        response = self.login_api.login(self.session)
        logging.info("登录 = {}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        #获取充值验证码
        r = random.random()
        response = self.trust_api.get_img_recharge_code(self.session,str(r))
        logging.info("get_img_recharge_code:{}".format(response))
        self.assertEquals(200,response.status_code)
        #充值
        response = self.trust_api.get_recharge(self.session)
        logging.info("充值请求:{}".format(response.json()))
        form_data = response.json().get("description").get("form")
        # 调用第三方接口
        response = decode_third_request(form_data)
        logging.info("调用第三方充值请求:{}".format(response.text))
        self.assertEquals(200, response.status_code)
        self.assertEquals("NetSave OK", response.text)




