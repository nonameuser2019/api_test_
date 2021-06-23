import pytest


class ClientRegistration:
    register = 'https://api.platform.masterservice.company/api/v1/customer/register'
    name_list = [('Александр', True), ('Марк-Эдгар', True), ('Mark-Edgar', True), pytest.param('', True, marks=pytest.mark.xfail),
                 pytest.param('Al', True, marks=pytest.mark.xfail), pytest.param('Alex1', True, marks=pytest.mark.xfail),
                 pytest.param('   ', True, marks=pytest.mark.xfail), pytest.param('Alex+!', True, marks=pytest.mark.xfail)]
    phone_list = [
        ('0685340603', True), ('30685340603', True), ('380685340603', True), ('+380685340603', True), ('685340603', False),
        ('+3800685340603', False),('++380685340603', False), ('+38006853406f3', False), ('+38006853406F3', False),
        ('+38006853406а3', False), ('+38006853406А3', False), ('068534060!', False), ('06853&060!', False)
    ]