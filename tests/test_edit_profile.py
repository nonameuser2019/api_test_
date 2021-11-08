from tests.utils.json_fixture import JsonFixture
from tests.utils.variables import ClientProfileEdit
from tests.utils.http_manager import HttpManager
import requests
import pytest
import pymysql
import pytest_check as check


class TestEditProfile:
    # @pytest.mark.smoke
    # def test_check_possibility_change_email(self, create_account, auth, db_connect):
    #     body = JsonFixture.profile_data('test_mail@gmail.com')
    #     headers = JsonFixture.get_headers(auth.json()['data']['token'])
    #     result = HttpManager.post(ClientProfileEdit.edit_profile_endpoint, body, headers)
    #     assert result.status_code == 200, f'Error data does not changed'
    #     assert result.json()['message'] == 'Data updated successfully', f'Data does not updated'
    #     db_connect.execute(f'DELETE FROM customers WHERE phone = "0777777777"')
    #
    # @pytest.mark.smoke
    # def test_check_possibility_change_phone(self, create_account, auth, db_connect):
    #     body = JsonFixture.profile_data(phone='0685340603')
    #     headers = JsonFixture.get_headers(auth.json()['data']['token'])
    #     result = HttpManager.post(ClientProfileEdit.edit_profile_endpoint, body, headers)
    #     assert result.status_code == 200, f'Error data does not changed'
    #     assert result.json()['message'] == 'Data updated successfully', f'Data does not updated'
    #     db_connect.execute(f'DELETE FROM customers WHERE phone = "0685340603"')
    #
    # @pytest.mark.smoke
    # def test_check_possibility_change_name(self, create_account, auth, db_connect):
    #     body = JsonFixture.profile_data(name='Ivan Ivanov')
    #     headers = JsonFixture.get_headers(auth.json()['data']['token'])
    #     result = HttpManager.post(ClientProfileEdit.edit_profile_endpoint, body, headers)
    #     assert result.status_code == 200, f'Error data does not changed'
    #     assert result.json()['message'] == 'Data updated successfully', f'Data does not updated'
    #     db_connect.execute(f'DELETE FROM customers WHERE phone = "0777777777"')
    #
    # @pytest.mark.smoke
    # def test_check_possibility_change_password(self, create_account, auth, db_connect):
    #     body = JsonFixture.profile_data(password='Q1dflmnbv')
    #     headers = JsonFixture.get_headers(auth.json()['data']['token'])
    #     result = HttpManager.post(ClientProfileEdit.edit_profile_endpoint, body, headers)
    #     assert result.status_code == 200, f'Error data does not changed'
    #     assert result.json()['message'] == 'Data updated successfully', f'Data does not updated'
    #     db_connect.execute(f'DELETE FROM customers WHERE phone = "0777777777"')
    #
    # @pytest.mark.smoke
    # def test_check_possibility_change_all_data(self, create_account, auth, db_connect):
    #     body = JsonFixture.profile_data(email='test_mail@gmail.com', phone='0685340603', name='Ivan Ivanov', password='Q1dflmnbv')
    #     headers = JsonFixture.get_headers(auth.json()['data']['token'])
    #     result = HttpManager.post(ClientProfileEdit.edit_profile_endpoint, body, headers)
    #     db_connect.execute(f'SELECT name, email, phone FROM customers WHERE phone="0685340603"')
    #     data = db_connect.fetchall()
    #     assert data[0]['name'] == 'Ivan Ivanov' and data[0]['phone'] == '0685340603' and data[0]['email'] == 'test_mail@gmail.com',\
    #         f'Wrong data in DB'
    #     assert result.status_code == 200, f'Error data does not changed'
    #     assert result.json()['message'] == 'Data updated successfully', f'Data does not updated'
    #     db_connect.execute(f'DELETE FROM customers WHERE phone = "0685340603"')
    pass
