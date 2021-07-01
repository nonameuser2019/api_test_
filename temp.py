import configparser
import pytest
import os
import pymysql.cursors
import configparser
import pytest
import os
import pymysql.cursors
import requests
from tests.utils.json_fixture import JsonFixture
from tests.utils.variables import ClientAuth
import bcrypt
from tests.utils.json_fixture import JsonFixture


thisfolder = os.path.dirname(os.path.abspath(__file__))
inifile = os.path.join(thisfolder, 'db.ini')
parser = configparser.ConfigParser()
parser.read(inifile)

HOST = parser.get('db', 'host')
PORT = int(parser.get('db', 'port'))
DB_NAME = parser.get('db', 'db_name')
USER_NAME = parser.get('db', 'user_name')
DB_PASSWORD = parser.get('db', 'db_password')

connection = pymysql.connect(host=HOST,
                             port=PORT,
                             user=USER_NAME,
                             password=DB_PASSWORD,
                             db=DB_NAME,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()
cursor.execute('SELECT id FROM cart_temp')
data = cursor.fetchall()
print(data)
connection.commit()


# body = JsonFixture.for_login_customers()
# headers = {'Content-Type': 'application/json'}
# result = requests.post(ClientAuth.login_endpoint, json=body, headers=headers)
# print(result.status_code)



#get response form add card item
# endpoint = 'https://api.platform.masterservice.company/api/v1/cart/'
# body = JsonFixture.product_data(None, "", 2, "")
# headers = {'Content-Type': 'application/json'}
# response = requests.post(endpoint, json=body, headers=headers)
# print(response.status_code)
# response_json = response.json()
# print(response_json)
# print(body)


# endpoint = 'https://api.platform.masterservice.company/api/v1/product/'
# headers= {
#     'Content-Type': 'application/json'
# }
# product_id = 5010187
# payload = {"id": product_id}
# response = requests.get(endpoint, headers=headers, params=payload)
# print(response)
# print(response.json()["data"]["quantity"])