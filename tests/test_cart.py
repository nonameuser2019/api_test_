import allure

from tests.utils.json_fixture import JsonFixture
from tests.utils.variables import Cart
from tests.utils.http_manager import HttpManager
from tests.utils.sql_query import Sql
from tests.utils.error_messages import ErrorMessages
from tests.utils.allure_step import AllureStep
import pytest
import json
import pytest_check as check


class TestCartAddItem:
    @pytest.mark.parametrize('product_id, attr_id, count, client_id, res, status_code', Cart.product_id_list)
    @pytest.mark.smoke
    @allure.title('Check add to cart product with difference params')
    def test_check_add_item_with_different_id_param(self, db_connect, product_id, attr_id, count, client_id, res,
                                                    status_code):
        body = JsonFixture.product_data(product_id, attr_id, count, client_id)
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_status_code(200)):
            assert result.status_code == status_code, ErrorMessages.status_code_error(status_code, result.status_code)
        with allure.step(AllureStep.check_success_message(True)):
            assert result.json()['success'], ErrorMessages.succ_mess_error(True, result.json()['success'])
        db_connect.execute(Sql.delete_cart(result.json()['data']['id']))

    @pytest.mark.smoke
    @allure.title('Check product count')
    def test_check_product_count_from_response(self, db_connect):
        body = JsonFixture.product_data(5010187, "", 2, "")
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        cart = json.loads(result.content)['data']['cart']
        count = json.loads(cart)['5010187'][0]['count']
        with allure.step(AllureStep.check_status_code(200)):
            assert result.status_code == 200, ErrorMessages.status_code_error(200, result.status_code)
        with allure.step(AllureStep.check_response_param(count, "product_count")):
            assert count == 2, ErrorMessages.check_param_error(2, count)
        db_connect.execute(Sql.delete_cart(result.json()['data']['id']))

    @pytest.mark.smoke
    @allure.title('Check cart_hash')
    def test_check_cart_id_hash_in_response(self, db_connect):
        body = JsonFixture.product_data(5010187, "", 2, "")
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        cart_id_hash = result.json()["data"]["cart_id_hash"]
        with allure.step(AllureStep.check_status_code(200)):
            assert result.status_code == 200, ErrorMessages.status_code_error(200, result.status_code)
        with allure.step(AllureStep.check_response_param(cart_id_hash, "cart_id_hash")):
            assert cart_id_hash, f'Error length cart id hash is empty'
        db_connect.execute(Sql.delete_cart(result.json()['data']['id']))

    @pytest.mark.smoke
    @allure.title('Check product id')
    def test_check_cart_product_id_in_response(self, db_connect):
        body = JsonFixture.product_data(5010187, "", 2, "")
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        product_id = result.json()["data"]["id"]
        with allure.step(AllureStep.check_status_code(200)):
            assert result.status_code == 200, ErrorMessages.status_code_error(200, result.status_code)

        with allure.step(AllureStep.check_response_param(product_id, "product)id")):
            assert result.status_code == 200, f'Wrong product id'
        db_connect.execute(Sql.delete_cart(result.json()['data']['id']))

    @pytest.mark.smoke
    @allure.title('Check status code with response without attribute_id in body')
    def test_check_add_item_without_attribute_id(self, db_connect):
        body = JsonFixture.product_data(5010187, "", 2, "")
        body.pop('attribute_id')
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_status_code(200)):
            assert result.status_code == 422, ErrorMessages.status_code_error(422, result.status_code)
        db_connect.execute(Sql.delete_cart(result.json()['data']['id']))

    @pytest.mark.parametrize('count, res, status_code', Cart.product_count_list)
    @pytest.mark.smoke
    @allure.title('Test with different count')
    def test_send_requests_with_different_count(self, db_connect, count, res, status_code):
        body = JsonFixture.product_data(5010187, "", count, "")
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_status_code(200)):
            assert result.status_code == status_code, ErrorMessages.status_code_error(status_code, result.status_code)
        with allure.step(AllureStep.check_success_message(True)):
            assert result.json()['success'], ErrorMessages.succ_mess_error(True, result.json()['success'])
        db_connect.execute(Sql.delete_cart(result.json()['data']['id']))

    @pytest.mark.smoke
    @allure.title('Check possibility to add to cart product with over count')
    def test_send_request_with_over_count(self, db_connect, get_product_balance):
        body = JsonFixture.product_data(5010187, "", get_product_balance + 1, "")
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_status_code(200)):
            assert result.status_code == 422, ErrorMessages.status_code_error(422, result.status_code)
        db_connect.execute(Sql.delete_cart(result.json()['data']['id']))

    @pytest.mark.smoke
    @allure.title('Positive case with max product count')
    def test_send_request_with_max_count(self, db_connect, get_product_balance):
        body = JsonFixture.product_data(5010187, "", get_product_balance, "")
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_status_code(200)):
            assert result.status_code == 200, 'Error server does not allow send request with max quantity'
        db_connect.execute(Sql.delete_cart(result.json()['data']['id']))

    @pytest.mark.smoke
    @allure.title('Negative case with wrong client id')
    def test_send_request_with_wrong_client_id(self, db_connect):
        body = JsonFixture.product_data(5010187, "", 1, 000000)
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_response_param(000000, 'client_id')):
            assert result.status_code == 422, f'Error server allows send request with wrong client ID param'
        db_connect.execute(Sql.delete_cart(result.json()['data']['id']))

    @pytest.mark.smoke
    @allure.title('Negative test, send request without product count param')
    def test_send_request_without_count_param(self, db_connect):
        body = JsonFixture.product_data(5010187, "", 1, '')
        body.pop('count')
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_status_code(422)):
            assert result.status_code == 200, 'Error server allows send request without count param'
        db_connect.execute(Sql.delete_cart(result.json()['data']['id']))


