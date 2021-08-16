
class ErrorMessages:

    @staticmethod
    def status_code_error(exp, act):
        return f'Wrong status code. Expected result is {exp}. Actual result is{act}'

    @staticmethod
    def success_message_error(exp, act):
        return f'Wrong success result. Expected result is {exp}. Actual result is: {act}'

    @staticmethod
    def count_order_error(exp, act):
        return f'Wrong order count in DB, expected result is: {exp} but actual result is: {act}'
