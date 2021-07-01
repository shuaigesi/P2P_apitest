import json
import logging
import os
import pymysql
from bs4 import BeautifulSoup
import requests
import app

def assert_utils(self,response,status_code,status,desc):
    self.assertEquals(status_code, response.status_code)
    self.assertEquals(status, response.json().get("status"))
    self.assertEquals(desc, response.json().get("description"))

#解析第三方请求
def decode_third_request(form_data):
    # 解析form表单中的内容，提取第三方请求信息

    soup = BeautifulSoup(form_data, "html.parser")
    third_url = soup.form['action']
    logging.info("third_url = {}".format(third_url))
    data = {}
    for i in soup.find_all('input'):
        data[i['name']] = i['value']
        # data.setdefault(i['name'],i['value'])
    logging.info("data = {}".format(data))
    response = requests.post(url=third_url,data=data)
    return response

class  DButils():
    @classmethod
    def get_conn(cls,db_name):
        conn = pymysql.connect(host=app.DB_URL,database=db_name,port=app.DB_PORT,user=app.DB_USERNAME,password=app.DB_PWD,autocommit=True)
        return conn

    @classmethod
    def close(cls,cursor=None,conn=None):
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    @classmethod
    def delete(cls,db_name,sql):
        try:
            conn = cls.get_conn(db_name)
            cursor = conn.cursor()
            cursor.execute(sql)
        except Exception as e:
            conn.rollback()
        finally:
            cls.close(cursor,conn)

def build_get_img_data(file_name):
    file = app.BASE_DIR + "/data/"+ file_name
    testcase_data=[]
    with open(file,encoding="utf-8") as f :
        data = json.load(f)
        data_list = data.get("test_get_img_code")
        for test_data in data_list:
            testcase_data.append((test_data.get("type"),test_data.get("status_code")))
        print("json data={}".format(testcase_data))


    return testcase_data

def bulid_register_data(file_name):
    testcase_data = []
    file = app.BASE_DIR + "/data/"+ file_name
    with open(file,encoding="utf-8") as f:
        test_data = json.load(f)
        test_data_list = test_data.get("register_data")
        for test in test_data_list:
            testcase_data.append((test.get("phone"),test.get("password"),test.get("verifycode"),test.get("phone_code"),test.get("dy_server"),test.get("invite_phone"),test.get("status_code"),test.get("status"),test.get("description")))
        print("register json data = {}".format(testcase_data))
        return testcase_data

def bulid_data(file_name,json_name,test_param):
    file = app.BASE_DIR +"/data/"+file_name
    with open(file,encoding="utf-8") as f:
        dict_data = json.load(f)
        test_case_data =[]
        for test_data in dict_data.get(json_name):
            test = []
            for param in test_param.split(","):
                test.append(test_data.get(param))
            test_case_data.append(test)
    print(test_case_data)
    return test_case_data













