import configparser
import pytest
import os
import pymysql.cursors
import requests
from tests.utils.json_fixture import JsonFixture
from tests.utils.variables import ClientAuth, ClientRegistration
from tests.utils.http_manager import HttpManager


@pytest.fixture()
def db_connect():
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
    try:
        with connection.cursor() as cursor:
            yield cursor
            print('\nSuccessful connection to database')
    finally:
        connection.commit()
        connection.close()
        print('\nClosed db connect')

@pytest.fixture()
def auth():
    body = JsonFixture.for_login_customers()
    headers = {'Content-Type': 'application/json'}
    result = requests.post(ClientAuth.login_endpoint, json=body, headers=headers)
    return result

@pytest.fixture()
def create_account():
    body = JsonFixture.for_register_new_user('Main-Test', '0777777777', 'Qwerty123')
    response = HttpManager.post(ClientRegistration.reg_endpoint, body, headers=JsonFixture.get_header_without_token())
    return response

