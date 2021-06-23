import pytest


class ClientRegistration:
    register = 'https://api.platform.masterservice.company/api/v1/customer/register'
    name_list = [('Александр', True), ('Марк-Эдгар', True), ('Mark-Edgar', True), pytest.param('', True, marks=pytest.mark.xfail),
                 pytest.param('Al', True, marks=pytest.mark.xfail), pytest.param('Alex1', True, marks=pytest.mark.xfail),
                 pytest.param('   ', True, marks=pytest.mark.xfail), pytest.param('Alex+!', True, marks=pytest.mark.xfail)]