from tests.utils.json_fixture import JsonFixture
from tests.utils.variables import Cart
from tests.utils.http_manager import HttpManager
import pytest


class TestCartAddItem:

    @pytest.mark.parametrize('product_id, attr_id, count, client_id, res, status_code', Cart.product_id_list)
    @pytest.mark.smoke
    def test_check_add_item_without_id_param(self, db_connect, product_id, attr_id, count, client_id, res, status_code):
        body = JsonFixture.product_data(product_id, attr_id, count, client_id)
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        assert result.status_code == status_code, f'Wrong status code from server. Status code from server: {result.status_code}'
        assert result.json()['success'] == res, f'Expected status code 400. Success message from server: {result.json()["success"]}'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={result.json()['data']['id']}")

    @pytest.mark.smoke
    def test_check_response_attr_with_response_with_valid_params(self, db_connect):
        product_id = 5010187
        attr_id = ""
        count = 2
        client_id = ""
        body = JsonFixture.product_data(product_id, attr_id, count, client_id)
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        assert result.status_code == 200, f'Wrong status code from server. Status code from server: {result.status_code}'
        assert result.json()["data"][product_id]["count"] == count
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={result.json()['data']['id']}")

    @pytest.mark.smoke
    def test_check_cart_id_hash_in_response(self, db_connect):
        product_id = 5010187
        attr_id = ""
        count = 2
        client_id = ""
        body = JsonFixture.product_data(product_id, attr_id, count, client_id)
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        assert result.status_code == 200, f'Wrong status code from server. Status code from server: {result.status_code}'
        assert result.json()["data"]["cart_id_hash"], f'card_id_hash not found in response from server'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={result.json()['data']['id']}")

    @pytest.mark.smoke
    def test_check_cart_model_id_in_response(self, db_connect):
        product_id = 5010187
        attr_id = ""
        count = 2
        client_id = ""
        body = JsonFixture.product_data(product_id, attr_id, count, client_id)
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        assert result.status_code == 200, f'Wrong status code from server. Status code from server: {result.status_code}'
        assert result.json()["data"]["id"], 'Cart model id not found in server response'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={result.json()['data']['id']}")

    @pytest.mark.smoke
    def test_check_add_item_without_attribute_id(self, db_connect):
        body= JsonFixture.product_data(5010187, None, 2, "")
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        assert result.status_code == 400, f'Error impossible send request without attribute_id. Status code: {result.status_code}'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={result.json()['data']['id']}")

    @pytest.mark.parametrize('count, res, status_code', Cart.product_count_list)
    @pytest.mark.smoke
    def test_send_requests_with_different_count(self, db_connect, count, res, status_code):
        body = JsonFixture.product_data(5010187, "", count, "")
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        assert result.status_code == status_code, f'Wrong status code expected status code: {status_code} ' \
                                                  f'And response status code from server: {result.status_code}'
        assert result.json()['success'] == res, f'Wrong result Expected result: {res} Actual result: {result.json()["success"]}'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={result.json()['data']['id']}")

    @pytest.mark.smoke
    def test_send_request_with_over_count(self, db_connect, get_product_balance):
        body = JsonFixture.product_data(5010187, "", get_product_balance + 1, "")
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        assert result.status_code == 400, 'Error server allows add count more then stock quantity'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={result.json()['data']['id']}")

    @pytest.mark.smoke
    def test_send_request_with_max_count(self, db_connect, get_product_balance):
        body = JsonFixture.product_data(5010187, "", get_product_balance, "")
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        assert result.status_code == 200, 'Error server does not allow send request with max quantity'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={result.json()['data']['id']}")

    @pytest.mark.smoke
    def test_send_request_with_wrong_clientid(self, db_connect):
        body = JsonFixture.product_data(5010187, "", 1, 000000)
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        assert result.status_code == 400, f'Error server allows send request with wrong client ID param'
        assert result.json()['success'], f'Error expected result success == false but response from servrer: ' \
                                         f'{result.json()["success"]}'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={result.json()['data']['id']}")

    @pytest.mark.smoke
    def test_send_request_with_wrong_type_client_id(self, db_connect):
        body = JsonFixture.product_data(5010187, "", 1, 'FFFFFFF')
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        assert result.status_code == 400, f'Error server allows send request with wrong data type client ID param'
        assert result.json()['success'], f'Error expected result success == false but response from servrer: ' \
                                         f'{result.json()["success"]}'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={result.json()['data']['id']}")