import requests

class HttpManager:
    #headers = {'Content-Type': 'application/json'}

    @staticmethod
    def get(url, headers):
        result = requests.get(url,
                              headers=headers)
        return result

    @staticmethod
    def post(url, body, headers):
        result = requests.post(url,
                               json=body,
                               headers=headers)
        return result

