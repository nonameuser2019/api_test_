import pytest
from tests.utils.variables import ProfileAdresses
from tests.utils.sql_query import Sql
from tests.utils.json_fixture import JsonFixture
from tests.utils.http_manager import HttpManager
import pytest_check as check
from tests.utils.error_messages import ErrorMessages
from tests.utils import support_tools


class TestAddDeliveryAddress:
    #all test for puick up delivery type
    pick_up_address = 'cacdaf1a-8638-11e7-a99d-a0369f7dce69'

    @pytest.mark.smoke
    def test_send_request_with_valid_pick_up_params(self, auth, get_city_guid, get_delivery_type):
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        delivery_type = support_tools.get_neccessary_guid(get_delivery_type, 'Самовывоз')
        city_guid = support_tools.get_neccessary_guid(get_city_guid, 'Харьков')
        body = JsonFixture.delivery_address('test', delivery_type['guid'], TestAddDeliveryAddress.pick_up_address, city_guid['guid'])
        print(body)
        result = HttpManager.post(ProfileAdresses.add_delivery_endpoint, body, headers=headers)
        check.equal(result.status_code, 201, ErrorMessages.status_code_error(201, result.status_code))
        check.equal(result.json()['data']['fields_data']['type'], 'Самовывоз', 'Wrong delivery type')
        check.equal(result.json()['data']['fields_data']['city'], 'Харьков', 'Wrong city')
        check.equal(result.json()['data']['fields_data']['address_pickup'], 'Харьков, ул. Биологическая, 18', 'Wrong pic up address')

    @pytest.mark.smoke
    def test_send_request_without_token(self, auth, get_city_guid, get_delivery_type):
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'] + '12fdsvgf')
        delivery_type = support_tools.get_neccessary_guid(get_delivery_type, 'Самовывоз')
        city_guid = support_tools.get_neccessary_guid(get_city_guid, 'Харьков')
        body = JsonFixture.delivery_address('test', delivery_type['guid'], TestAddDeliveryAddress.pick_up_address, city_guid['guid'])
        result = HttpManager.post(ProfileAdresses.add_delivery_endpoint, body, headers=headers)
        check.equal(result.status_code, 401, ErrorMessages.status_code_error(401, result.status_code))

    @pytest.mark.smoke
    def test_send_request_without_type_guid(self, auth, get_city_guid, get_delivery_type):
        delivery_type = support_tools.get_neccessary_guid(get_delivery_type, 'Самовывоз')
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        city_guid = support_tools.get_neccessary_guid(get_city_guid, 'Харьков')
        body = JsonFixture.delivery_address('test', delivery_type['guid'], TestAddDeliveryAddress.pick_up_address,
                                            city_guid['guid'])
        body.pop('type_guid')
        result = HttpManager.post(ProfileAdresses.add_delivery_endpoint, body, headers=headers)
        check.equal(result.status_code, 422, ErrorMessages.status_code_error(422, result.status_code))

    @pytest.mark.smoke
    @pytest.mark.parametrize('guid, status_code', ProfileAdresses.delivery_type_list)
    def test_send_request_with_wrong_type_guid(self, auth, get_city_guid, get_delivery_type, guid, status_code):
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        delivery_type = guid
        city_guid = support_tools.get_neccessary_guid(get_city_guid, 'Харьков')
        body = JsonFixture.delivery_address('test', delivery_type, TestAddDeliveryAddress.pick_up_address,
                                            city_guid['guid'])
        result = HttpManager.post(ProfileAdresses.add_delivery_endpoint, body, headers=headers)
        check.equal(result.status_code, status_code, ErrorMessages.status_code_error(status_code, result.status_code))

    @pytest.mark.smoke
    def test_send_request_without_city_guid(self, auth, get_city_guid, get_delivery_type):
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        delivery_type = support_tools.get_neccessary_guid(get_delivery_type, 'Самовывоз')
        city_guid = support_tools.get_neccessary_guid(get_city_guid, 'Харьков')
        body = JsonFixture.delivery_address('test', delivery_type['guid'], TestAddDeliveryAddress.pick_up_address,
                                            city_guid['guid'])
        body.pop('city_guid')
        result = HttpManager.post(ProfileAdresses.add_delivery_endpoint, body, headers=headers)
        check.equal(result.status_code, 422, ErrorMessages.status_code_error(422, result.status_code))

    @pytest.mark.smoke
    @pytest.mark.parametrize('guid, status_code', ProfileAdresses.city_guid_list)
    def test_send_request_with_wrong_city_guid(self, auth, get_city_guid, get_delivery_type, guid, status_code):
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        delivery_type = support_tools.get_neccessary_guid(get_delivery_type, 'Самовывоз')
        city_guid = guid
        body = JsonFixture.delivery_address('test', delivery_type['guid'], TestAddDeliveryAddress.pick_up_address,
                                            city_guid)
        result = HttpManager.post(ProfileAdresses.add_delivery_endpoint, body, headers=headers)
        check.equal(result.status_code, status_code, ErrorMessages.status_code_error(status_code, result.status_code))

    @pytest.mark.smoke
    def test_send_request_without_pick_up_address_delivery(self, auth, get_city_guid, get_delivery_type):
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        delivery_type = support_tools.get_neccessary_guid(get_delivery_type, 'Самовывоз')
        city_guid = support_tools.get_neccessary_guid(get_city_guid, 'Харьков')
        body = JsonFixture.delivery_address('test', delivery_type['guid'], TestAddDeliveryAddress.pick_up_address,
                                            city_guid['guid'])
        body.pop('address_pickup_guid')
        result = HttpManager.post(ProfileAdresses.add_delivery_endpoint, body, headers=headers)
        check.equal(result.status_code, 422, ErrorMessages.status_code_error(422, result.status_code))

    @pytest.mark.smoke
    @pytest.mark.parametrize('guid, status_code', ProfileAdresses.city_guid_list)
    def test_send_request_with_wrong_pick_up_addr(self, auth, get_city_guid, get_delivery_type, guid, status_code):
        headers = JsonFixture.get_headers(auth.json()['data']['access_token'])
        delivery_type = support_tools.get_neccessary_guid(get_delivery_type, 'Самовывоз')
        city_guid = support_tools.get_neccessary_guid(get_city_guid, 'Харьков')
        body = JsonFixture.delivery_address('test', delivery_type['guid'], guid, city_guid['guid'])
        result = HttpManager.post(ProfileAdresses.add_delivery_endpoint, body, headers=headers)
        check.equal(result.status_code, status_code, ErrorMessages.status_code_error(status_code, result.status_code))