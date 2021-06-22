class JsonFixture:

    @staticmethod
    def for_register_new_user(name, login, password):
        json = {
            "data": {
                "name": name,
                "login": login,
                "password": password}
        }
        return json