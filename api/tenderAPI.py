import app
class tenderAPI():
    def __init__(self):
        self.tender_url = app.BASE_URL + "/trust/trust/tender"
        self.tenderlist_url = app.BASE_URL +"/loan/tender/mytenderlist"
        self.tenderinfo_url = app.BASE_URL + "/common/loan/loaninfo"

    def tender(self,session,id="1101",amount="100",password="123456"):
        data = {"id":id,
                "depositCertificate":"-1",
                "amount":amount,
                "password":password}
        response = session.post(self.tender_url,data)
        return response

    def get_tenderlist(self,session,status="tender"):
        data = {"status":status}
        response = session.post(self.tenderlist_url)
        return response

    def get_tenderinfo(self,session,id="1101"):
        data = {"id":id }
        response = session.post(self.tenderinfo_url,data)
        return response