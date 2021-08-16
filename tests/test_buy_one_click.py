from tests.utils.http_manager import HttpManager
from tests.utils.json_fixture import JsonFixture
from tests.utils.error_messages import ErrorMessages
import pytest
from tests.utils.variables import OrdersByClick, ClientRegistration
import pytest_check as check
from simplejson.errors import JSONDecodeError


class TestOrderByOneClick:

    PRODUCT_WITH_PARAMS = '131333'

    @pytest.mark.smoke
    def test_send_request_with_all_valid_param(self, db_connect):
        body = JsonFixture.order_by_click()
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        db_connect.execute(f'SELECT id FROM `order` WHERE id=(%s)', result.json()['data']['order_id'])
        data = db_connect.fetchall()
        check.equal(result.status_code, 200), ErrorMessages.status_code_error(200, result.status_code)
        check.equal(result.json()['success'], True), ErrorMessages.succ_mess_error(True, result.json()['success'])
        check.equal(len(data), 1), ErrorMessages.count_order_error(1, len(data))

    @pytest.mark.smoke
    def test_send_request_with_product_with_attr_id(self, db_connect):
        body = JsonFixture.order_by_click(product_id="109189", attribute_id="1")
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        db_connect.execute(f'SELECT id FROM `order` WHERE id=(%s)', result.json()['data']['order_id'])
        data = db_connect.fetchall()
        check.equal(result.status_code, 200), ErrorMessages.status_code_error(200, result.status_code)
        check.equal(result.json()['success'], True), ErrorMessages.succ_mess_error(True, result.json()["success"])
        check.equal(len(data), 1), ErrorMessages.count_order_error(1, len(data))

    @pytest.mark.smoke
    def test_send_req_with_unavailable_product(self):
        body = JsonFixture.order_by_click(product_id="249953")
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        check.equal(result.status_code, 200), ErrorMessages.status_code_error(200, result.status_code)
        check.equal(result.json()['success'], True), ErrorMessages.succ_mess_error(True, result.json()['success'])

    @pytest.mark.smoke
    def test_send_request_with_empty_body(self):
        body = {}
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        check.equal(result.status_code, 400), ErrorMessages.status_code_error(400, result.status_code)
        try:
            check.equal(result.json()['success'], False), ErrorMessages.succ_mess_error(False, result.json()['success'])
        except JSONDecodeError:
            check.is_true(False), f'Response from server is not json format'

    @pytest.mark.smoke
    def test_send_request_with_wrong_phone(self):
        body = JsonFixture.order_by_click(phone='+38')
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        check.equal(result.status_code, 400), ErrorMessages.status_code_error(400, result.status_code)
        check.equal(result.json()['success'], False), ErrorMessages.succ_mess_error(False, result.json()['success'])

    @pytest.mark.smoke
    @pytest.mark.parametrize('phone, res, status_code', ClientRegistration.phone_list)
    def test_send_request_with_wrong_phone(self, phone, res, status_code):
        body = JsonFixture.order_by_click(phone=phone)
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        check.equal(result.status_code, status_code), ErrorMessages.status_code_error(status_code, result.status_code)
        check.equal(result.json()['success'], res), ErrorMessages.succ_mess_error(res, result.json()['success'])

    @pytest.mark.smoke
    def test_send_request_without_phone(self):
        body = JsonFixture.order_by_click()
        body.pop('phone')
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        check.equal(result.status_code, 400), ErrorMessages.status_code_error(400, result.status_code)
        check.equal(result.json()['success'], False), ErrorMessages.succ_mess_error(False, result.json()['success'])

    @pytest.mark.smoke
    @pytest.mark.parametrize('product_id, status_code, res', OrdersByClick.product_id_list)
    def test_send_requst_with_different_prod_id(self, product_id, status_code, res):
        body = JsonFixture.order_by_click(product_id=product_id)
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        check.equal(result.status_code, status_code), ErrorMessages.status_code_error(status_code, result.status_code)
        check.equal(result.json()['success'], res), ErrorMessages.succ_mess_error(res, result.json()['success'])

    @pytest.mark.smoke
    def test_send_request_without_product_id(self):
        body = JsonFixture.order_by_click()
        body.pop('product_id')
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        check.equal(result.status_code, 400), ErrorMessages.status_code_error(400, result.status_code)
        try:
            check.equal(result.json()['success'], False), ErrorMessages.succ_mess_error(False, result.json()['success'])
        except JSONDecodeError:
            check.is_true(False), f'Response from server is not json format'

    @pytest.mark.smoke
    @pytest.mark.parametrize('attribute_id, status_code, res', OrdersByClick.product_id_list)
    def test_send_request_without_attr_id_for_product_with_attr(self, attribute_id, status_code, res):
        body = JsonFixture.order_by_click(product_id=TestOrderByOneClick.PRODUCT_WITH_PARAMS)
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        check.equal(result.status_code, status_code), ErrorMessages.status_code_error(status_code, result.status_code)
        check.equal(result.json()['success'], res), ErrorMessages.succ_mess_error(res, result.json()['success'])

    @pytest.mark.smoke
    def test_send_request_with_max_count_plus_one(self, get_product_balance):
        body = JsonFixture.order_by_click(count=get_product_balance + 1)
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        check.equal(result.status_code, 400), ErrorMessages.status_code_error(400, result.status_code)
        check.equal(result.json()['success'], False), ErrorMessages.succ_mess_error(False, result.json()['success'])

    @pytest.mark.smoke
    def test_send_request_with_zero_count(self):
        body = JsonFixture.order_by_click()
        body['count'] = 0
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        check.equal(result.status_code, 400), ErrorMessages.status_code_error(400, result.status_code)
        check.equal(result.json()['success'], False), ErrorMessages.succ_mess_error(False, result.json()['success'])

    @pytest.mark.smoke
    def test_send_request_with_max_count(self, get_product_balance):
        body = JsonFixture.order_by_click()
        body['count'] = get_product_balance
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        check.equal(result.status_code, 200), ErrorMessages.status_code_error(200, result.status_code)
        check.equal(result.json()['success'], True), ErrorMessages.succ_mess_error(True, result.json()['success'])

    @pytest.mark.smoke
    def test_send_request_without_count_param(self):
        body = JsonFixture.order_by_click()
        body.pop('count')
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        check.equal(result.status_code, 400), ErrorMessages.status_code_error(400, result.status_code)
        try:
            check.equal(result.json()['success'], False), ErrorMessages.succ_mess_error(False, result.json()['success'])
        except JSONDecodeError:
            check.is_true(False), f'Response from server is not json format'

    @pytest.mark.smoke
    def test_send_request_with_wrong_client_id(self):
        body = JsonFixture.order_by_click()
        body['customer_id'] = '000999888'
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        check.equal(result.status_code, 400), ErrorMessages.status_code_error(400, result.status_code)
        check.equal(result.json()['success'], False), ErrorMessages.succ_mess_error(False, result.json()['success'])

    @pytest.mark.smoke
    def test_send_request_without_client_id(self):
        body = JsonFixture.order_by_click()
        body.pop('customer_id')
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        check.equal(result.status_code, 400), ErrorMessages.status_code_error(400, result.status_code)
        check.equal(result.json()['success'], False), ErrorMessages.succ_mess_error(False, result.json()['success'])

    @pytest.mark.smoke
    def test_send_request_with_wrong_currency_id(self):
        body = JsonFixture.order_by_click(currency_id=840)
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        check.equal(result.status_code, 400), ErrorMessages.status_code_error(400, result.status_code)
        check.equal(result.json()['success'], False), ErrorMessages.succ_mess_error(False, result.json()['success'])

    @pytest.mark.smoke
    def test_send_request_without_currency_id(self):
        body = JsonFixture.order_by_click()
        body.pop('currency_id')
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        check.equal(result.status_code, 400), ErrorMessages.status_code_error(400, result.status_code)
        check.equal(result.json()['success'], False), ErrorMessages.succ_mess_error(False, result.json()['success'])


    @pytest.mark.smoke
    def test_send_request_without_currency_id_string_type(self):
        body = JsonFixture.order_by_click('980')
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        check.equal(result.status_code, 400), ErrorMessages.status_code_error(400, result.status_code)
        check.equal(result.json()['success'], False), ErrorMessages.succ_mess_error(False, result.json()['success'])







