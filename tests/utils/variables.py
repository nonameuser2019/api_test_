import pytest
from .support_tools import *

class ClientRegistration:
    reg_endpoint = 'https://api.platform.masterservice.company/api/v1/register'
    name_list = [('Александр', True, 200), ('Марк-Эдгар', True, 200), ('Mark-Edgar', True, 200), ('', False, 422),
                 ('Al', True, 200), ('Alex1', False, 422), ('   ', False, 422), ('Alex+!', False, 422)
                 ]
    phone_list = [
        ('0685340603', True, 200), ('30685340603', False, 422), ('380685340603', True, 200),
        ('+380685340603', True, 200), ('685340603', False, 422), ('+3800685340603', False, 422),
        ('++380685340603', False, 422), ('+38006853406f3', False, 422), ('+38006853406F3', False, 422),
        ('+38006853406а3', False, 422), ('+38006853406А3', False, 422), ('068534060!', False, 422),
        ('06853&060!', False, 422), ("", False, 422), (False, False, 422), (True, False, 422),
        (380685340603, False, 422)
    ]
    email_list = [
        ('TEST@gmail.com', True, 200), ('TEST777@gmail.com', True, 200), ('test-777@gmail.com', True, 200),
        ('test_777@gmail.com', True, 200), ('test.777@gmail.com', True, 200), ('test.77.7@gmail.com', True, 200),
        ('@gmail.com', False, 422), ('user@gmail.', False, 422), ('user1gmail.com', False, 422),
        ('user@gmailcom', False, 422), ('u..ser@gmail.com', False, 422)
    ]
    password_list = [
        ('!Qwerty123', True, 200), ('Uytrew1', False, 422), ('FRASDFN1', True, 200), ('qazwsx2', False, 422),
        ('qazwsdfG', True, 200), ('Qwerty1щ', False, 422), ('Qwerty1Ц', False, 422)
    ]


class ClientAuth:
    login_endpoint = 'https://api.platform.masterservice.company/api/v1/login'
    login_password_list = [
        ('', 'Qwerty123', False), ('main_test@qa.com', '', False), ('', '', False), ('main_test@qa.co', 'Qwerty123', False),
        ('main_test@qa.com', 'False', False), ('main_test@qa.co', 'Qwerty1231', False)
    ]

class ClientLogOut:
    logout_endpoint = 'https://api.platform.masterservice.company/api/v1/customer/logout'

class ClientProfileEdit:
    edit_profile_endpoint = 'https://api.platform.masterservice.company/api/v1/customer/profile/edit'

class Cart:

    add_cart_item_endpoint = 'https://api.platform.masterservice.company/api/v1/cart/'
    del_car_item_endpoint = 'https://api.platform.masterservice.company/api/v1/cart/'
    update_cart_endpoint = 'https://api.platform.masterservice.company/api/v1/cart/'
    get_cart_endpoint = 'https://api.platform.masterservice.company/api/v1/'
    product_id_list = [
        (5010187, "", 1, "", True, 200), (None, "", 2, "", False, 422), ("", "", 1, "", False, 422), (100500100, "", 1, "", False, 422),
        ("FFF", "", 1, "", False, 422), ("5010187", "", 2, "", False, 422)
    ]

    product_count_list = [
        (None, False, 422), (0, False, 422), (-1, False, 422), ("FFF", False, 422), (1, True, 200)
    ]
    product_change_count_list = [
        (5, True, 200), (1, True, 200), (0, False, 422), (2, False, 422)
    ]

class Orders:
    create_order_endpoint = 'https://api.platform.masterservice.company/api/v1/order-add'
    delivery_type_list = [
        ('f442a653-f442a653-f442a653', False, 422), ('', False, 422),  (None, False, 422), (True, False, 422),
        (False, False, 422), (0, False, 422)
    ]
    adress_pickup_list = [
        ('', False, 422), (None, False, 422), (True, False, 422), (False, False, 422),
        ('cacdaf1a-8638-11e7-a99d-a0369f7dce00', False, 422)
    ]
    company_guid_list = [
        ('e80b3d9f-091f-11e5-bcf7-6805ca197e01', False, 422),
    ]
    delivery_params = [
        ('e80b3d9f-091f-11e5-bcf7-dpolgkeigjiej', False, 422), ("", False, 422), (None, False, 422), (False, False, 422),
        (True, False, 422)
    ]
    pick_up_addresses = [
        ('cacdaf1a-8638-11e7-a99d-a0369f7dce69', True, 200), ('c6568da3-bd65-11e7-a99d-509a4ca97561', True, 200),
        ('66b1b46b-0a4b-11e8-a9a1-509a4ca97561', True, 200), ('32681a55-8e4b-11e8-a9aa-509a4ca97561', True, 200),
        ('b7ed3201-8638-11e7-a99d-a0369f7dce69', True, 200), ('e4161498-cfce-11e9-a9b9-509a4ca97563', True, 200),
        ('035b2c03-8f1b-11e8-a9aa-509a4ca97561', True, 200)
    ]

class OrdersByClick:
    oreder_by_click_endpoint = 'https://api.platform.masterservice.company/api/v1/order-one-click-add'
    product_id_list = [
        ('1005008736925', 422, False), ("", 422, False), (True, 422, False), (False, 422, False),
        ('Hey Bro!', 422, False)
    ]
    attribute_id_list = [
        ('', 422, False), ('123', 422, False), (123, 422, False)
    ]

class OrdersHistory:
    get_orders_endpoint = 'https://api.platform.masterservice.company/api/v1/orders'
    per_page_list = [
        (-15, 422, '15'), ('15', 200, '15'), ('-15', 422, '15')
    ]

class B2cProfile:
    get_b2c_prof_endpoint = 'https://api.platform.masterservice.company/api/v1/b2c-profile'
    change_info_endpoint = 'https://api.platform.masterservice.company/api/v1/b2c-profile/change-info'
    name_list = [
        ('a', 422), ('al', 200), (generate_long_name(128), 200), (generate_long_name(129), 422), ('Alex', 200),
        ('Alex First', 200), ('Alex123', 422), ('     ', 422), ('Alex-First', 200), ('Alex#+=', 422)
    ]

class ProfileAdresses:
    add_delivery_endpoint = 'https://api.platform.masterservice.company/api/v1/delivery'
    delivery_type_list = [
        ('cacdaf1a-8638-11e7-a99d-a0369f7dce69', 422), ('', 422), (True, 422)
    ]
    city_guid_list = [
        ('7150812c-9b87-11de-822f-000c2965ae0e', 422), ('', 422), (True, 422)
    ]
    pick_up_delivery_adr_list = [
        ('7150812c-9b87-11de-822f-000c2965ae0e', 422), ('', 422), (True, 422)
    ]