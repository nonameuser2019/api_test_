import pytest


class ClientRegistration:
    reg_endpoint = 'https://api.platform.masterservice.company/api/v1/customer/register'
    name_list = [('Александр', True), ('Марк-Эдгар', True), ('Mark-Edgar', True), ('', True), ('Al', True),
                 ('Alex1', True), ('   ', True), ('Alex+!', True)
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