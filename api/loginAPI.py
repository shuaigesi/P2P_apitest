import app
import requests

class loginAPI():
    def __init__(self):
        self.getImgCode_url = app.BASE_URL+"/common/public/verifycode1/"
        self.getSmsCode_url = app.BASE_URL+"/member/public/sendSms"
        self.register_url = app.BASE_URL + "/member/public/reg"
        self.login_url = app.BASE_URL + "/member/public/login"



    def getImgCode(self,session,r):
        response = session.get(url=self.getImgCode_url+ r )
        return response

    def getSmsCode(self,session,phone,imgVerifyCode):
        data = {"phone":phone,"imgVerifyCode":imgVerifyCode,"type":"reg"}
        response = session.post(url=self.getSmsCode_url,params = data)
        return response

    def register(self,session,phone,password,verifycode='8888',phone_code='666666',dy_server='on',invite_phone=''):
        data = {"phone":phone,
                "password":password,
                "verifycode":verifycode,
                "phone_code":phone_code,
                "dy_server":dy_server,
                "invite_phone":invite_phone}
        response = session.post(self.register_url,data=data)
        return response

    def login(self,session,phone='13112711112',password='test123456'):
        data = {"keywords":phone,"password":password}
        response = session.post(self.login_url,data)
        return response




