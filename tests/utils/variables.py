import pytest


class ClientRegistration:
    reg_endpoint = 'https://api.platform.masterservice.company/api/v1/customer/register'
    name_list = [('Александр', True), ('Марк-Эдгар', True), ('Mark-Edgar', True), ('', False), ('Al', False),
                 ('Alex1', False), ('   ', False), ('Alex+!', False)
                 ]
    phone_list = [
        ('0685340603', True), ('30685340603', True), ('380685340603', True), ('+380685340603', True), ('685340603', False),
        ('+3800685340603', False),('++380685340603', False), ('+38006853406f3', False), ('+38006853406F3', False),
        ('+38006853406а3', False), ('+38006853406А3', False), ('068534060!', False), ('06853&060!', False)
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