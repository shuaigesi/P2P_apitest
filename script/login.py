import random
import unittest
from asyncio import sleep

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

    #参数为随机小数时获取图片验证码成功
    def test01_get_img_code_random_float(self):
        r = random.random()
        response = self.login_api.getImgCode(self.session,str(r))
        logging.info("随机小数获取图片验证码测试结果：{}".format(response))
        print(response)
        self.assertEquals(200,response.status_code)

    #参数为随机整数时获取图片验证码成功
    def test02_get_img_code_random_int(self):
        r = random.randint(10000000,90000000)
        response = self.login_api.getImgCode(self.session, str(r))
        logging.info("随机整数获取图片验证码测试结果：{}".format(response))
        print(response)
        self.assertEquals(200, response.status_code)

    #参数为空时，获取图片验证码失败
    def test03_get_img_code_param_is_null(self):
        response = self.login_api.getImgCode(self.session,"" )
        logging.info("参数为空时，获取图片验证码失败测试结果：{}".format(response))
        print(response.status_code)
        self.assertEquals(404, response.status_code)

    #参数为字母时，获取图片验证码失败
    def test04_get_img_code_random_char(self):
        r = random.sample("abcdefghijklmno",8)
        rand = '.'.join(r)
        response = self.login_api.getImgCode(self.session, rand)
        logging.info("参数为字母时，获取图片验证码失败测试结果：{}".format(response))
        print(response)
        self.assertEquals(400, response.status_code)

    #获取短信验证码成功 - 参数正确
    def test05_get_sms_code_success(self):
        #获取图片验证码
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEquals(200, response.status_code)
        #获取短信验证码
        response = self.login_api.getSmsCode(self.session,self.phone1,self.img_code)
        logging.info("获取短信验证码成功 - 参数正确测试结果：{}".format(response))
        assert_utils(self,response,200,200,"短信发送成功")


    #获取短信验证码失败 - 图片验证码错误
    def test06_get_sms_code_imgcode_is_wrong(self):
        r = random.random()
        response = self.login_api.getImgCode(self.session,str(r))
        self.assertEquals(200, response.status_code)
        error_img_code = '6666'
        response = self.login_api.getSmsCode(self.session,self.phone1,error_img_code)
        logging.info("获取短信验证码失败 - 图片验证码错误:{}".format(response.json()))
        assert_utils(self,response,200,100,"图片验证码错误")

    #获取短信验证码失败，图片验证码为空
    def test07_get_sms_code_imgcode_is_null(self):
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEquals(200, response.status_code)
        empty_img_code = ''
        response = self.login_api.getSmsCode(self.session, self.phone1, empty_img_code)
        logging.info("获取短信验证码失败，图片验证码为空:{}".format(response.json()))
        assert_utils(self, response, 200, 100, "图片验证码错误")

    #获取短信验证码失败，图片手机号为空
    def test08_get_sms_code_phone_is_null(self):
        r = random.random()
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEquals(200, response.status_code)
        empty_phone = ''
        response = self.login_api.getSmsCode(self.session, empty_phone, self.img_code)
        logging.info("获取短信验证码失败，图片手机号为空:{}".format(response.json()))
        self.assertEquals(200,response.status_code)
        self.assertEquals(100,response.json().get("status"))

    #获取短信验证码失败，不调用获取图片验证码接口
    def test09_get_sms_code_success(self):
        response = self.login_api.getSmsCode(self.session, self.phone1, self.img_code)
        logging.info("获取短信验证码失败，不调用获取图片验证码接口：{}".format(response))
        assert_utils(self, response, 200, 100, "图片验证码错误")

    #注册成功，输入必填项
    def test10_register_success_param_must(self):
        r = random.random()
        #获取图片验证码
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEquals(200, response.status_code)
        # 获取短信验证码
        response = self.login_api.getSmsCode(self.session, self.phone1, self.img_code)
        assert_utils(self, response, 200, 200, "短信发送成功")
        #注册
        response = self.login_api.register(self.session,self.phone1,self.password)
        logging.info("注册成功，输入必填项的测试结果：{}".format(response.json()))
        assert_utils(self,response,200,200,"注册成功")

    #注册成功，输入所有参数项
    def test11_register_success_param_all(self):
        r = random.random()
        #获取图片验证码
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEquals(200, response.status_code)
        # 获取短信验证码
        response = self.login_api.getSmsCode(self.session, self.phone2, self.img_code)
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 注册
        response = self.login_api.register(self.session, self.phone2, self.password,invite_phone='13112711111')
        logging.info("注册成功，输入所有参数项：{}".format(response.json()))
        assert_utils(self, response, 200, 200, "注册成功")

    # 注册失败，手机号已存在
    def test12_register_phone_is_exist(self):
        r = random.random()
        #获取图片验证码
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEquals(200, response.status_code)
        # 获取短信验证码
        response = self.login_api.getSmsCode(self.session, self.phone1, self.img_code)
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 注册
        response = self.login_api.register(self.session, self.phone1, self.password)
        logging.info("注册失败，手机号已存在：{}".format(response.json()))
        assert_utils(self, response, 200, 100, "手机已存在!")

    #注册失败，密码为空
    def test13_register_password_is_null(self):
        r = random.random()
        #获取图片验证码
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEquals(200, response.status_code)
        # 获取短信验证码
        response = self.login_api.getSmsCode(self.session, self.phone3, self.img_code)
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 注册
        response = self.login_api.register(self.session, self.phone3,"")
        logging.info("注册失败，密码为空：{}".format(response.json()))
        assert_utils(self, response, 200, 100, "密码不能为空")

    #注册失败，图片验证码错误
    def test14_register_img_code_is_wrong(self):
        r = random.random()
        #获取图片验证码
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEquals(200, response.status_code)
        # 获取短信验证码
        response = self.login_api.getSmsCode(self.session, self.phone4, self.img_code)
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 注册
        response = self.login_api.register(self.session, self.phone4,self.password,"1234")
        logging.info("注册失败，图片验证码错误：{}".format(response.json()))
        assert_utils(self, response, 200, 100, "验证码错误!")

    # 注册失败，短信验证码错误
    def test15_register_phone_code_is_wrong(self):
        r = random.random()
        #获取图片验证码
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEquals(200, response.status_code)
        # 获取短信验证码
        response = self.login_api.getSmsCode(self.session, self.phone4, self.img_code)
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 注册
        response = self.login_api.register(self.session, self.phone4, self.password,self.img_code,"123456")
        logging.info("注册失败，图片验证码错误：{}".format(response.json()))
        assert_utils(self, response, 200, 100, "验证码错误")

    #注册失败,不同意条款协议
    def test16_register_no_agree_protocol(self):
        r = random.random()
        # 获取图片验证码
        response = self.login_api.getImgCode(self.session, str(r))
        self.assertEquals(200, response.status_code)
        # 获取短信验证码
        response = self.login_api.getSmsCode(self.session, self.phone4, self.img_code)
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 注册
        response = self.login_api.register(self.session, self.phone4, self.password, self.img_code,dy_server='off')
        logging.info("注册失败,不同意条款协议：{}".format(response.json()))
        assert_utils(self, response, 200, 100, "请同意我们的条款")

    #登录成功
    def test17_login_success(self):
        response = self.login_api.login(self.session)
        logging.info("登录成功：{}".format(response.json()))
        assert_utils(self,response,200,200,"登录成功")

    #登录失败，用户不存在
    def test18_login_phone_not_exist(self):
        Wphone = '12236549852'
        response = self.login_api.login(self.session,Wphone)
        logging.info("登录失败，用户不存在：{}".format(response.json()))
        assert_utils(self, response, 200, 100, "用户不存在")

    #登录失败，密码为空
    def test19_login_password_is_empty(self):
        response = self.login_api.login(self.session,password="")
        logging.info("登录失败，密码为空：{}".format(response.json()))
        assert_utils(self, response, 200, 100, "密码不能为空")

    # 登录失败，密码错误
    # 登录失败，第二次
    # 登录失败，锁定一分钟
    # 登录成功，等60秒后登录输入正确手机、密码
    def test20_login_password_is_wrong(self):
        response = self.login_api.login(self.session,password="123")
        logging.info("登录第一次失败：{}".format(response.json()))
        assert_utils(self, response, 200, 100, "密码错误1次,达到3次将锁定账户")
        response = self.login_api.login(self.session, password="123")
        logging.info("登录第二次失败：{}".format(response.json()))
        assert_utils(self, response, 200, 100, "密码错误2次,达到3次将锁定账户")
        response = self.login_api.login(self.session, password="123")
        logging.info("登录第三次失败：{}".format(response.json()))
        assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
        time.sleep(60)
        response = self.login_api.login(self.session)
        logging.info("60s后登录成功：{}".format(response.json()))
        assert_utils(self, response, 200, 200, "登录成功")


