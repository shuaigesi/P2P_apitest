import unittest
import requests
import logging
from api.approveAPI import approveAPI
from api.loginAPI import loginAPI
from utils import assert_utils
from bs4 import BeautifulSoup
class approve(unittest.TestCase):

    realname = "张三"
    id_card = "110101200803071018"
    phone1 = '13112711112'
    phone2 = '13112711113'
    password = 'test123456'

    def setUp(self):
        self.login_api = loginAPI()
        self.approve_api = approveAPI()
        self.session = requests.session()
    def tearDown(self):
        self.session.close()

    #认证成功
    def test01_approve_success(self):
        #登录
        response = self.login_api.login(self.session)
        logging.info("登录成功测试结果为：{}".format(response.json()))
        assert_utils(self,response,200,200,"登录成功")
        #认证
        response = self.approve_api.approve(self.session,self.realname,self.id_card)
        logging.info("认证成功测试结果为：{}".format(response.json()))
        assert_utils(self,response,200,200,"提交成功!")

    #认证失败-姓名为空
    def test02_approve_realname_is_empty(self):
        response = self.login_api.login(self.session,self.phone2)
        logging.info("认证失败-姓名为空测试结果为：{}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        # 认证
        response = self.approve_api.approve(self.session, "", self.id_card)
        logging.info("认证成功测试结果为：{}".format(response.json()))
        assert_utils(self, response, 200, 100, "姓名不能为空")

    # 认证失败-身份证号为空
    def test03_approve_idcard_is_empty(self):
        #登录
        response = self.login_api.login(self.session,self.phone2)
        logging.info("登录成功测试结果为：{}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        # 认证
        response = self.approve_api.approve(self.session, self.realname, "")
        logging.info("认证失败-身份证号为空测试结果为：{}".format(response.json()))
        assert_utils(self, response, 200, 100, "身份证号不能为空!")

    #获取认证信息
    def test04_get_approve(self):
        # 登录
        response = self.login_api.login(self.session)
        logging.info("登录成功测试结果为：{}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")
        # 获取认证信息
        response = self.approve_api.getapprove(self.session)
        logging.info("获取认证信息测试结果为：{}".format(response.json()))
        self.assertEquals(200,response.status_code)
        self.assertIn("张**",response.json().get("realname"))

