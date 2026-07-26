import requests


class RestHandler:

    @staticmethod
    def execute(endpoint, method="POST", **payload):

        response = requests.request(
            method=method,
            url=endpoint,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        return response.json()