class TestDellItem:

    @pytest.mark.smoke
    @allure.title('Positive case. delete cart')
    def test_delete_cart_item_with_valid_param(self, create_cart_item, db_connect):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.del_prod_data()
        result = HttpManager.delete(Cart.del_car_item_endpoint + cart_id_hash, body,
                                    JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_status_code(200)):
            assert result.status_code == 200, ErrorMessages.status_code_error(200, result.status_code)
        with allure.step(AllureStep.check_success_message(True)):
            assert result.json()['success'], ErrorMessages.succ_mess_error(True, result.json()['success'])
        db_connect.execute(Sql.delete_cart(result.json()['data']['id']))

    @pytest.mark.smoke
    @allure.title('Negative case. Try to delete cart. Send request without hash')
    def test_check_possibility_delete_item_without_hash(self):
        body = JsonFixture.del_prod_data()
        result = HttpManager.delete(Cart.del_car_item_endpoint, body, JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_status_code(405)):
            assert result.status_code == 405, ErrorMessages.status_code_error(405, result.status_code)

    @pytest.mark.smoke
    @allure.title('Delete cart. Use wrong hash')
    def test_check_possibility_delete_item_with_wrong_hash(self, create_cart_item, db_connect):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.del_prod_data()
        result = HttpManager.delete(Cart.del_car_item_endpoint + cart_id_hash + 'dfg', body,
                                    JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_success_message(False)):
            assert result.json()['success'] is False, ErrorMessages.succ_mess_error(False, result.json()['success'])

    @pytest.mark.smoke
    @allure.title('Negative case. Delete cart item using wrong product id')
    def test_check_possibility_delete_item_with_wrong_product_id(self, create_cart_item, db_connect):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.del_prod_data(product_id=product_id + 1)
        result = HttpManager.delete(Cart.del_car_item_endpoint + cart_id_hash, body,
                                    JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_status_code(422)):
            assert result.status_code == 422, ErrorMessages.status_code_error(422, result.status_code)
        db_connect.execute(Sql.delete_cart(result['data']['id']))

    @pytest.mark.smoke
    @allure.title('Negative test, delete item with empty product id')
    def test_check_possibility_delete_item_with_empty_product_id(self, create_cart_item):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.del_prod_data(product_id="")
        result = HttpManager.delete(Cart.del_car_item_endpoint + cart_id_hash, body,
                                    JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_status_code(422)):
            assert result.status_code == 422, ErrorMessages.status_code_error(422, result.status_code)
        with allure.step(AllureStep.check_success_message(False)):
            assert result.json()['success'] is False, ErrorMessages.succ_mess_error(False, result.json()['success'])

    @pytest.mark.smoke
    @allure.title('Positive case, delete one product from two')
    def test_check_possibility_delete_one_item_from_two_products(self, create_cart_item, db_connect):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.product_data(282799, "", 2, "")
        HttpManager.update(Cart.update_cart_endpoint + cart_id_hash, body, JsonFixture.get_header_without_token())
        result = HttpManager.delete(Cart.del_car_item_endpoint + cart_id_hash, body,
                                    JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_status_code(200)):
            assert result.status_code == 200, ErrorMessages.status_code_error(200, result.status_code)
        with allure.step(AllureStep.check_success_message(True)):
            assert result.json()['success'], ErrorMessages.succ_mess_error(True, result.json()['success'])
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={cart_id}")


