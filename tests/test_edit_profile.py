from tests.utils.json_fixture import JsonFixture
from tests.utils.variables import ClientProfileEdit
from tests.utils.http_manager import HttpManager
import requests
import pytest
import pymysql


class TestEditProfile:
    @pytest.mark.smoke
    def test_check_possibility_change_email(self, auth, db_connect):
        body = JsonFixture.profile_data('test_mail@gmail.com')
        headers = JsonFixture.get_headers(auth.json()['data']['token'])
        result = HttpManager.post(ClientProfileEdit.edit_profile_endpoint, body, headers)
        assert result.status_code == 200, f'Error data does not changed'
        assert result.json()['message'] == 'Data updated successfully', f'Data does not updated'
        db_connect.execute(f'UPDATE customers SET email="defolt_test@gmail.com" WHERE id = 19392')

    @pytest.mark.smoke
    def test_check_possibility_change_phone(self, auth, db_connect):
        body = JsonFixture.profile_data(phone='0685340603')
        headers = JsonFixture.get_headers(auth.json()['data']['token'])
        result = HttpManager.post(ClientProfileEdit.edit_profile_endpoint, body, headers)
        assert result.status_code == 200, f'Error data does not changed'
        assert result.json()['message'] == 'Data updated successfully', f'Data does not updated'
        db_connect.execute(f'UPDATE customers SET phone="0777777777" WHERE id = 19392')

    @pytest.mark.smoke
    def test_check_posibility_change_name(self, auth, db_connect):
        body = JsonFixture.profile_data(name='Ivan Ivanov')
        headers = JsonFixture.get_headers(auth.json()['data']['token'])
        result = HttpManager.post(ClientProfileEdit.edit_profile_endpoint, body, headers)
        assert result.status_code == 200, f'Error data does not changed'
        assert result.json()['message'] == 'Data updated successfully', f'Data does not updated'
        db_connect.execute(f'UPDATE customers SET name="Main-Test" WHERE id = 19392')

    @pytest.mark.smoke
    def test_check_possibility_change_password(self, auth, db_connect):
        body = JsonFixture.profile_data(password='Q1dflmnbv')
        headers = JsonFixture.get_headers(auth.json()['data']['token'])
        result = HttpManager.post(ClientProfileEdit.edit_profile_endpoint, body, headers)
        assert result.status_code == 200, f'Error data does not changed'
        assert result.json()['message'] == 'Data updated successfully', f'Data does not updated'
        db_connect.execute(f'UPDATE customers SET password="Qwerty123" WHERE id = 19392')

    @pytest.mark.smoke
    def test_check_possibility_change_all_data(self, auth, db_connect):
        body = JsonFixture.profile_data(email='test_mail@gmail.com', phone='0685340603', name='Ivan Ivanov', password='Q1dflmnbv')
        headers = JsonFixture.get_headers(auth.json()['data']['token'])
        result = HttpManager.post(ClientProfileEdit.edit_profile_endpoint, body, headers)
        assert result.status_code == 200, f'Error data does not changed'
        assert result.json()['message'] == 'Data updated successfully', f'Data does not updated'
        db_connect.execute(f'UPDATE customers SET password="Qwerty123", name="Main-Test"", phone="0777777777",'
                           f'email="defolt_test@gmail.com" WHERE id = 19392')
