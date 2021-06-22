import requests

class HttpManager:
    headers = {'Content-Type': 'application/json'}

    @staticmethod
    def get(url):
        result = requests.get(url,
                              headers=HttpManager.headers)
        return result

    @staticmethod
    def post(url, body):
        result = requests.post(url,
                               json=body,
                               headers=HttpManager.headers)
        return result
