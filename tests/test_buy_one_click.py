from tests.utils.http_manager import HttpManager
from tests.utils.json_fixture import JsonFixture
from tests.utils.error_messages import ErrorMessages
from tests.utils.allure_step import AllureStep
import pytest
from tests.utils.variables import OrdersByClick, ClientRegistration
from simplejson.errors import JSONDecodeError
from tests.utils.sql_query import Sql
import allure
from pytest_check import check
class TestOrderByOneClick:

    PRODUCT_WITH_PARAMS = '131333'

    @pytest.mark.smoke
    @allure.title('Positive test with valid data')
    def test_send_request_with_all_valid_param(self, db_connect):
        body = JsonFixture.order_by_click()
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        db_connect.execute(Sql.get_order_by_order_id(result.json()['data']['order_id']))
        data = db_connect.fetchall()
        with allure.step(AllureStep.check_status_code('200')):
            assert result.status_code == 200, ErrorMessages.status_code_error(200, result.status_code)
        with allure.step('Check success param in response, expected result is True'):
            assert result.json()['success'], ErrorMessages.get_response_error(result.json())
        with allure.step('Check order in DB by order_id'):
            assert len(data) == 1, ErrorMessages.count_order_error(1, len(data))

    @pytest.mark.smoke
    @allure.title('Positive test with product with attribute id ')
    def test_send_request_with_product_with_attr_id(self, db_connect):
        body = JsonFixture.order_by_click(product_id="109189", attribute_id="1")
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        db_connect.execute(Sql.get_order_by_order_id(result.json()['data']['order_id']))
        data = db_connect.fetchall()
        with allure.step(AllureStep.check_status_code('200')):
            assert result.status_code == 200, ErrorMessages.status_code_error(200, result.status_code)
        with allure.step('Check success param in response, expected result is True'):
            assert result.json()['success'], ErrorMessages.get_response_error(result.json())
        with allure.step('Check order in DB by order_id'):
            assert len(data) == 1, ErrorMessages.count_order_error(1, len(data))

    @pytest.mark.smoke
    def test_send_req_with_unavailable_product(self):
        body = JsonFixture.order_by_click(product_id="249953")
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_status_code('200')):
            assert result.status_code == 200, ErrorMessages.status_code_error(200, result.status_code)
        with allure.step('Check success param in response, expected result is True'):
            assert result.json()['success'], ErrorMessages.get_response_error(result.json())

    @pytest.mark.smoke
    @allure.title('Negative test. Impossible to send request with empty body')
    def test_send_request_with_empty_body(self):
        body = {}
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_status_code('422')):
            assert result.status_code == 422, ErrorMessages.status_code_error(422, result.status_code)

    @pytest.mark.smoke
    @allure.title('Negative test. Use invalid phone like +038')
    def test_send_request_with_wrong_phone(self):
        body = JsonFixture.order_by_click(phone='+38')
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_status_code('422')):
            assert result.status_code == 422, ErrorMessages.status_code_error(422, result.status_code)

    @pytest.mark.smoke
    @pytest.mark.parametrize('phone, res, status_code', ClientRegistration.phone_list)
    @allure.title('Validate field of phone')
    def test_send_request_with_wrong_phone(self, phone, res, status_code):
        body = JsonFixture.order_by_click(phone=phone)
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_status_code(status_code)):
            assert result.status_code == status_code, ErrorMessages.status_code_error(status_code, result.status_code)
        with allure.step(AllureStep.check_success_message(res)):
            assert result.json()['success'] == res, ErrorMessages.succ_mess_error(res, result.json()['success'])

    @pytest.mark.smoke
    @allure.title('Negative test with body that does not have param of phone')
    def test_send_request_without_phone(self):
        body = JsonFixture.order_by_click()
        body.pop('phone')
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_status_code('422')):
            assert result.status_code == 422, ErrorMessages.status_code_error(422, result.status_code)
        with allure.step(AllureStep.check_success_message(False)):
            assert result.json()['success'] == False, ErrorMessages.succ_mess_error(False, result.json()['success'])

    @pytest.mark.smoke
    @pytest.mark.parametrize('product_id, status_code, res', OrdersByClick.product_id_list)
    @allure.title('Tests with different product id')
    def test_send_request_with_different_prod_id(self, product_id, status_code, res):
        body = JsonFixture.order_by_click(product_id=product_id)
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_status_code(status_code)):
            assert result.status_code == status_code, ErrorMessages.status_code_error(status_code, result.status_code)
        with allure.step(AllureStep.check_success_message(res)):
            assert result.json()['success'] == res, ErrorMessages.succ_mess_error(res, result.json()['success'])

    @pytest.mark.smoke
    @allure.title('Negative test with body that has not product_id param')
    def test_send_request_without_product_id(self):
        body = JsonFixture.order_by_click()
        body.pop('product_id')
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_status_code(422)):
            assert result.status_code == 422, ErrorMessages.status_code_error(422, result.status_code)


    @pytest.mark.smoke
    @pytest.mark.parametrize('attribute_id, status_code, res', OrdersByClick.product_id_list)
    def test_send_request_without_attr_id_for_product_with_attr(self, attribute_id, status_code, res):
        body = JsonFixture.order_by_click(product_id=TestOrderByOneClick.PRODUCT_WITH_PARAMS)
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_status_code(status_code)):
            assert result.status_code == status_code, ErrorMessages.status_code_error(status_code, result.status_code)

    @pytest.mark.smoke
    @allure.title('Positive test with max product count')
    def test_send_request_with_max_count(self, get_product_balance):
        body = JsonFixture.order_by_click()
        body['count'] = get_product_balance
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_status_code(200)):
            assert result.status_code == 200, ErrorMessages.status_code_error(200, result.status_code)

    @pytest.mark.smoke
    @allure.title('Negative test. Body does not have count param')
    def test_send_request_without_count_param(self):
        body = JsonFixture.order_by_click()
        body.pop('count')
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_status_code(200)):
            assert result.status_code == 422, ErrorMessages.status_code_error(422, result.status_code)

    @pytest.mark.smoke
    @allure.title('Negative test. Body has wrong customer id')
    def test_send_request_with_wrong_client_id(self):
        body = JsonFixture.order_by_click()
        body['customer_id'] = '000999888'
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_status_code(200)):
            assert result.status_code == 422, ErrorMessages.status_code_error(422, result.status_code)

    @pytest.mark.smoke
    def test_send_request_without_client_id(self):
        body = JsonFixture.order_by_click()
        body.pop('customer_id')
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        check.equal(result.status_code, 422, ErrorMessages.status_code_error(422, result.status_code))
        check.equal(result.json()['success'], False, ErrorMessages.get_response_error(result.json()))

    @pytest.mark.smoke
    def test_send_request_with_wrong_currency_id(self):
        body = JsonFixture.order_by_click(currency_id=840)
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        check.equal(result.status_code, 422, ErrorMessages.status_code_error(422, result.status_code))
        check.equal(result.json()['success'], False, ErrorMessages.get_response_error(result.json()))

    @pytest.mark.smoke
    def test_send_request_without_currency_id(self):
        body = JsonFixture.order_by_click()
        body.pop('currency_id')
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        check.equal(result.status_code, 422, ErrorMessages.status_code_error(422, result.status_code))
        check.equal(result.json()['success'], False, ErrorMessages.get_response_error(result.json()))

    @pytest.mark.smoke
    def test_send_request_without_currency_id_string_type(self):
        body = JsonFixture.order_by_click('980')
        result = HttpManager.post(OrdersByClick.oreder_by_click_endpoint, body, JsonFixture.get_header_without_token())
        check.equal(result.status_code, 422, ErrorMessages.status_code_error(422, result.status_code))
        check.equal(result.json()['success'], False, ErrorMessages.get_response_error(result.json()))
