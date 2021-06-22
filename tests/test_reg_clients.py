from tests.utils.json_fixture import JsonFixture
from tests.utils.variables import ClientRegistration
from tests.utils.http_manager import HttpManager
import requests
import pytest

class TestRegistrationNewUser:

    @pytest.mark.test
    @pytest.mark.smoke
    def test_reg_with_valid_param(self, db_connect):
        body = JsonFixture.for_register_new_user("AlexTest", "0685340262", "Qwerty123")
        result = HttpManager.post(ClientRegistration.register, body)
        response_json = result.json()
        db_connect.execute('DELETE FROM customers WHERE phone="0685340262"')
        assert result.status_code == 200, f'Response form the server: {response_json["message"]}'
        assert response_json['success'], f'Response form the server: {response_json["message"]}'

    @pytest.mark.smoke
    def test_reg_with_empty_name(self):
        body = JsonFixture.for_register_new_user("", "0685340262", "Qwerty123")
        result = HttpManager.post(ClientRegistration.register, body)
        response_json = result.json()
        assert result.status_code == 200, f'Response form the server: {response_json["message"]}'
        assert response_json['success'], f'Registration faild success=false'
