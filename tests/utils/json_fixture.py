import configparser

class JsonFixture:

    @staticmethod
    def for_register_new_user(name='main_test', login='0685340603', email='test@gmail.com', password='Qwert123'):
        json = {
            "name": name,
            "login": login,
            "email": email,
            "password": password
        }

    def for_register_new_user(name='main_test', email='test@gmail.com', phone='380685340603', password='Qwert123'):
        json = {
            "name": name,
            "email": email,
            "phone": phone,
            "password": password
        }
        return json

    @staticmethod
    def for_login_customers(phone='0685340603', password='33160900'):
        json = {
            "login": phone,
            "password": password
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
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-localization': 'ru'
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
                "type_guid": "f442a653-b32b-4be9-9b5e-4a5abb206d85",  # самовывоз
                "company_guid": "",
                "province_guid": "",
                "city_guid": "",
                "office_guid": "",
                "address_pickup_guid": "cacdaf1a-8638-11e7-a99d-a0369f7dce69",  # биологическая
                "address_delivery": ""},
            "payment_method": "d1e84b1a-e266-4a41-b553-0d030e40bc26",
            "comment": "Test Comment",
            "client_id": "",
            "currency_id": 980,
            "cart_id_hash": None
        }
        return order_data

    @staticmethod
    def order_by_click(phone="380990000000", product_id="5028837", attribute_id="", count="1", currency_id=980):
        order_data = {
            "phone": phone,
            "product_id": product_id,
            "attribute_id": attribute_id,
            "count": count,
            "currency_id": currency_id,
            "customer_id": ""
        }
        return order_data

    @staticmethod
    def b2c_info(first_name='Alex', last_name='Zhernoklev', middle_name='Alexandrovich'):
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'middle_name': middle_name
        }
        return data

    @staticmethod
    def delivery_address(name, delivery_type, pick_up_address, city_guid):
        data = {
            'name': name,
            'type_guid': delivery_type,
            'city_guid': city_guid,
            'address_pickup_guid': pick_up_address
        }
        return data