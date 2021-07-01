import  unittest
from lib.HTMLTestRunner_PY3 import HTMLTestRunner
import time

from script.login import login
from script.approve import approve
from script.tender import tender
from script.trust import trust
from script.tender_process import tenderProcess
import app

suite = unittest.TestSuite()
suite.addTest(unittest.makeSuite(login))
suite.addTest(unittest.makeSuite(approve))
suite.addTest(unittest.makeSuite(trust))
suite.addTest(unittest.makeSuite(tender))
suite.addTest(unittest.makeSuite(tenderProcess))

report_file = app.BASE_DIR + "/report/report{}.html".format(time.strftime("%Y%m%d-%H%M%S"))
with open(report_file,'wb') as f :
    runner = HTMLTestRunner(f,title="p2p金融项目接口测试报告",description="test")
    runner.run(suite)

