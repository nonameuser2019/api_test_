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
    def for_login_customers(login='0777777777', password='Qwerty123'):
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
