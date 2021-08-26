from tests.utils.json_fixture import JsonFixture
from tests.utils.variables import Cart
from tests.utils.http_manager import HttpManager
from tests.utils.sql_query import Sql
from tests.utils.error_messages import ErrorMessages
import pytest
import json
from simplejson.errors import JSONDecodeError
import pytest_check as check


class TestCartAddItem:
    @pytest.mark.parametrize('product_id, attr_id, count, client_id, res, status_code', Cart.product_id_list)
    @pytest.mark.smoke
    def test_check_add_item_with_different_id_param(self, db_connect, product_id, attr_id, count, client_id, res,
                                                    status_code):
        body = JsonFixture.product_data(product_id, attr_id, count, client_id)
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        check.equal(result.status_code, status_code, ErrorMessages.status_code_error(status_code, result.status_code))
        check.equal(result.json()['success'], res, ErrorMessages.get_response_error(result.json()))
        db_connect.execute(Sql.delete_cart(result.json()['data']['id']))

    @pytest.mark.smoke
    def test_check_response_attr_with_response_with_valid_params(self, db_connect):
        body = JsonFixture.product_data(5010187, "", 2, "")
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        cart = json.loads(result.content)['data']['cart']
        count = json.loads(cart)['5010187'][0]['count']
        check.equal(result.status_code, 200, ErrorMessages.status_code_error(200, result.status_code))
        check.equal(count, 2, ErrorMessages.check_param_error(2, count))
        db_connect.execute(Sql.delete_cart(result.json()['data']['id']))

    @pytest.mark.smoke
    def test_check_cart_id_hash_in_response(self, db_connect):
        body = JsonFixture.product_data(5010187, "", 2, "")
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        check.equal(result.status_code, 200, ErrorMessages.status_code_error(200, result.status_code))
        check.is_true(result.json()["data"]["cart_id_hash"], ErrorMessages.check_param_is_present('cart_id_hash'))
        db_connect.execute(Sql.delete_cart(result.json()['data']['id']))

    @pytest.mark.smoke
    def test_check_cart_product_id_in_response(self, db_connect):
        body = JsonFixture.product_data(5010187, "", 2, "")
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        check.equal(result.status_code, 200, ErrorMessages.status_code_error(200, result.status_code))
        check.is_true(result.json()["data"]["id"], ErrorMessages.check_param_is_present('product_id'))
        db_connect.execute(Sql.delete_cart(result.json()['data']['id']))

    @pytest.mark.smoke
    def test_check_add_item_without_attribute_id(self, db_connect):
        body = JsonFixture.product_data(5010187, "", 2, "")
        body.pop('attribute_id')
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        check.equal(result.status_code, 422, ErrorMessages.status_code_error(422, result.status_code))
        db_connect.execute(Sql.delete_cart(result.json()['data']['id']))

    @pytest.mark.parametrize('count, res, status_code', Cart.product_count_list)
    @pytest.mark.smoke
    def test_send_requests_with_different_count(self, db_connect, count, res, status_code):
        body = JsonFixture.product_data(5010187, "", count, "")
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        check.equal(result.status_code, status_code, ErrorMessages.status_code_error(status_code, result.status_code))
        check.equal(result.json()['success'], res, ErrorMessages.succ_mess_error(res, result.json()['success']))
        db_connect.execute(Sql.delete_cart(result.json()['data']['id']))

    @pytest.mark.smoke
    def test_send_request_with_over_count(self, db_connect, get_product_balance):
        body = JsonFixture.product_data(5010187, "", get_product_balance + 1, "")
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        check.equal(result.status_code, 422, 'Error server allows add count more then stock quantity')
        db_connect.execute(Sql.delete_cart(result.json()['data']['id']))

    @pytest.mark.smoke
    def test_send_request_with_max_count(self, db_connect, get_product_balance):
        body = JsonFixture.product_data(5010187, "", get_product_balance, "")
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        assert result.status_code == 200, 'Error server does not allow send request with max quantity'
        db_connect.execute(Sql.delete_cart(result.json()['data']['id']))

    @pytest.mark.smoke
    def test_send_request_with_wrong_client_id(self, db_connect):
        body = JsonFixture.product_data(5010187, "", 1, 000000)
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        check.equal(result.status_code, 422, f'Error server allows send request with wrong client ID param')
        check.is_false(result.json()['success'], f'Server allows create basket with wrong client id')
        db_connect.execute(Sql.delete_cart(result.json()['data']['id']))

    @pytest.mark.smoke
    def test_send_request_with_wrong_type_client_id(self, db_connect):
        body = JsonFixture.product_data(5010187, "", 1, 'FFFFFFF')
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        check.equal(result.status_code, 422, f'Error server allows send request with wrong data type client ID param')
        check.is_false(result.json()['success'], ErrorMessages.status_code_error(False, result.json()['success']))
        db_connect.execute(Sql.delete_cart(result.json()['data']['id']))

    @pytest.mark.smoke
    def test_send_request_without_count_param(self, db_connect):
        body = JsonFixture.product_data(5010187, "", 1, '')
        body.pop('count')
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        check.equal(result.status_code, 422, f'Error server allows send request without count param')
        check.is_false(result.json()['success'], ErrorMessages.status_code_error(False, result.json()['success']))
        db_connect.execute(Sql.delete_cart(result.json()['data']['id']))


