from tests.utils.http_manager import HttpManager
from tests.utils.json_fixture import JsonFixture
from tests.utils.error_messages import ErrorMessages
import pytest
from tests.utils.variables import OrdersByClick
import pytest_check as check


class TestOrderByOneClick:

    @pytest.mark.smoke
    def test_send_request_with_all_valid_param(self, db_connect):
        body = JsonFixture.order_by_click()
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        db_connect.execute(f'SELECT id FROM `order` WHERE id=(%s)', result.json()['data']['order_id'])
        data = db_connect.fetchall()
        check.equal(result.status_code, 200), ErrorMessages.status_code_error(200, result.status_code)
        check.equal(result.json()['success'], True), ErrorMessages.success_message_error(True, result.json()['success'])
        check.equal(len(data), 1), ErrorMessages.count_order_error(1, len(data))

    @pytest.mark.smoke
    def test_send_request_with_product_with_attr_id(self, db_connect):
        body = JsonFixture.order_by_click(product_id="109189", attribute_id="1")
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        db_connect.execute(f'SELECT id FROM `order` WHERE id=(%s)', result.json()['data']['order_id'])
        data = db_connect.fetchall()
        check.equal(result.status_code, 200), f'Wrong status code. Expected result is 200. Actual ' \
                                              f'result is {result.status_code}'
        check.equal(result.json()['success'], True), f'Wrong success result. Expected result is True. Actual ' \
                                                     'result: {result.json()["success"]}'
        check.equal(len(data), 1), f'Wrong product count in DB, expected result is 1 but actual result {len(data)}'

    @pytest.mark.test
    @pytest.mark.smoke
    def test_send_req_with_unavailable_product(self):
        body = JsonFixture.order_by_click(product_id="249953")
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        check.equal(result.status_code, 400), f'Wrong status code. Expected result is 200. Actual ' \
                                              f'result is {result.status_code}'
        check.equal(result.json()['success'], False), f'Wrong success result. Expected result is True. Actual ' \
                                                     'result: {result.json()["success"]}'