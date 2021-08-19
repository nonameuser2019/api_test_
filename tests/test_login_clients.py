from tests.utils.json_fixture import JsonFixture
from tests.utils.variables import ClientAuth
from tests.utils.http_manager import HttpManager
from tests.utils.error_messages import ErrorMessages
import pytest
import pytest_check as check

class TestAuthCustomers:

    @pytest.mark.test
    @pytest.mark.smoke
    def test_sign_in_with_valid_params(self):
        body = JsonFixture.for_login_customers()
        result = HttpManager.post(ClientAuth.login_endpoint, body, headers=JsonFixture.get_header_without_token())
        check.equal(result.status_code, 200), ErrorMessages.status_code_error(200, result.status_code)
        check.equal(result.json()['success'], True), ErrorMessages.succ_mess_error(True, result.json()['success'])


    @pytest.mark.smoke
    def test_sign_in_with_login_is_email(self):
        body = JsonFixture.for_login_customers('main_test@qa.com', 'Qwerty123')
        result = HttpManager.post(ClientAuth.login_endpoint, body, headers=JsonFixture.get_header_without_token())
        response_json = result.json()
        assert result.status_code == 200 and response_json['success'] and response_json[
            'message'] == 'Login successful', \
            f'Log in is wrong. Message from server {response_json["message"]}'



    @pytest.mark.smoke
    def test_sign_in_with_confused_login_and_password(self):
        body = JsonFixture.for_login_customers(login='Qwerty123', password='0777777777')
        result = HttpManager.post(ClientAuth.login_endpoint, body, headers=JsonFixture.get_header_without_token())
        response_json = result.json()
        assert result.status_code == 401 and not response_json['success'] and response_json[
            'message'] == 'Not find users with this login!', \
            f'Log in is wrong. Message from server {response_json["message"]}'

    @pytest.mark.smoke
    @pytest.mark.parametrize('login, password, res', ClientAuth.login_password_list)
    def test_sign_in_with_different_login_and_password(self, login, password, res):
        body = JsonFixture.for_login_customers(login='')
        result = HttpManager.post(ClientAuth.login_endpoint, body, headers=JsonFixture.get_header_without_token())
        response_json = result.json()
        assert result.status_code == 401, f'Wrong status code, expected status code: 401 actual status code: {result.status_code}'
        assert response_json['success'] == res
