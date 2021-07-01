import app
class trustAPI():
    def __init__(self):
        self.trust_register_url = app.BASE_URL +"/trust/trust/register"
        self.get_recharge_code_url = app.BASE_URL + "/common/public/verifycode/"
        self.get_recharge_url = app.BASE_URL + "/trust/trust/recharge"

    def trust_register(self,session):
        response = session.post(self.trust_register_url)
        return response

    def get_img_recharge_code(self,session,r):
        url = self.get_recharge_code_url + r
        response = session.get(url)
        return response

    def get_recharge(self,session,amount="2000",valicode="8888"):
        data = {"paymentType":"chinapnrTrust",
                "amount":amount,
                "formStr":"reForm",
                "valicode":valicode}
        response = session.post(self.get_recharge_url,data)
        return response


