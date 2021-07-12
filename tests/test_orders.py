from tests.utils.json_fixture import JsonFixture
from tests.utils.variables import Orders
from tests.utils.http_manager import HttpManager
import pytest
import random


class TestCreateOrder:
    # below all tests with for check delivery type pickup
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
    def test_create_order_with_different_delivery_guid(self, create_cart_item, delivery_guid, result, status_code):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.order_data()
        body['cart_id_hash'] = cart_id_hash
        body['delivery']['type_guid'] = delivery_guid
        result = HttpManager.post(Orders.create_order_endpoint, body, JsonFixture.get_header_without_token())
        assert result.status_code == status_code, f'Wrong status code. Expected result is {status_code}.' \
                                                  f' Actual result is {result.status_code }'
        assert result.json()['success'], 'Wrong success result. Expected result True. Actual' \
                                         ' result: {result.json()["success"]}'

    @pytest.mark.smoke
    def test_create_order_without_delivery_type(self, create_cart_item):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.order_data()
        body['cart_id_hash'] = cart_id_hash
        body['delivery'].pop('type_guid')
        result = HttpManager.post(Orders.create_order_endpoint, body, JsonFixture.get_header_without_token())
        assert result.status_code == 400, f'Wrong status code. Expected result is 400. Actual ' \
                                          f'result is {result.status_code}'
        assert result.json()['success'], 'Wrong success result. Expected result True. Actual ' \
                                         'result: {result.json()["success"]}'

    @pytest.mark.smoke
    def test_create_order_without_delivery_type_and_pickup_guid(self, create_cart_item):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.order_data()
        body['cart_id_hash'] = cart_id_hash
        body['delivery'].pop('type_guid')
        body['delivery'].pop('address_pickup_guid')
        result = HttpManager.post(Orders.create_order_endpoint, body, JsonFixture.get_header_without_token())
        assert result.status_code == 400, f'Wrong status code. Expected result is 400. Actual ' \
                                          f'result is {result.status_code}'
        assert result.json()['success'], 'Wrong success result. Expected result True. Actual ' \
                                         'result: {result.json()["success"]}'

    @pytest.mark.smoke
    def test_create_order_without_pick_up_guid(self, create_cart_item):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.order_data()
        body['cart_id_hash'] = cart_id_hash
        body['delivery'].pop('address_pickup_guid')
        result = HttpManager.post(Orders.create_order_endpoint, body, JsonFixture.get_header_without_token())
        assert result.status_code == 400, f'Wrong status code. Expected result is 400. Actual ' \
                                          f'result is {result.status_code}'
        assert result.json()['success'], 'Wrong success result. Expected result True. Actual ' \
                                         'result: {result.json()["success"]}'

    @pytest.mark.smoke
    @pytest.mark.parametrize('pick_up_guid, res, status_code', Orders.adress_pickup_list)
    def test_create_order_with_different_adresses_pickup_guid(self, create_cart_item, pick_up_guid, res, status_code):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.order_data()
        body['cart_id_hash'] = cart_id_hash
        body['delivery']['address_pickup_guid'] = pick_up_guid
        result = HttpManager.post(Orders.create_order_endpoint, body, JsonFixture.get_header_without_token())
        assert result.status_code == status_code, f'Wrong status code. Expected result is {status_code}. Actual ' \
                                          f'result is {result.status_code}'
        assert result.json()['success'] == res, 'Wrong success result. Expected result True. Actual ' \
                                         'result: {result.json()["success"]}'

    # below all tests with for check delivery type Delivery company
    @pytest.mark.test
    @pytest.mark.smoke
    def test_create_order_with_different_np_params(self, create_cart_item, db_connect):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.order_data()
        body['delivery']['company_guid'] = 'e80b3d9f-091f-11e5-bcf7-6805ca197e53'
        body['cart_id_hash'] = cart_id_hash
        db_connect.execute(f'SELECT DescriptionRu, Ref FROM delivery_np_area')
        data = db_connect.fetchall()
        body['delivery']['province_guid'] = data[random.randint(0, len(data))]['Ref']
        db_connect.execute("SELECT DescriptionRu, Ref FROM delivery_np_cities WHERE Area=(%s)", body['delivery']['province_guid'])
        temp_data = db_connect.fetchall()
        body['delivery']['city_guid'] = temp_data[random.randint(0, len(temp_data))]['Ref']
        db_connect.execute("SELECT DescriptionRu, Ref FROM delivery_np_offices WHERE CityRef=(%s)", body['delivery']['city_guid'])
        office_list = db_connect.fetchall()
        body['delivery']['office_guid'] = office_list[0]['Ref']
        result = HttpManager.post(Orders.create_order_endpoint, body, JsonFixture.get_header_without_token())
        assert result.status_code == 200, f'Wrong status code. Expected result is 200. Actual ' \
                                                  f'result is {result.status_code}'
        assert result.json()['success'], 'Wrong success result. Expected result True. Actual ' \
                                                'result: {result.json()["success"]}'

