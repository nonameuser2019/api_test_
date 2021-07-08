from tests.utils.json_fixture import JsonFixture
from tests.utils.variables import Cart, Orders
from tests.utils.http_manager import HttpManager
import pytest
import json
from simplejson.errors import JSONDecodeError

class TestCreateOrder:
    @pytest.mark.smoke
    def test_check_possibility_create_order_pickup_delivery(self, create_cart_item, db_connect):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.order_data()
        body['cart_id_hash'] = cart_id_hash
        result = HttpManager.post(Orders.create_order_endpoint, body, JsonFixture.get_header_without_token())

        assert result.status_code == 200, f'Wrong status code. Expected result is 200. Actual result' \
                                                  f'is {result.status_code}'
        assert result.json()[
            'success'], 'Wrong success result. Expected result True. Actual result: {result.json()["success"]}'

    @pytest.mark.parametrize('delivery_guid, result, status_code', Orders.delivery_type_list)
    @pytest.mark.smoke
    def test_check_possibility_create_order_with_different_delivery_guid(self, create_cart_item, delivery_guid, result, status_code):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.order_data()
        body['cart_id_hash'] = cart_id_hash
        body['delivery']['type_guid'] = delivery_guid
        result = HttpManager.post(Orders.create_order_endpoint, body, JsonFixture.get_header_without_token())
        assert result.status_code == status_code, f'Wrong status code. Expected result is {status_code}. Actual result' \
                                                  f'is {result.status_code }'
        assert result.json()['success'], 'Wrong success result. Expected result True. Actual result: {result.json()["success"]}'

    @pytest.mark.smoke
    def test_check_possibility_create_order_without_delivery_type(self, create_cart_item):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.order_data()
        body['cart_id_hash'] = cart_id_hash
        body['delivery'].pop('type_guid')
        result = HttpManager.post(Orders.create_order_endpoint, body, JsonFixture.get_header_without_token())
        assert result.status_code == 400, f'Wrong status code. Expected result is 400. Actual result' \
                                                  f'is {result.status_code}'
        assert result.json()[
            'success'], 'Wrong success result. Expected result True. Actual result: {result.json()["success"]}'









