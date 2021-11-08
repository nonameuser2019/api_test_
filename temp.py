import configparser
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
order_id = cursor.execute('SELECT pc.name, pc.category_id, pc.url, pc.guid FROM product_category pc JOIN '
                          'product_category_parent pcp ON pcp.category_guid = pc.guid WHERE pcp.parent_guid IN '
                          '(SELECT pc.guid FROM product_category pc JOIN product_category_parent '
                          'pcp ON pcp.category_guid = pc.guid WHERE pcp.parent_guid = '
                          '("65551dd2-19ea-11eb-a9c0-509a4ca97563")) OR pcp.parent_guid = "65551dd2-19ea-11eb-a9c0-509a4ca97563"')
data = cursor.fetchall()
print(data)




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