from tests.utils.json_fixture import JsonFixture
from tests.utils.variables import Cart
from tests.utils.http_manager import HttpManager
import pytest
import json
from simplejson.errors import JSONDecodeError


class TestCartAddItem:

    @pytest.mark.parametrize('product_id, attr_id, count, client_id, res, status_code', Cart.product_id_list)
    @pytest.mark.smoke
    def test_check_add_item_with_different_id_param(self, db_connect, product_id, attr_id, count, client_id, res,
                                                    status_code):
        body = JsonFixture.product_data(product_id, attr_id, count, client_id)
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        assert result.status_code == status_code, f'Wrong status code from server. Status code from server: {result.status_code}'
        assert result.json()[
                   'success'] == res, f'Expected status code 400. Success message from server: {result.json()["success"]}'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={result.json()['data']['id']}")

    @pytest.mark.smoke
    def test_check_response_attr_with_response_with_valid_params(self, db_connect):
        product_id = 5010187
        attr_id = ""
        count = 2
        client_id = ""
        body = JsonFixture.product_data(product_id, attr_id, count, client_id)
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        cart = json.loads(result.content)['data']['cart']
        assert result.status_code == 200, f'Wrong status code from server. Status code from server: {result.status_code}'
        assert json.loads(cart)['5010187'][0]['count'] == count
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
        body = JsonFixture.product_data(5010187, None, 2, "")
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
        assert result.json()[
                   'success'] == res, f'Wrong result Expected result: {res} Actual result: {result.json()["success"]}'
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


class TestDellItem:
    @pytest.mark.smoke
    def test_fixture_create_item(self, create_cart_item):
        cart_id_hash, product_id, cart_id = create_cart_item
        assert isinstance(cart_id_hash, str) and isinstance(product_id, int), f'Wrong data types cart_id_hash expected' \
        f' data type is string actual type is {type(cart_id_hash)} and expected data type for product_id is int and' \
                                                                              f' actual result is: {type(product_id)}'
    @pytest.mark.smoke
    def test_delete_cart_item_with_valid_param(self, create_cart_item, db_connect):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.del_prod_data()
        result = HttpManager.delete(Cart.del_car_item_endpoint+cart_id_hash, body, JsonFixture.get_header_without_token())
        assert result.status_code == 200 and result.json()['success'], f'Cart does not delete. Message from server: ' \
                                                                       f'{result.json()["message"]}'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={result.json()['data']['id']}")

    @pytest.mark.smoke
    def test_check_response_params(self, create_cart_item, db_connect):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.del_prod_data()
        result = HttpManager.delete(Cart.del_car_item_endpoint + cart_id_hash, body, JsonFixture.get_header_without_token()).json()
        assert result['data']['id'] == cart_id and result['data']['cart_id_hash'] == cart_id_hash, f'Wrong response ' \
        f'parametrs cart_id and cart_id_hash'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={result['data']['id']}")

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

    # Below are test from update cart items
    @pytest.mark.smoke
    @pytest.mark.parametrize('count, res, status_code', Cart.product_change_count_list)
    def test_check_possibility_increase_of_product_count(self, create_cart_item, db_connect, count, res, status_code):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.product_data(product_id, "", count, "")
        result = HttpManager.delete(Cart.update_cart_endpoint + cart_id_hash, body, JsonFixture.get_header_without_token())
        assert result.status_code == 200, f'Wrong status code. Expected result is 201 but actual status code ' \
                                          f'is: {result.status_code}'
        try:
            cart = json.loads(result.content)['data']['cart']
            actual_count = json.loads(cart)['5010187'][0]['count']
            assert actual_count == count, f'New count item is wrong. Expected result {count}. Actual result {actual_count}'
        except JSONDecodeError:
            assert False, f'Response from server is not json format'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={result.json()['data']['id']}")

    @pytest.mark.smoke
    def test_check_change_count_to_over_stock(self, create_cart_item, get_product_balance, db_connect):
        cart_id_hash, product_id, cart_id = create_cart_item
        product_count = get_product_balance
        print(type(product_count))
        body = JsonFixture.product_data(product_id, "", product_count + 1, "")
        result = HttpManager.delete(Cart.update_cart_endpoint + cart_id_hash, body,
                                    JsonFixture.get_header_without_token())
        assert result.status_code == 200, f'Wrong status code. Expected result is 201 but actual status code ' \
                                          f'is: {result.status_code}'
        try:
            cart = json.loads(result.content)['data']['cart']
            actual_count = json.loads(cart)['5010187'][0]['count']
            #I need to write assert bofore the update method will be fixed
        except JSONDecodeError:
            assert False, f'Response from server is not json format'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={result.json()['data']['id']}")


    # Below are test from get cart item
    @pytest.mark.smoke
    def test_get_cart_item_with_valid_hash(self, create_cart_item, db_connect):
        cart_id_hash, product_id, cart_id = create_cart_item
        result = HttpManager.get(Cart.get_cart_endpoint, headers=JsonFixture.get_header_without_token())
        assert result.status_code == 200, f'Wrong status code. Expected result is 200 but actual status code ' \
                                          f'is: {result.status_code}'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={result.json()['data']['id']}")