class TestUpdateCartItems:

    @pytest.mark.smoke
    @pytest.mark.parametrize('count, res, status_code', Cart.product_change_count_list)
    @allure.title('Positive case, check increase of product in cart')
    def test_check_possibility_increase_of_product_count(self, create_cart_item, db_connect, count, res, status_code):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.product_data(product_id, "", count, "")
        result = HttpManager.update(Cart.update_cart_endpoint + cart_id_hash, body,
                                    JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_status_code(status_code)):
            assert result.status_code == status_code, ErrorMessages.status_code_error(status_code, result.status_code)
        actual_count = json.loads(result.content)['data'][str(product_id)][0]['count']
        with allure.step(AllureStep.check_response_param(count, "product_count")):
            assert actual_count == count, f'New count item is wrong. Expected result {count}. Actual result {actual_count}'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={cart_id}")

    @pytest.mark.smoke
    @allure.title("Negative case. Add to cart product with over count")
    def test_check_change_count_to_over_stock(self, create_cart_item, get_product_balance, db_connect):
        cart_id_hash, product_id, cart_id = create_cart_item
        product_count = get_product_balance
        body = JsonFixture.product_data(product_id, "", product_count + 1, "")
        result = HttpManager.update(Cart.update_cart_endpoint + cart_id_hash, body,
                                    JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_status_code(400)):
            assert result.status_code == 400, ErrorMessages.status_code_error(400, result.status_code)
        with allure.step(AllureStep.check_success_message(result.json()['success'])):
            assert not result.json()['success'], ErrorMessages.succ_mess_error(False, result.json()['success'])
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={result.json()['data']['id']}")

    @pytest.mark.smoke
    @allure.title('Positive case, add max product count to basket')
    def test_check_change_count_to_max_count(self, create_cart_item, get_product_balance, db_connect):
        cart_id_hash, product_id, cart_id = create_cart_item
        product_count = get_product_balance
        body = JsonFixture.product_data(product_id, "", product_count, "")
        result = HttpManager.update(Cart.update_cart_endpoint + cart_id_hash, body,
                                    JsonFixture.get_header_without_token())
        actual_count = json.loads(result.content)['data'][str(product_id)][0]['count']
        with allure.step(AllureStep.check_response_param(product_count, 'product_count')):
            assert actual_count == product_count, f'New count item is wrong. Expected result {product_count}.' \
                                              f' Actual result {actual_count}'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={cart_id}")

    @pytest.mark.smoke
    @allure.title('Positive case. Add product to present cart')
    def test_check_possibility_to_add_new_product_to_cart(self, create_cart_item, db_connect):
        prod_id = 282799
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.product_data(product_id=prod_id, attribute_id="", count=2, client_id="")
        result = HttpManager.update(Cart.update_cart_endpoint + cart_id_hash, body,
                                    JsonFixture.get_header_without_token())
        actual_count = json.loads(result.content)['data'][str(prod_id)][0]['count']
        with allure.step(AllureStep.check_status_code(200)):
            assert result.status_code == 200, ErrorMessages.status_code_error(200, result.status_code)
        with allure.step(AllureStep.check_response_param(actual_count, "actual-count")):
            assert actual_count == 2, f'Wrong product count. Expected result 2. Actual result {actual_count}'
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={cart_id}")

    @pytest.mark.smoke
    @allure.title('Negative case. Add to cart unavailable product')
    def test_check_add_to_cart_product_that_unavailable(self, create_cart_item, db_connect):
        prod_id = 6523
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.product_data(product_id=prod_id, attribute_id="", count=2, client_id="")
        result = HttpManager.update(Cart.update_cart_endpoint + cart_id_hash, body,
                                    JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_status_code(400)):
            assert result.status_code == 400, ErrorMessages.status_code_error(400, result.status_code)
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={cart_id}")

    @pytest.mark.smoke
    @allure.title('negative case, change cart use wrong cart_id_hash')
    def test_check_possibility_send_request_with_wrong_cart_hash(self, create_cart_item, db_connect):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.product_data(product_id, "", 2, "")
        result = HttpManager.update(Cart.update_cart_endpoint + cart_id_hash + 'sd', body,
                                    JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_success_message(False)):
            assert not result.json()['success'], ErrorMessages.succ_mess_error(False, result.json()['success'])
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={cart_id}")

    @pytest.mark.smoke
    @allure.title('Negative case. Try to send request without cart hash')
    def test_check_possibility_send_request_without_cart_hash(self, create_cart_item, db_connect):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.product_data(product_id, "", 2, "")
        result = HttpManager.update(Cart.update_cart_endpoint, body, JsonFixture.get_header_without_token())
        with allure.step(AllureStep.check_status_code(405)):
            assert result.status_code == 405,ErrorMessages.status_code_error(405, result.status_code)
        db_connect.execute(f"DELETE FROM cart_temp WHERE id={cart_id}")
