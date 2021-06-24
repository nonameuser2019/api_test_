from tests.utils.json_fixture import JsonFixture
from tests.utils.variables import ClientRegistration, ClientAuth
from tests.utils.http_manager import HttpManager
import requests
import pytest

class TestLogOutClient:
    def test_logout_with_token(self, auth):
        pass