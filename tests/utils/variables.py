import pytest


class ClientRegistration:
    reg_endpoint = 'https://api.platform.masterservice.company/api/v1/customer/register'
    name_list = [('Александр', True), ('Марк-Эдгар', True), ('Mark-Edgar', True), ('', False), ('Al', False),
                 ('Alex1', False), ('   ', False), ('Alex+!', False)
                 ]
    phone_list = [
        ('0685340603', True, 200), ('30685340603', True, 200), ('380685340603', True, 200),
        ('+380685340603', True, 200), ('685340603', False, 400), ('+3800685340603', False, 400),
        ('++380685340603', False, 400), ('+38006853406f3', False, 400), ('+38006853406F3', False, 400),
        ('+38006853406а3', False, 400), ('+38006853406А3', False, 400), ('068534060!', False, 400),
        ('06853&060!', False, 400), ("", False, 400), (False, False, 400), (True, False, 400),
        (380685340603, False, 400)
    ]
    email_list = [
        ('TEST@gmail.com', True), ('TEST777@gmail.com', True), ('test-777@gmail.com', True), ('test_777@gmail.com', True),
        ('test.777@gmail.com', True), ('test.77.7@gmail.com', True), ('@gmail.com', False), ('user@gmail.', False),
        ('user1gmail.com', False), ('user@gmailcom', False), ('u..ser@gmail.com', False)
    ]
    password_list = [
        ('!Qwerty123', True), ('Uytrew1', False), ('FRASDFN1', False), ('qazwsx2', False), ('qazwsdfG', False),
        ('Qwerty1щ', False), ('Qwerty1Ц', False)
    ]


class ClientAuth:
    login_endpoint = 'https://api.platform.masterservice.company/api/v1/customer/login'
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
        (5010187, "", 1, "", True, 200), (None, "", 2, "", False, 400), ("", "", 1, "", False, 400), (100500100, "", 1, "", False, 400),
        ("FFF", "", 1, "", False, 400), ("5010187", "", 2, "", False, 400)
    ]

    product_count_list = [
        (None, False, 400), (0, False, 400), (-1, False, 400), ("FFF", False, 400), (1, True, 200)
    ]
    product_change_count_list = [
        (5, True, 200), (1, True, 200), (0, False, 400), (2, False, 400)
    ]

class Orders:
    create_order_endpoint = 'https://api.platform.masterservice.company/api/v1/order-add'
    delivery_type_list = [
        ('f442a653-f442a653-f442a653', False, 400), ('', False, 400),  (None, False, 400), (True, False, 400),
        (False, False, 400), (0, False, 400)
    ]
    adress_pickup_list = [
        ('', False, 400), (None, False, 400), (True, False, 400), (False, False, 400),
        ('cacdaf1a-8638-11e7-a99d-a0369f7dce00', False, 400)
    ]
    company_guid_list = [
        ('e80b3d9f-091f-11e5-bcf7-6805ca197e01', False, 400),
    ]
    delivery_params = [
        ('e80b3d9f-091f-11e5-bcf7-dpolgkeigjiej', False, 400), ("", False, 400), (None, False, 400), (False, False, 400),
        (True, False, 400)
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
        ('1005008736925', 400, False), ("", 400, False), (True, 400, False), (False, 400, False),
        ('Hey Bro!', 400, False)
    ]
    attribute_id_list = [
        ('', 400, False), ('123', 400, False), (123, 400, False)
    ]
