
class ErrorMessages:

    @staticmethod
    def status_code_error(exp, act):
        return f'Wrong status code. Expected result is {exp}. Actual result is {act}'

    @staticmethod
    def succ_mess_error(exp, act):
        return f'Wrong success result. Expected result is {exp}. Actual result is: {act}'

    @staticmethod
    def count_order_error(exp, act):
        return f'Wrong order count in DB, expected result is: {exp} but actual result is: {act}'

    @staticmethod
    def get_response_error(response: dict):
        try:
            return f'Response error {response["errors"]}'
        except KeyError:
            return 'There are not errors in response'

    @staticmethod
    def check_param_error(ex_res, result):
        return f'Expected result is {ex_res}. Actual resutl is {result}'

    @staticmethod
    def check_param_is_present(name):
        return f'Param {name} is not present in response'
