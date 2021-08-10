from tests.utils.json_fixture import JsonFixture
from tests.utils.variables import Orders
from tests.utils.http_manager import HttpManager
import pytest
import pytest_check as check
import random



class TestCreateOrder:
    # these defaults data for new post
    company_guid_np = 'e80b3d9f-091f-11e5-bcf7-6805ca197e53'
    province_guid_np = '7150813b-9b87-11de-822f-000c2965ae0e'
    city_guid_np = 'd40d5ff5-fcca-11e1-a04c-d4ae527baec9'
    office_guid_np = 'd40d5ff5-fcca-11e1-a04c-d4ae527baec9'
    delivery_type = 'b983ffd7-6fee-4341-823c-bc970e783c64'  # delivery company

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
                                                  f' Actual result is {result.status_code}'
        assert result.json()['success'] == result, f'Wrong success result. Expected result is {result}. Actual' \
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
        assert result.json()['success'] == False, 'Wrong success result. Expected result True. Actual ' \
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
        assert result.json()['success'] == False, 'Wrong success result. Expected result False. Actual ' \
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
        assert result.json()['success'] == False, 'Wrong success result. Expected result False. Actual ' \
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
        assert result.json()['success'] == res, 'Wrong success result. Expected result {res}. Actual ' \
                                                'result: {result.json()["success"]}'

    # below all tests with for check delivery type Delivery company with new post
    @pytest.mark.smoke
    def test_create_order_with_different_np_params(self, create_cart_item, db_connect):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.order_data()
        body['delivery']['type_guid'] = 'b983ffd7-6fee-4341-823c-bc970e783c64'
        body['delivery']['company_guid'] = 'e80b3d9f-091f-11e5-bcf7-6805ca197e53'
        body['cart_id_hash'] = cart_id_hash
        db_connect.execute(f'SELECT DescriptionRu, Ref FROM delivery_np_area')
        data = db_connect.fetchall()
        body['delivery']['province_guid'] = data[random.randint(0, len(data))]['Ref']
        db_connect.execute("SELECT DescriptionRu, Ref FROM delivery_np_cities WHERE Area=(%s)",
                           body['delivery']['province_guid'])
        temp_data = db_connect.fetchall()
        body['delivery']['city_guid'] = temp_data[random.randint(0, len(temp_data))]['Ref']
        db_connect.execute("SELECT DescriptionRu, Ref FROM delivery_np_offices WHERE CityRef=(%s)",
                           body['delivery']['city_guid'])
        office_list = db_connect.fetchall()
        body['delivery']['office_guid'] = office_list[0]['Ref']
        result = HttpManager.post(Orders.create_order_endpoint, body, JsonFixture.get_header_without_token())
        assert result.status_code == 200, f'Wrong status code. Expected result is 200. Actual ' \
                                          f'result is {result.status_code}'
        assert result.json()['success'], 'Wrong success result. Expected result True. Actual ' \
                                         'result: {result.json()["success"]}'

    @pytest.mark.smoke
    def test_create_order_without_company_guid_param(self, create_cart_item):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.order_data()
        body['delivery']['type_guid'] = TestCreateOrder.delivery_type
        body['delivery'].pop('company_guid')
        body['cart_id_hash'] = cart_id_hash
        body['delivery']['province_guid'] = TestCreateOrder.province_guid_np
        body['delivery']['city_guid'] = TestCreateOrder.city_guid_np
        body['delivery']['office_guid'] = TestCreateOrder.office_guid_np
        result = HttpManager.post(Orders.create_order_endpoint, body, JsonFixture.get_header_without_token())
        assert result.status_code == 400, f'Wrong status code. Expected result is 400. Actual ' \
                                          f'result is {result.status_code}'
        assert result.json()['success'] == False, 'Wrong success result. Expected result is False. Actual ' \
                                                  'result: {result.json()["success"]}'

    @pytest.mark.smoke
    def test_create_order_with_wrong_company_guid(self, create_cart_item):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.order_data()
        body['delivery']['type_guid'] = TestCreateOrder.delivery_type
        body['delivery']['company_guid'] = 'e80b3d9f-091f-11e5-bcf7-6805ca112548'
        body['cart_id_hash'] = cart_id_hash
        body['delivery']['province_guid'] = TestCreateOrder.province_guid_np
        body['delivery']['city_guid'] = TestCreateOrder.city_guid_np
        body['delivery']['office_guid'] = TestCreateOrder.office_guid_np
        result = HttpManager.post(Orders.create_order_endpoint, body, JsonFixture.get_header_without_token())
        assert result.status_code == 400, f'Wrong status code. Expected result is 400. Actual ' \
                                          f'result is {result.status_code}'
        assert result.json()['success'] == False, 'Wrong success result. Expected result is False. Actual ' \
                                                  'result: {result.json()["success"]}'

    @pytest.mark.smoke
    @pytest.mark.parametrize('guid, res, status_code', Orders.delivery_params)
    def test_create_order_with_different_province_guid(self, create_cart_item, guid, res, status_code):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.order_data()
        body['cart_id_hash'] = cart_id_hash
        body['delivery']['type_guid'] = TestCreateOrder.delivery_type
        body['delivery']['company_guid'] = TestCreateOrder.company_guid_np
        body['delivery']['province_guid'] = guid
        body['delivery']['city_guid'] = TestCreateOrder.city_guid_np
        body['delivery']['office_guid'] = TestCreateOrder.office_guid_np
        result = HttpManager.post(Orders.create_order_endpoint, body, JsonFixture.get_header_without_token())
        assert result.status_code == status_code, f'Wrong status code. Expected result is {status_code}. Actual ' \
                                          f'result is {result.status_code}'
        assert result.json()['success'] == res, f'Wrong success result. Expected result is {res}. Actual ' \
                                                  'result: {result.json()["success"]}'

    @pytest.mark.smoke
    def test_create_order_without_province_guid(self, create_cart_item):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.order_data()
        body['cart_id_hash'] = cart_id_hash
        body['delivery']['type_guid'] = TestCreateOrder.delivery_type
        body['delivery']['company_guid'] = TestCreateOrder.company_guid_np
        body['delivery'].pop('province_guid')
        body['delivery']['city_guid'] = TestCreateOrder.city_guid_np
        body['delivery']['office_guid'] = TestCreateOrder.office_guid_np
        result = HttpManager.post(Orders.create_order_endpoint, body, JsonFixture.get_header_without_token())
        assert result.status_code == 400, f'Wrong status code. Expected result is 400. Actual ' \
                                                  f'result is {result.status_code}'
        assert result.json()['success'] == False, f'Wrong success result. Expected result is False. Actual ' \
                                                'result: {result.json()["success"]}'

    @pytest.mark.smoke
    @pytest.mark.parametrize('guid, res, status_code', Orders.delivery_params)
    def test_create_order_with_different_city_guid(self, create_cart_item, guid, res, status_code):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.order_data()
        body['cart_id_hash'] = cart_id_hash
        body['delivery']['type_guid'] = TestCreateOrder.delivery_type
        body['delivery']['company_guid'] = TestCreateOrder.company_guid_np
        body['delivery']['province_guid'] = TestCreateOrder.province_guid_np
        body['delivery']['city_guid'] = guid
        body['delivery']['office_guid'] = TestCreateOrder.office_guid_np
        result = HttpManager.post(Orders.create_order_endpoint, body, JsonFixture.get_header_without_token())
        check.equal(result.status_code, status_code), f'Wrong status code. Expected result is {status_code}. Actual ' \
                                                                                    f'result is {result.status_code}'
        check.equal(result.json()['success'], res), f'Wrong success result. Expected result is {res}. Actual ' \
                                                        'result: {result.json()["success"]}'

    @pytest.mark.smoke
    def test_create_order_without_city_guid(self, create_cart_item):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.order_data()
        body['cart_id_hash'] = cart_id_hash
        body['delivery']['type_guid'] = TestCreateOrder.delivery_type
        body['delivery'].pop('city_guid')
        body['delivery']['office_guid'] = TestCreateOrder.office_guid_np
        result = HttpManager.post(Orders.create_order_endpoint, body, JsonFixture.get_header_without_token())
        check.equal(result.status_code, 400), f'Wrong status code. Expected result is {400}. Actual ' \
                                                      f'result is {result.status_code}'
        check.is_false(result.json()['success']), f'Wrong success result. Expected result is False. Actual ' \
                                                    'result: {result.json()["success"]}'

    @pytest.mark.smoke
    @pytest.mark.parametrize('guid, res, status_code', Orders.delivery_params)
    def test_create_order_with_different_office_guid(self, create_cart_item, guid, res, status_code):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.order_data()
        body['cart_id_hash'] = cart_id_hash
        body['delivery']['type_guid'] = TestCreateOrder.delivery_type
        body['delivery']['city_guid'] = TestCreateOrder.city_guid_np
        body['delivery']['office_guid'] = guid
        result = HttpManager.post(Orders.create_order_endpoint, body, JsonFixture.get_header_without_token())
        check.equal(result.status_code, status_code), f'Wrong status code. Expected result is {status_code}. Actual ' \
                                              f'result is {result.status_code}'
        check.equal(result.json()['success'], res), f'Wrong success result. Expected result is False. Actual ' \
                                                  'result: {result.json()["success"]}'

    @pytest.mark.smoke
    def test_create_order_without_office_guid(self, create_cart_item):
        cart_id_hash, product_id, cart_id = create_cart_item
        body = JsonFixture.order_data()
        body['cart_id_hash'] = cart_id_hash
        body['delivery']['type_guid'] = TestCreateOrder.delivery_type
        body['delivery']['city_guid'] = TestCreateOrder.city_guid_np
        body['delivery'].pop('office_guid')
        result = HttpManager.post(Orders.create_order_endpoint, body, JsonFixture.get_header_without_token())
        check.equal(result.status_code, 400), f'Wrong status code. Expected result is 400. Actual ' \
                                              f'result is {result.status_code}'
        check.is_false(result.json()['success']), f'Wrong success result. Expected result is False. Actual ' \
                                                  'result: {result.json()["success"]}'



