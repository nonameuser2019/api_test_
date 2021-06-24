from tests.utils.json_fixture import JsonFixture
from tests.utils.variables import ClientRegistration, ClientAuth
from tests.utils.http_manager import HttpManager
import requests
import pytest


class TestLogOutClient:
    def test_logout_with_token(self, auth):
        token = auth.json()['data']['token']
        headers = JsonFixture.get_headers(token)
        response = requests.post(ClientAuth.login_endpoint, headers=headers)
        assert response.status_code == 200, f'Logout is not success'