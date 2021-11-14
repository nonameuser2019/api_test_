class AllureStep:

    @staticmethod
    def check_status_code(status_code):
        return f'Check status code, expected status code is {status_code}'

    @staticmethod
    def check_success_message(message):
        return f'Check success param in response, expected result is {message}'
