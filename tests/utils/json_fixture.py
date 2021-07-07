import configparser

class JsonFixture:

    @staticmethod
    def for_register_new_user(name='main_test', login='0685340603', password='Qwert123'):
        json = {
            "data": {
                "name": name,
                "login": login,
                "password": password}
        }
        return json

    @staticmethod
    def for_login_customers(login='0000000000', password='Qwerty123'):
        json = {
            "data": {
                "login": login,
                "password": password
            }
        }
        return json

    @staticmethod
    def get_headers(token):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+token
        }
        return headers

    @staticmethod
    def get_header_without_token():
        headers = {
            'Content-Type': 'application/json'
        }
        return headers

    @staticmethod
    def profile_data(email=None, phone=None, name=None, password=None):
        profile_data = {
            "data": {
                "email": email,
                "phone": phone,
                "name": name,
                "password": password
            }
        }
        return profile_data

    @staticmethod
    def product_data(product_id=None, attribute_id=None, count=None, client_id=None):
        product_data = {
            "product_id": product_id,
            "attribute_id": attribute_id,
            "count": count,
            "client_id": client_id
        }
        return product_data

    @staticmethod
    def del_prod_data(product_id=5010187, attribute_id=""):
        del_product_data = {
            "product_id": product_id,
            "attribute_id": attribute_id
        }
        return del_product_data

    @staticmethod
    def order_data():
        order_data = {
            "contact_details":{
                "name": "Test Customer",
                "phone": "0680000000",
                "email": "test@gmail.com",
                "res_name": "Test Customer",
                "res_phone": "0680000000"},
            "delivery": {
                "type_guid": "f442a653-b32b-4be9-9b5e-4a5abb206d85",
                "company_guid": "",
                "province_guid": "",
                "city_guid": "",
                "office_guid": "",
                "address_pickup_guid": "cacdaf1a-8638-11e7-a99d-a0369f7dce69",
                "address_delivery": ""},
            "payment_method": "d1e84b1a-e266-4a41-b553-0d030e40bc26",
            "comment": "Test Comment",
            "client_id": "",
            "currency_id": 980,
            "cart_id_hash": None
        }
        return order_data
