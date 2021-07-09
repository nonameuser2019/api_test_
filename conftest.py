import configparser
import pytest
import os
import pymysql.cursors
import requests
from tests.utils.json_fixture import JsonFixture
from tests.utils.variables import ClientAuth, ClientRegistration, Cart
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


@pytest.fixture()
def get_product_balance(product_id=5010187):
    endpoint = 'https://api.platform.masterservice.company/api/v1/product/'
    headers= {
        'Content-Type': 'application/json'
    }
    payload = {"id": product_id}
    response = requests.get(endpoint, headers=headers, params=payload)
    return int(response.json()["data"]["quantity"])


@pytest.fixture()
def create_cart_item(product_id=5010187, count=2):
    body = JsonFixture.product_data(product_id, "", count, "")
    response = HttpManager.post(Cart.add_cart_item_endpoint, body, JsonFixture.get_header_without_token())
    response_json = response.json()
    cart_id_hash = response_json['data']['cart_id_hash']
    cart_id = response_json['data']['id']
    return cart_id_hash, product_id, cart_id


@pytest.fixture(db_connect)
def get_adress_pick_up_guid(city):
    db_connect.execute('SELECT name, guid FROM service_addresses')
    data = db_connect.fetchall()
    for ad in data:
        if city in ad['name']:
            return ad['guid']





