import unittest
import requests
import logging
from utils import assert_utils,decode_third_request
from api.loginAPI import loginAPI
from api.tenderAPI import tenderAPI
class tender(unittest.TestCase):
    def setUp(self):
        self.login_api = loginAPI()
        self.tender_api = tenderAPI()
        self.session = requests.session()
    def tearDown(self):
        self.session.close()

    #投资成功
    def test01_tender_success(self):
        #登录
        response = self.login_api.login(self.session)
        logging.info("login :{}".format(response.json()))
        assert_utils(self,response,200,200,"登录成功")
        #投资
        response = self.tender_api.tender(self.session)
        logging.info("投资 :{}".format(response.json()))
        self.assertEquals(200,response.status_code)
        self.assertEquals(200,response.json().get("status"))
        form_data = response.json().get("description").get("form")
        #发送第三方投资请求
        response =  decode_third_request(form_data)
        logging.info("发送第三方投资请求:{}".format(response.text))
        self.assertEquals(200,response.status_code)
        self.assertEquals("InitiativeTender OK",response.text)

    #获取投资列表
    def test02_get_tender_list(self):
        # 登录
        response = self.login_api.login(self.session)
        logging.info("login :{}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        #查看投资列表
        response = self.tender_api.get_tenderlist(self.session)
        logging.info("查看投资列表:{}".format(response.json()))
        self.assertEquals(200,response.status_code)

        self.assertEquals("2",response.json().get("isCert"))

    #获取投资产品详情
    def test03_get_tender_info(self):
        # 登录
        response = self.login_api.login(self.session)
        logging.info("login :{}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        #查看投资产品详情
        response = self.tender_api.get_tenderinfo(self.session)
        logging.info("查看投资产品详情:{}".format(response.json()))
        assert_utils(self,response,200,200,'OK')
        self.assertEqual('1101', response.json().get("data").get("loan_info").get("id"))


