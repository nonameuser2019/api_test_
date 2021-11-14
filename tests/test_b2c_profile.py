import random
from tests.utils.json_fixture import JsonFixture
from tests.utils.variables import B2cProfile
from tests.utils.error_messages import ErrorMessages
from tests.utils.http_manager import HttpManager
from tests.utils.sql_query import Sql
import pytest
import allure
class TestGetB2cProfile:

    @pytest.mark.smoke
    def test_check_status_code_with_correct_token(self, auth):
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        result = HttpManager.get(B2cProfile.get_b2c_prof_endpoint, headers=headers)
        assert result.status_code == 200, ErrorMessages.status_code_error(200, result.status_code)

    @pytest.mark.smoke
    @pytest.mark.parametrize('param, status_code', B2cProfile.possitive_assers)
    def test_check_all_response_data(self, auth, db_connect, param, status_code):
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        result = HttpManager.get(B2cProfile.get_b2c_prof_endpoint, headers=headers)
        db_connect.execute(Sql.get_usr_data(result.json()['data']['id']))
        user_data = db_connect.fetchall()
        data = result.json()['data']
        assert data[param] == user_data[0][param], ErrorMessages.check_param_error(data[param], user_data[0][param])

    @pytest.mark.smoke
    def test_send_request_with_wrong_token(self, auth):
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'] + 'asdwsdadwdas')
        result = HttpManager.get(B2cProfile.get_b2c_prof_endpoint, headers=headers)
        assert result.status_code == 401, ErrorMessages.status_code_error(401, result.status_code)

    @pytest.mark.smoke
    def test_send_request_without_token(self):
        headers = JsonFixture.get_header_without_token()
        result = HttpManager.get(B2cProfile.get_b2c_prof_endpoint, headers=headers)
        assert result.status_code == 401, ErrorMessages.status_code_error(401, result.status_code)


class TestChangeB2cInfo:

    @pytest.mark.smoke
    @pytest.mark.parametrize('param, status_code', B2cProfile.change_info_aserts)
    def test_change_info_with_valid_all_data(self, auth, param, status_code):
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        body = JsonFixture.b2c_info()
        result = HttpManager.update(B2cProfile.change_info_endpoint, body, headers=headers)
        data = result.json()['data']
        assert data[param] == body[param], ErrorMessages.check_param_error(data[param], body[param])

    @pytest.mark.smoke
    def test_send_request_without_middle_name(self, auth):
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        body = JsonFixture.b2c_info()
        body.pop('middle_name')
        result = HttpManager.update(B2cProfile.change_info_endpoint, body, headers=headers)
        assert result.status_code == 422, ErrorMessages.status_code_error(422, result.status_code)

    @pytest.mark.smoke
    def test_send_request_without_first_name(self, auth):
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        body = JsonFixture.b2c_info()
        body.pop('first_name')
        result = HttpManager.update(B2cProfile.change_info_endpoint, body, headers=headers)
        assert result.status_code == 422, ErrorMessages.status_code_error(422, result.status_code)

    @pytest.mark.smoke
    def test_send_request_without_last_name(self, auth):
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        body = JsonFixture.b2c_info()
        body.pop('last_name')
        result = HttpManager.update(B2cProfile.change_info_endpoint, body, headers=headers)
        assert result.status_code == 422, ErrorMessages.status_code_error(422, result.status_code)

    @pytest.mark.smoke
    def test_send_request_without_token(self):
        headers = JsonFixture.get_header_without_token()
        body = JsonFixture.b2c_info()
        result = HttpManager.update(B2cProfile.change_info_endpoint, body, headers=headers)
        assert result.status_code == 401, ErrorMessages.status_code_error(401, result.status_code)

    @pytest.mark.smoke
    def test_send_request_with_wrong_token(self, auth):
        headers = JsonFixture.get_headers(auth.json()['data']['access_token']+'asdwqwd')
        body = JsonFixture.b2c_info()
        result = HttpManager.update(B2cProfile.change_info_endpoint, body, headers=headers)
        assert result.status_code == 401, ErrorMessages.status_code_error(401, result.status_code)

    @pytest.mark.smoke
    @pytest.mark.parametrize('name, status_code', B2cProfile.name_list)
    def test_send_requests_with_different_first_name(self, auth, name, status_code):
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        body = JsonFixture.b2c_info(first_name=name)
        result = HttpManager.update(B2cProfile.change_info_endpoint, body, headers=headers)
        assert status_code == status_code, ErrorMessages.status_code_error(status_code, result.status_code)

    @pytest.mark.smoke
    @pytest.mark.parametrize('name, status_code', B2cProfile.name_list)
    def test_send_requests_with_different_last_name(self, auth, name, status_code):
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        body = JsonFixture.b2c_info(last_name=name)
        result = HttpManager.update(B2cProfile.change_info_endpoint, body, headers=headers)
        assert status_code == status_code, ErrorMessages.status_code_error(status_code, result.status_code)

    @pytest.mark.smoke
    @pytest.mark.parametrize('name, status_code', B2cProfile.name_list)
    def test_send_requests_with_different_middle_name(self, auth, name, status_code):
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        body = JsonFixture.b2c_info(middle_name=name)
        result = HttpManager.update(B2cProfile.change_info_endpoint, body, headers=headers)
        assert status_code == status_code, ErrorMessages.status_code_error(status_code, result.status_code)