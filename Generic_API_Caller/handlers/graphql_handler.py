import requests


class GraphQLHandler:

    @staticmethod
    def execute(endpoint, query, variables=None):

        response = requests.post(

            endpoint,

            json={
                "query": query,
                "variables": variables
            },

            timeout=30
        )

        response.raise_for_status()

        return response.json()