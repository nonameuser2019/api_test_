from tests.utils.json_fixture import JsonFixture
from tests.utils.variables import Cart
from tests.utils.http_manager import HttpManager
import pytest


class TestCartAddItem:
    @pytest.mark.smoke
    def test_check_add_item_with_all_valid_params(self, db_connect):
        body = JsonFixture.product_data(5010187, "", 2, "")
        result = HttpManager.post(Cart.add_cart_item_endpoint, body, headers=JsonFixture.get_header_without_token())
        id = result.json()['data']['id']
        assert result.status_code == 200, f'Wrong status code from server. Status code from server: {result.status_code}'
        assert result.json()['success'], f'Success is not true. Success message from server: {result.json()["success"]}'
        db_connect.execute(f'DELETE FROM cart_temp WHERE id={id}')





