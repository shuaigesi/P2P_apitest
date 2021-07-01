import random
import unittest
import logging
from utils import assert_utils,decode_third_request,DButils
import app
import requests

from api.approveAPI import approveAPI
from api.loginAPI import loginAPI
from api.tenderAPI import tenderAPI
from api.trustAPI import trustAPI

class tenderProcess(unittest.TestCase):
    phone = '13112711116'
    tender_id = 1101
    imVerifyCode = '8888'


    @classmethod
    def setUpClass(cls):
        cls.aprove_api = approveAPI()
        cls.login_api = loginAPI()
        cls.tender_api = tenderAPI()
        cls.trust_api = trustAPI()
        cls.session = requests.session()

    @classmethod
    def tearDownClass(cls):
        cls.session.close()
        sql1="delete from mb_member_register_log where phone = '13112711112' or phone = '13112711113' or phone = '13112711114' or phone = '13112711115' or phone = '13112711116' or phone = '13112711117';"
        DButils.delete(app.DB_MEMBER,sql1)
        logging.info("delete sql1:{}".format(sql1))
        sql2="delete i.* from mb_member_login_log i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone = '13112711112' or m.phone = '13112711113' or m.phone = '13112711114' or m.phone = '13112711115' or phone = '13112711116' or phone = '13112711117';"
        DButils.delete(app.DB_MEMBER, sql2)
        logging.info("delete sql2:{}".format(sql2))
        sql3="delete i.* from mb_member_info i INNER JOIN mb_member m on i.member_id = m.id WHERE m.phone = '13112711112' or m.phone = '13112711113' or m.phone = '13112711114' or m.phone = '13112711115' or phone = '13112711116' or phone = '13112711117';"
        DButils.delete(app.DB_MEMBER, sql3)
        logging.info("delete sql3:{}".format(sql3))
        sql4="delete  from mb_member WHERE phone = '13112711112' or phone = '13112711113' or phone = '13112711114' or phone = '13112711115' or phone = '13112711116' or phone = '13112711117';"
        DButils.delete(app.DB_MEMBER, sql4)
        logging.info("delete sql4:{}".format(sql4))
    def test01_register_success(self):
        # 请求图片验证码
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 请求短信验证码
        response = self.login_api.getSmsCode(self.session, self.phone, self.imVerifyCode)
        logging.info("sms verify response={}".format(response.json()))
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 发送注册请求
        response = self.login_api.register(self.session, self.phone, 'test123456')
        logging.info("reg response={}".format(response.json()))
        # 断言
        assert_utils(self, response, 200, 200, "注册成功")

    def test02_login_success(self):
        """登录成功"""
        # 发送登录请求
        response = self.login_api.login(self.session, self.phone, 'test123456')
        logging.info("login response={}".format(response.json()))
        # 断言
        assert_utils(self, response, 200, 200, "登录成功")

    def test03_trust_success(self):
        """开户"""
        # 获取开户信息
        response = self.trust_api.trust_register(self.session)
        logging.info("trust response={}".format(response.json()))
        # 断言获取的开户信息是否正确
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 获取开户信息响应中的HTML内容（为后续请求的地址和参数）
        form_data = response.json().get("description").get("form")
        logging.info("form response={}".format(form_data))
        # 发送第三方的请求，请求第三方接口进行开户
        response = decode_third_request(form_data)
        logging.info("third-interface response={}".format(response.text))
        # 断言第三方接口请求处理是否成功
        self.assertEqual('UserRegister OK', response.text)

    def test04_recharge_success(self):
        """充值"""
        # 获取充值验证码
        r = random.random()
        response = self.trust_api.get_img_recharge_code(self.session, str(r))
        self.assertEqual(200, response.status_code)
        logging.info("get_recharge_code response={}".format(response.text))

        # 充值
        amount = '1000'
        response = self.trust_api.get_recharge(self.session, amount)
        logging.info("recharge response={}".format(response.text))
        # 断言获取的开户信息是否正确
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 获取开户信息响应中的HTML内容（为后续请求的地址和参数）
        form_data = response.json().get("description").get("form")
        logging.info("form response={}".format(form_data))
        # 发送第三方的请求，请求第三方接口进行开户
        response = decode_third_request(form_data)
        logging.info("third-interface response={}".format(response.text))
        # 断言第三方接口请求处理是否成功
        self.assertEqual('NetSave OK', response.text)

    def test05_get_loaninfo(self):
        """获取投资产品详情"""
        # 请求投资产品的详情
        response = self.tender_api.get_tenderinfo(self.session, self.tender_id)
        logging.info("get_tender response = {}".format(response.json()))
        # 断言投资详情是否正确
        assert_utils(self, response, 200, 200, "OK")
        self.assertEqual('1101', response.json().get("data").get("loan_info").get("id"))

    def test06_tender(self):
        # 投资
        # 发送投资请求
        amount = '100'
        response = self.tender_api.tender(self.session, self.tender_id, amount)
        logging.info("tender response = {}".format(response.json()))
        # 断言投资结果是否正确
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 获取开户信息响应中的HTML内容（为后续请求的地址和参数）
        form_data = response.json().get("description").get("form")
        logging.info("form response={}".format(form_data))
        # 发送第三方的请求，请求第三方接口进行开户
        response = decode_third_request(form_data)
        logging.info("third-interface response={}".format(response.text))
        # 断言第三方接口请求处理是否成功
        self.assertEqual('InitiativeTender OK', response.text)

    def test07_get_tenderlist(self):
        """获取我的投资列表"""
        status = "tender"
        # 发送获取投资列表的请求
        response = self.tender_api.get_tenderlist(self.session, status)
        logging.info("get_tender response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
