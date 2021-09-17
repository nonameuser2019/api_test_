import random

from tests.utils.json_fixture import JsonFixture
from tests.utils.variables import OrdersHistory
from tests.utils.error_messages import ErrorMessages
from tests.utils.http_manager import HttpManager
from tests.utils.sql_query import Sql
import pytest
import pytest_check as check


class TestOrderHistory:

    @pytest.mark.smoke
    def test_send_request_with_correct_token(self, auth):
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        result = HttpManager.get(OrdersHistory.get_orders_endpoint, headers=headers)
        check.equal(result.status_code, 200, ErrorMessages.status_code_error(200, result.status_code))
        check.greater(result.json()['meta']['total'], 0, f'Wrong orders count')

    @pytest.mark.smoke
    def test_send_request_with_wrong_token(self, auth):
        headers = JsonFixture.get_headers(auth.json()['data']['access_token']+'ksfdjghsdgfudhg')
        result = HttpManager.get(OrdersHistory.get_orders_endpoint, headers=headers)
        check.equal(result.status_code, 401, ErrorMessages.status_code_error(401, result.status_code))

    @pytest.mark.smoke
    @pytest.mark.test
    def test_check_search_with_order_id(self, auth, db_connect):
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        db_connect.execute(Sql.get_order_ids())
        id_list = db_connect.fetchall()
        payload = {'search': id_list[random.randint(0, len(id_list))]['id']}
        result = HttpManager.get(OrdersHistory.get_orders_endpoint, headers=headers, payload=payload)
        check.equal(result.status_code, 200, ErrorMessages.status_code_error(200, result.status_code))
        check.equal(result.json()['meta']['total'], 1, f'Wrong orders count with id: {payload["search"]}')