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
    def test_check_search_with_order_id(self, auth, db_connect):
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        db_connect.execute(Sql.get_order_ids())
        id_list = db_connect.fetchall()
        payload = {'search': id_list[random.randint(0, len(id_list))]['id']}
        result = HttpManager.get(OrdersHistory.get_orders_endpoint, headers=headers, payload=payload)
        check.equal(result.status_code, 200, ErrorMessages.status_code_error(200, result.status_code))
        check.equal(result.json()['meta']['total'], 1, f'Wrong orders count with id: {payload["search"]}')

    @pytest.mark.smoke
    def test_check_search_with_wrong_search_pattern(self, auth, db_connect):
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        payload = {'search': '12525fvsv342434'}
        result = HttpManager.get(OrdersHistory.get_orders_endpoint, headers=headers, payload=payload)
        check.equal(result.status_code, 200, ErrorMessages.status_code_error(200, result.status_code))
        check.equal(result.json()['meta']['total'], 0, f'Wrong orders count with id: {payload["search"]}')

    @pytest.mark.smoke
    def test_send_request_with_start_date_without_finish_date(self, auth):
        start_date = '2021-08-01'
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        payload = {'start_date': start_date}
        result = HttpManager.get(OrdersHistory.get_orders_endpoint, headers=headers, payload=payload)
        check.equal(result.status_code, 200, ErrorMessages.status_code_error(200, result.status_code))
        for order in result.json()['data']:
            assert order['date'].split()[0] >= start_date, f'Wrong filter of date'

    @pytest.mark.smoke
    def test_send_request_with_the_same_start_and_finish_date(self, auth):
        start_date = '2021-09-14'
        finish_date = '2021-09-14'
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        payload = {'start_date': start_date, 'finish_date': finish_date}
        result = HttpManager.get(OrdersHistory.get_orders_endpoint, headers=headers, payload=payload)
        check.equal(result.status_code, 200, ErrorMessages.status_code_error(200, result.status_code))
        for order in result.json()['data']:
            assert order['date'].split()[0] > start_date, f'Wrong filter of date'

    @pytest.mark.smoke
    def test_send_request_with_finish_date_smaller_start_date(self, auth):
        start_date = '2021-09-14'
        finish_date = '2021-09-13'
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        payload = {'start_date': start_date, 'finish_date': finish_date}
        result = HttpManager.get(OrdersHistory.get_orders_endpoint, headers=headers, payload=payload)
        check.equal(result.status_code, 200, ErrorMessages.status_code_error(200, result.status_code))
        check.equal(result.json()['meta']['total'], 0, f'Wrong orders count')

    @pytest.mark.smoke
    def test_test_request_with_only_finish_date(self, auth):
        finish_date = '2021-09-13'
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        payload = {'finish_date': finish_date}
        result = HttpManager.get(OrdersHistory.get_orders_endpoint, headers=headers, payload=payload)
        check.equal(result.status_code, 200, ErrorMessages.status_code_error(200, result.status_code))
        for order in result.json()['data']:
            assert order['date'].split()[0] <= finish_date, f'Wrong filter of date'

    @pytest.mark.smoke
    def test_send_request_with_wrong_date(self, auth):
        start_date = '2021-09-141'
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        payload = {'finish_date': start_date}
        result = HttpManager.get(OrdersHistory.get_orders_endpoint, headers=headers, payload=payload)
        check.equal(result.status_code, 422, ErrorMessages.status_code_error(422, result.status_code))

    @pytest.mark.smoke
    @pytest.mark.parametrize('value, status_code, response_value', OrdersHistory.per_page_list)
    def test_send_with_negative_value_of_per_page(self, auth, value, status_code, response_value):
        payload = {'per_page': value}
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        result = HttpManager.get(OrdersHistory.get_orders_endpoint, headers=headers, payload=payload)
        check.equal(result.status_code, status_code, ErrorMessages.status_code_error(status_code, result.status_code))
        check.equal(result.json()['meta']['per_page'], response_value, f'Wrong per_page value in response')

    @pytest.mark.smoke
    def test_send_with_string_cant_be_number_of_per_page(self, auth):
        payload = {'per_page': 'eleven'}
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        result = HttpManager.get(OrdersHistory.get_orders_endpoint, headers=headers, payload=payload)
        check.equal(result.status_code, 422, ErrorMessages.status_code_error(422, result.status_code))

    @pytest.mark.smoke
    def test_request_with_0_in_page_param(self, auth):
        payload = {'page': 0}
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        result = HttpManager.get(OrdersHistory.get_orders_endpoint, headers=headers, payload=payload)
        check.equal(result.status_code, 200, ErrorMessages.status_code_error(200, result.status_code))
        check.equal(result.json()['meta']['current_page'], 1, f'Wrong page value in response')

    @pytest.mark.smoke
    def test_request_with_page_in_range_between1_and_max_page(self, auth, get_max_page):
        page = random.randint(1, get_max_page + 1)
        payload = {'page': page}
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        result = HttpManager.get(OrdersHistory.get_orders_endpoint, headers=headers, payload=payload)
        check.equal(result.status_code, 200, ErrorMessages.status_code_error(200, result.status_code))
        check.equal(result.json()['meta']['current_page'], page, f'Wrong page value in response')

    @pytest.mark.smoke
    def test_request_with_page_param_max_plus_one(self, auth, get_max_page):
        payload = {'page': get_max_page + 1}
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        result = HttpManager.get(OrdersHistory.get_orders_endpoint, headers=headers, payload=payload)
        check.equal(result.status_code, 200, ErrorMessages.status_code_error(200, result.status_code))
        check.is_false(result.json()['data'], f'Wrong orders count')

    @pytest.mark.test
    @pytest.mark.smoke
    def test_request_with_page_string_param_that_cant_be_number(self, auth, get_max_page):
        payload = {'page': 'qwerty'}
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        result = HttpManager.get(OrdersHistory.get_orders_endpoint, headers=headers, payload=payload)
        check.equal(result.status_code, 422, ErrorMessages.status_code_error(200, result.status_code))