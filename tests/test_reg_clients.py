from tests.utils.json_fixture import JsonFixture
from tests.utils.variables import ClientRegistration
from tests.utils.http_manager import HttpManager
from tests.utils.error_messages import ErrorMessages
import pytest
import pytest_check as check


class TestRegistrationNewUser:

    @pytest.mark.test
    @pytest.mark.smoke
    def test_reg_with_valid_param(self, db_connect):
        body = JsonFixture.for_register_new_user()
        result = HttpManager.post(ClientRegistration.reg_endpoint, body, headers=JsonFixture.get_header_without_token())
        db_connect.execute('DELETE FROM customers WHERE phone=%s', '%body["login"]')
        check.equal(result.status_code, 200), ErrorMessages.status_code_error(200, result.status_code)
        check.equal(result.json()['success'], True), ErrorMessages.succ_mess_error(True, result.json()['success'])

    @pytest.mark.smoke
    @pytest.mark.parametrize('name, res, status_code', ClientRegistration.name_list)
    def test_reg_with_different_names(self, db_connect, name, res, status_code):
        body = JsonFixture.for_register_new_user(name)
        result = HttpManager.post(ClientRegistration.reg_endpoint, body, headers=JsonFixture.get_header_without_token())
        db_connect.execute('DELETE FROM customers WHERE phone=%s', '%body["login"]')
        check.equal(result.status_code, status_code), ErrorMessages.status_code_error(status_code, result.status_code)
        check.equal(result.json()['success'], res), ErrorMessages.succ_mess_error(res, result.json()['success'])


    @pytest.mark.smoke
    def test_check_reg_with_empty_all_param(self):
        body = JsonFixture.for_register_new_user("", "", "", "")
        result = HttpManager.post(ClientRegistration.reg_endpoint, body, headers=JsonFixture.get_header_without_token())
        check.equal(result.status_code, 422), ErrorMessages.status_code_error(422, result.status_code)
        check.equal(result.json()['success'], False), ErrorMessages.succ_mess_error(False, result.json()['success'])

    @pytest.mark.smoke
    def test_reg_with_empty_login(self, db_connect):
        body = JsonFixture.for_register_new_user('Alex', login="")
        result = HttpManager.post(ClientRegistration.reg_endpoint, body, headers=JsonFixture.get_header_without_token())
        db_connect.execute('DELETE FROM customers WHERE phone=%s', '%body["login"]')
        check.equal(result.status_code, 422), ErrorMessages.status_code_error(422, result.status_code)
        check.equal(result.json()['success'], False), ErrorMessages.succ_mess_error(False, result.json()['success'])

    @pytest.mark.smoke
    def test_reg_with_empty_password(self, db_connect):
        body = JsonFixture.for_register_new_user(password="")
        result = HttpManager.post(ClientRegistration.reg_endpoint, body, headers=JsonFixture.get_header_without_token())
        db_connect.execute('DELETE FROM customers WHERE phone=%s', '%body["login"]')
        check.equal(result.status_code, 422), ErrorMessages.status_code_error(422, result.status_code)
        check.equal(result.json()['success'], False), ErrorMessages.succ_mess_error(False, result.json()['success'])

    @pytest.mark.smoke
    def test_reg_with_empty_body(self):
        body = {}
        result = HttpManager.post(ClientRegistration.reg_endpoint, body, headers=JsonFixture.get_header_without_token())
        check.equal(result.status_code, 422), ErrorMessages.status_code_error(422, result.status_code)
        check.equal(result.json()['success'], False), ErrorMessages.succ_mess_error(False, result.json()['success'])

    @pytest.mark.smoke
    @pytest.mark.parametrize('phone, res, status_code', ClientRegistration.phone_list)
    def test_reg_with_different_phones(self, db_connect, phone, res, status_code):
        body = JsonFixture.for_register_new_user(login=phone)
        result = HttpManager.post(ClientRegistration.reg_endpoint, body, headers=JsonFixture.get_header_without_token())
        db_connect.execute('DELETE FROM customers WHERE phone=%s', '%body["login"]')
        check.equal(result.status_code, status_code), ErrorMessages.status_code_error(status_code, result.status_code)
        check.equal(result.json()['success'], res), ErrorMessages.succ_mess_error(res, result.json()['success'])

    @pytest.mark.smoke
    @pytest.mark.parametrize('email, res, status_code', ClientRegistration.email_list)
    def test_reg_with_different_emails(self, db_connect, email, res, status_code):
        body = JsonFixture.for_register_new_user(email=email)
        result = HttpManager.post(ClientRegistration.reg_endpoint, body, headers=JsonFixture.get_header_without_token())
        db_connect.execute('DELETE FROM customers WHERE phone=%s', '%body["login"]')
        check.equal(result.status_code, status_code), ErrorMessages.status_code_error(status_code, result.status_code)
        check.equal(result.json()['success'], res), ErrorMessages.succ_mess_error(res, result.json()['success'])

    @pytest.mark.smoke
    @pytest.mark.parametrize('password, res, status_code', ClientRegistration.password_list)
    def test_reg_with_different_passwords(self, db_connect, password, res, status_code):
        body = JsonFixture.for_register_new_user(password=password)
        result = HttpManager.post(ClientRegistration.reg_endpoint, body, headers=JsonFixture.get_header_without_token())
        db_connect.execute('DELETE FROM customers WHERE phone=%s', '%body["login"]')
        check.equal(result.status_code, status_code), ErrorMessages.status_code_error(status_code, result.status_code)
        check.equal(result.json()['success'], res), ErrorMessages.succ_mess_error(res, result.json()['success'])
