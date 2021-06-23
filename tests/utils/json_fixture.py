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