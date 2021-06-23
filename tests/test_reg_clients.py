from tests.utils.json_fixture import JsonFixture
from tests.utils.variables import ClientRegistration
from tests.utils.http_manager import HttpManager
import requests
import pytest


class TestRegistrationNewUser:

    @pytest.mark.smoke
    def test_reg_with_valid_param(self, db_connect):
        body = JsonFixture.for_register_new_user("AlexTest")
        result = HttpManager.post(ClientRegistration.register, body)
        response_json = result.json()
        db_connect.execute('DELETE FROM customers WHERE phone="0685340603"')
        assert result.status_code == 200, f'Registration failed, response from the server: {response_json["message"]}'
        assert response_json['success'], f'Registration failed, response from the server:: {response_json["message"]}'

    @pytest.mark.smoke
    @pytest.mark.parametrize('name, res', ClientRegistration.name_list)
    def test_reg_with_different_names(self, db_connect, name, res):
        body = JsonFixture.for_register_new_user(name)
        result = HttpManager.post(ClientRegistration.register, body)
        response_json = result.json()
        #assert result.status_code == 200, f'Registration failed, response from the server: {response_json["message"]}'
        assert response_json['success'] == res, f'Registration failed, response from the server:: {response_json["message"]}'
        db_connect.execute(f"DELETE FROM customers WHERE phone={body['data']['login']}")

    @pytest.mark.smoke
    def test_check_reg_with_empty_all_param(self, db_connect):
        body = JsonFixture.for_register_new_user("", "", "")
        result = HttpManager.post(ClientRegistration.register, body)
        response_json = result.json()
        assert result.status_code == 400, f'Registration failed, response from the server: {response_json["message"]}'
        assert not response_json['success'], f'Registration failed, response from the server:: {response_json["message"]}'
        db_connect.execute('DELETE FROM customers WHERE phone="0685340603"')

    @pytest.mark.smoke
    def test_reg_with_empty_login(self, db_connect):
        body = JsonFixture.for_register_new_user('Alex', "")
        result = HttpManager.post(ClientRegistration.register, body)
        response_json = result.json()
        assert result.status_code == 400, f'Registration failed, response from the server: {response_json["message"]}'
        assert not response_json['success'], f'Registration failed, response from the server:: {response_json["message"]}'
        db_connect.execute('DELETE FROM customers WHERE phone="0685340603"')

    @pytest.mark.smoke
    def test_reg_with_empty_password(self, db_connect):
        body = JsonFixture.for_register_new_user(password="")
        result = HttpManager.post(ClientRegistration.register, body)
        response_json = result.json()
        assert result.status_code == 400, f'Registration failed, response from the server: {response_json["message"]}'
        assert not response_json['success'], f'Registration failed, response from the server:: {response_json["message"]}'
        db_connect.execute('DELETE FROM customers WHERE phone="0685340603"')

    @pytest.mark.smoke
    def test_reg_with_empty_body(self, db_connect):
        body = {
            "data":{}
        }
        result = HttpManager.post(ClientRegistration.register, body)
        response_json = result.json()
        assert result.status_code == 400, f'Registration failed, response from the server: {response_json["message"]}'
        assert not response_json['success'], f'Registration failed, response from the server:: {response_json["message"]}'
        db_connect.execute('DELETE FROM customers WHERE phone="0685340603"')

    @pytest.mark.test
    @pytest.mark.smoke
    @pytest.mark.parametrize('phone, res', ClientRegistration.phone_list)
    def test_reg_with_different_phones(self, db_connect, phone, res):
        body = JsonFixture.for_register_new_user(login=phone)
        result = HttpManager.post(ClientRegistration.register, body)
        response_json = result.json()
        assert response_json['success'] == res, f'Registration failed, response from the server:: {response_json["message"]}'
        db_connect.execute(f"DELETE FROM customers WHERE phone='0685340603'")
