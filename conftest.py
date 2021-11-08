import configparser
import pytest
import os
import pymysql.cursors
import requests
from tests.utils.json_fixture import JsonFixture
from tests.utils.variables import ClientAuth, ClientRegistration, Cart, OrdersHistory
from tests.utils.http_manager import HttpManager
import random
import allure


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
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'X-localization': 'ru'}
    result = HttpManager.post(ClientAuth.login_endpoint, body, headers=headers)
    return result


@pytest.fixture()
def create_account():
    body = JsonFixture.for_register_new_user('Main-Test', '0777777777', 'Qwerty123')
    response = HttpManager.post(ClientRegistration.reg_endpoint, body, headers=JsonFixture.get_header_without_token())
    return response


@pytest.fixture()
def get_product_balance(product_id=5010187):
    endpoint = 'https://api.platform.masterservice.company/api/v1/product/'
    headers = {
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


@pytest.fixture()
# не готова, запрос не хочет работать с библиотекой
def get_address_pick_up_guid(db_connect):
    db_connect.execute('SELECT guid FROM service_cities')
    city_guid_list = db_connect.fetchall()
    city_guid = random.choice(city_guid_list)["guid"]
    db_connect.execute('SELECT service_addresses.guid address_guid, service_addresses.name, '
                       'service_cities.name FROM service_addressesJOIN service_cities ON '
                       'service_addresses.city_id = service_cities.id '
                       'WHERE service_cities.guid = "2db80678-b4fb-11e3-abca-74d435146aa2"')
    data = db_connect.fetchall()
    return random.choice(data), city_guid


@pytest.fixture()
def get_max_page(auth):
    headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
    result = HttpManager.get(OrdersHistory.get_orders_endpoint, headers=headers)
    return result.json()['meta']['last_page']


@pytest.fixture()
def get_city_guid(db_connect):
    db_connect.execute('SELECT name, guid FROM service_cities')
    data = db_connect.fetchall()
    return data

@pytest.fixture()
def get_delivery_type(db_connect):
    db_connect.execute('SELECT name, guid FROM delivery_type')
    data = db_connect.fetchall()
    return data