class TestDellItem:

    @pytest.mark.smoke
    def test_delete_cart_item_with_valid_param(self, create_cart_item, db_connect):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.del_prod_data()
        result = HttpManager.delete(Cart.del_car_item_endpoint+cart_id_hash, body, JsonFixture.get_header_without_token())
        check.equal(result.status_code, 200, ErrorMessages.status_code_error(200, result.status_code))
        check.is_true(result.json()['success'], ErrorMessages.succ_mess_error(True, result.json()['success']))
        db_connect.execute(Sql.delete_cart(result.json()['data']['id']))

    @pytest.mark.smoke
    def test_check_response_params(self, create_cart_item, db_connect):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.del_prod_data()
        result = HttpManager.delete(Cart.del_car_item_endpoint + cart_id_hash, body, JsonFixture.get_header_without_token()).json()
        check.equal(result['data']['id'], cart_id, ErrorMessages.check_param_error(cart_id, result['data']['id']))
        check.equal(result['data']['cart_id_hash'], cart_id_hash, ErrorMessages.status_code_error(cart_id_hash, result['data']['cart_id_hash']))
        db_connect.execute(Sql.delete_cart(result['data']['id']))
    @pytest.mark.test
    @pytest.mark.smoke
    def test_check_possibility_delete_item_without_hash(self, db_connect):
        body = JsonFixture.del_prod_data()
        result = HttpManager.delete(Cart.del_car_item_endpoint, body, JsonFixture.get_header_without_token())
        assert result.status_code == 405, f'Wrong status code expected status code is 405 but status code from ' \
                                          f'server {result.status_code}'
        try:
            assert not result.json()['success'], f'Success true but expected succes is false message from server ' \
                                            f'is {result.json()["message"]}'
        except JSONDecodeError:
            assert False, f'Response from server is not json format'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={result.json()['data']['id']}")

    @pytest.mark.smoke
    def test_check_possibility_delete_item_with_wrong_cart_id_param(self, create_cart_item, db_connect):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.del_prod_data()
        result = HttpManager.delete(Cart.del_car_item_endpoint + cart_id_hash + 'dfg', body,JsonFixture.get_header_without_token())
        assert result.status_code == 200, f'Wrong status code. Expected result is 200 but actual status code ' \
                                          f'is: {result.status_code}'
        try:
            assert not result.json()['success'], f'Wrong success. Expected result false but actual result ' \
                                                 f'{result.json()["success"]}'
            assert result.json()['message'] == "Cart don`t find", f'Wrong message from server. Expected message is ' \
                                                    f'Cart don`t find. Actual message is: {result.json()["message"]}'
        except JSONDecodeError:
            assert False, f'Response from server is not json format'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={result.json()['data']['id']}")

    @pytest.mark.smoke
    def test_check_possibility_delete_item_with_wrong_product_id(self, create_cart_item, db_connect):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.del_prod_data(product_id=product_id+1)
        result = HttpManager.delete(Cart.del_car_item_endpoint + cart_id_hash, body, JsonFixture.get_header_without_token())
        assert result.status_code == 200, f'Wrong status code. Expected result is 200 but actual status code ' \
                                          f'is: {result.status_code}'
        try:
            assert not result.json()['success'], f'Wrong success. Expected result false but actual result ' \
                                                 f'{result.json()["success"]}'
            assert result.json()['message'] == "Cart don`t find", f'Wrong message from server. Expected message is ' \
                                                f'Cart don`t find. Actual message is: {result.json()["message"]}'
        except JSONDecodeError:
            assert False, f'Response from server is not json format'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={result.json()['data']['id']}")

    @pytest.mark.smoke
    def test_check_possibility_delete_item_with_empty_product_id(self, create_cart_item, db_connect):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.del_prod_data(product_id=None)
        result = HttpManager.delete(Cart.del_car_item_endpoint + cart_id_hash, body, JsonFixture.get_header_without_token())
        assert result.status_code == 200, f'Wrong status code. Expected result is 200 but actual status code ' \
                                          f'is: {result.status_code}'
        try:
            assert not result.json()['success'], f'Wrong success. Expected result false but actual result ' \
                                                 f'{result.json()["success"]}'
            assert result.json()['message'] == "Cart don`t find", f'Wrong message from server. Expected message is ' \
                                                f'Cart don`t find. Actual message is: {result.json()["message"]}'
        except JSONDecodeError:
            assert False, f'Response from server is not json format'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={result.json()['data']['id']}")

    @pytest.mark.smoke
    def test_check_possibility_delete_one_item_from_two_products(self, create_cart_item, db_connect):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.product_data(282799, "", 2, "")
        HttpManager.update(Cart.update_cart_endpoint + cart_id_hash, body, JsonFixture.get_header_without_token())
        result = HttpManager.delete(Cart.del_car_item_endpoint + cart_id_hash, body, JsonFixture.get_header_without_token())
        assert result.status_code == 200, f'Wrong status code. Expected result is 200 but actual status code ' \
                                          f'is: {result.status_code}'
        assert result.json()['success'], f'Wrong success message. Expected result False.' \
                                             f' Actual result {result.json()["success"]}'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={cart_id}")


