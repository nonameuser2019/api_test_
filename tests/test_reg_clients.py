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
        db_connect.execute('DELETE FROM customers WHERE phone="0685340262"')
        assert result.status_code == 200, f'Registration failed, response from the server: {response_json["message"]}'
        assert response_json['success'], f'Registration failed, response from the server:: {response_json["message"]}'

    @pytest.mark.smoke
    def test_reg_with_name_of_latin_letters(self, db_connect):
        pass


    @pytest.mark.smoke
    def test_reg_with_empty_name(self):
        body = JsonFixture.for_register_new_user("")
        result = HttpManager.post(ClientRegistration.register, body)
        response_json = result.json()
        assert result.status_code == 400, f'Response from the server: {response_json["message"]}'
        assert not response_json['success'], f'Response from the server: {response_json["success"]}'

    @pytest.mark.test
