import configparser
import datetime
import random

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
from datetime import datetime



# thisfolder = os.path.dirname(os.path.abspath(__file__))
# inifile = os.path.join(thisfolder, 'db.ini')
# parser = configparser.ConfigParser()
# parser.read(inifile)
#
# HOST = parser.get('db', 'host')
# PORT = int(parser.get('db', 'port'))
# DB_NAME = parser.get('db', 'db_name')
# USER_NAME = parser.get('db', 'user_name')
# DB_PASSWORD = parser.get('db', 'db_password')
#
# connection = pymysql.connect(host=HOST,
#                              port=PORT,
#                              user=USER_NAME,
#                              password=DB_PASSWORD,
#                              db=DB_NAME,
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)
# email = "test@gmail.com"
# phone = "380685340603"
# cursor = connection.cursor()
# cursor.execute('SELECT * FROM customers WHERE phone = "{}" OR email = "{}"'.format(phone, email))
# data = cursor.fetchall()
# print(data)




# def get_adress_guid(adress):
#     cursor = connection.cursor()
#     cursor.execute('SELECT name, guid FROM service_addresses')
#     data = cursor.fetchall()
#     for ad in data:
#         if adress in ad['name']:
#             return ad['guid']
#
# def get_all_adresses_guid():
#     cursor = connection.cursor()
#     cursor.execute('SELECT name, guid FROM service_addresses')
#     data = cursor.fetchall()
#     adress_list = []
#     for ad in data:
#         adress_list.append(ad['guid'])
#     return adress_list




# connection.commit()
# body = JsonFixture.order_data()
# body['delivery']['address_pickup_guid'] = get_adress_guid('Харьков')
# print(body['delivery']['address_pickup_guid'])




# data = JsonFixture.order_data()
# print(data)
# data['delivery'].pop('type_guid')
# print(data)

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

endpoint = 'https://api.platform.masterservice.company/api/v1/login'
get_endpoint = 'https://api.platform.masterservice.company/api/v1/orders'
body = {
    'login': '0685340603',
    'password': '33160900'
}
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'X-localization': 'ru'}
payload = {'search': '452'}
result = requests.post(endpoint, json=body, headers=headers)
token = result.json()['data']['access_token']
headers['Authorization'] = 'Bearer ' + token
result = requests.get(get_endpoint, json=body, headers=headers)

date_1 = result.json()['data'][0]['date'].split()[0]
print(date_1)
clear_date = datetime.strptime(date_1, '%Y-%m-%d')
print(clear_date)
