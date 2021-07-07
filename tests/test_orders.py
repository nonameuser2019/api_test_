from tests.utils.json_fixture import JsonFixture
from tests.utils.variables import Cart, Orders
from tests.utils.http_manager import HttpManager
import pytest
import json
from simplejson.errors import JSONDecodeError

class TestCreateOrder:
    @pytest.mark.test
    @pytest.mark.smoke
    def test_check_possibility_create_order_pickup_delivery(self, create_cart_item, db_connect):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.order_data()
        body['cart_id_hash'] = cart_id_hash
        result = HttpManager.post(Orders.create_order_endpoint, body, JsonFixture.get_header_without_token())
        assert result.status_code == 200 and result.json()['success'], f'Cart does not delete. Message from server: ' \
                                                                       f'{result.json()["message"]}'
        assert result.json()['success'], 'Worng success result. Expected result True. Actual result: {result.json()["success"]}'