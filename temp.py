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
# cursor = connection.cursor()
# cursor.execute('SELECT name, email, phone FROM customers WHERE id=19392')
# data = cursor.fetchall()
# print(data[0]['email'])
# connection.commit()


# body = JsonFixture.for_login_customers()
# headers = {'Content-Type': 'application/json'}
# result = requests.post(ClientAuth.login_endpoint, json=body, headers=headers)
# print(result.status_code)

parser = configparser.ConfigParser()
parser.read('test_data.ini')
name = parser.get('users_data', 'name')
print(name)
parser.set('users_data', 'name', 'alex')
name = parser.get('users_data', 'name')
print(name)
