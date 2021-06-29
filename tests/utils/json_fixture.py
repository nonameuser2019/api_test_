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
