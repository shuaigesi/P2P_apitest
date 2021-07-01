import random
import unittest
from asyncio import sleep
from parameterized import parameterized
from utils import build_get_img_data
from utils import bulid_register_data
from utils import bulid_data

import requests
import logging

import time

from utils import assert_utils
from api.loginAPI import loginAPI
class login(unittest.TestCase):
    phone1 = '13112711112'
    phone2 = '13112711113'
    phone3 = '13112711114'
    phone4 = '13112711115'
    phone5 = '13112711116'
    password = 'test123456'
    img_code = '8888'


    def setUp(self):
        self.login_api = loginAPI()
        self.session = requests.session()

    def tearDown(self):
        self.session.close()

    #获取图片验证码参数化
    # @parameterized.expand(build_get_img_data("imgVerify.json"))
    @parameterized.expand(bulid_data("imgVerify.json","test_get_img_code","type,status_code"))
    def test01_get_verify_imgcode(self,type,status_code):
        r = ''
        if type == 'float':
            r = random.random()
        elif type == 'int':
            r = random.randint(100000000,900000000)
        elif type =='char':
            r = random.sample('abcdefghijklmn',8)
        response = self.login_api.getImgCode(self.session,str(r))
        logging.info("测试结果:{}".format(response))
        self.assertEquals(status_code,response.status_code)

    # @parameterized.expand(bulid_register_data("register.json"))
    @parameterized.expand(bulid_data("register.json", "register_data","phone,password,verifycode,phone_code,dy_server,invite_phone,status_code,status,description"))
    def test02_register(self,phone,password,verifycode,phone_code,dy_server,invite_phone,status_code,status,description):
        #获取图片验证码
        response = self.login_api.getImgCode(self.session,str(random.random()))
        logging.info("获取图片验证码:{}".format(response))
        self.assertEquals(200, response.status_code)
        #获取手机验证码
        response = self.login_api.getSmsCode(self.session,phone,"8888")
        logging.info("获取手机验证码:{}".format(response.json()))
        assert_utils(self, response, 200, 200, "短信发送成功")
        #注册
        response = self.login_api.register(self.session,phone,password,verifycode,phone_code,dy_server,invite_phone)
        logging.info("注册:{}".format(response.json()))
        assert_utils(self,response,status_code,status,description)