class TestUpdateCartItems:
    @pytest.mark.smoke
    @pytest.mark.parametrize('count, res, status_code', Cart.product_change_count_list)
    def test_check_possibility_increase_of_product_count(self, create_cart_item, db_connect, count, res, status_code):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.product_data(product_id, "", count, "")
        result = HttpManager.update(Cart.update_cart_endpoint + cart_id_hash, body, JsonFixture.get_header_without_token())
        assert result.status_code == status_code, f'Wrong status code. Expected result is 201 but actual status code ' \
                                          f'is: {result.status_code}'
        actual_count = json.loads(result.content)['data'][str(product_id)][0]['count']
        assert actual_count == count, f'New count item is wrong. Expected result {count}. Actual result {actual_count}'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={cart_id}")

    @pytest.mark.smoke
    def test_check_change_count_to_over_stock(self, create_cart_item, get_product_balance, db_connect):
        cart_id_hash, product_id, cart_id = create_cart_item
        product_count = get_product_balance
        body = JsonFixture.product_data(product_id, "", product_count + 1, "")
        result = HttpManager.update(Cart.update_cart_endpoint + cart_id_hash, body,
                                    JsonFixture.get_header_without_token())
        assert result.status_code == 400, f'Wrong status code. Expected result is 200 but actual status code ' \
                                          f'is: {result.status_code}'
        assert not result.json()['success'], f'Wrong success message. Expected result False.' \
                                             f' Actual result {result.json()["success"]}'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={result.json()['data']['id']}")

    @pytest.mark.smoke
    def test_check_change_count_to_max_count(self, create_cart_item, get_product_balance, db_connect):
        cart_id_hash, product_id, cart_id = create_cart_item
        product_count = get_product_balance
        body = JsonFixture.product_data(product_id, "", product_count, "")
        result = HttpManager.update(Cart.update_cart_endpoint + cart_id_hash, body,
                                    JsonFixture.get_header_without_token())
        actual_count = json.loads(result.content)['data'][str(product_id)][0]['count']
        assert result.status_code == 200, f'Wrong status code. Expected result is 200 but actual status code ' \
                                          f'is: {result.status_code}'
        assert result.json()['success'], f'Wrong success message. Expected result False.' \
                                             f' Actual result {result.json()["success"]}'
        assert actual_count == product_count, f'New count item is wrong. Expected result {product_count}.' \
                                              f' Actual result {actual_count}'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={cart_id}")

    @pytest.mark.smoke
    def test_check_possibility_to_add_new_product_to_cart(self, create_cart_item, db_connect):
        prod_id = 282799
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.product_data(product_id=prod_id, attribute_id="", count=2, client_id="")
        result = HttpManager.update(Cart.update_cart_endpoint + cart_id_hash, body,
                                    JsonFixture.get_header_without_token())
        actual_count = json.loads(result.content)['data'][str(prod_id)][0]['count']
        assert result.status_code == 200, f'Wrong status code. Expected result is 200 but actual status code ' \
                                          f'is: {result.status_code}'
        assert actual_count == 2, f'Wrong product count. Expected result 2. Actual result {actual_count}'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={cart_id}")

    @pytest.mark.smoke
    def test_check_add_to_cart_product_that_unavailable(self, create_cart_item, db_connect):
        prod_id = 6523
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.product_data(product_id=prod_id, attribute_id="", count=2, client_id="")
        result = HttpManager.update(Cart.update_cart_endpoint + cart_id_hash, body,
                                    JsonFixture.get_header_without_token())
        assert result.status_code == 400, f'Wrong status code. Expected result is 200 but actual status code ' \
                                          f'is: {result.status_code}'
        assert not result.json()['success'], f'Wrong success message. Expected result False.' \
                                         f' Actual result {result.json()["success"]}'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={cart_id}")

    @pytest.mark.smoke
    def test_check_possibility_send_request_with_wrong_cart_hash(self, create_cart_item, db_connect):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.product_data(product_id, "", 2, "")
        result = HttpManager.update(Cart.update_cart_endpoint + cart_id_hash + 'sd', body, JsonFixture.get_header_without_token())
        assert not result.json()['success'], f'Wrong success message. Expected result False.' \
                                             f' Actual result {result.json()["success"]}'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={cart_id}")

    @pytest.mark.smoke
    def test_check_possibility_send_request_without_cart_hash(self, create_cart_item, db_connect):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.product_data(product_id, "", 2, "")
        result = HttpManager.update(Cart.update_cart_endpoint, body,JsonFixture.get_header_without_token())
        assert result.status_code == 405, f'Wrong status code. Expected result is 405 but actual status code ' \
                                          f'is: {result.status_code}'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={cart_id}")
