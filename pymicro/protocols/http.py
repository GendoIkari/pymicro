from flask import Flask, jsonify, request
import requests

class HTTP:
    def __init__(self, host=None, port=None, ssl=False):
        self.host = host
        self.port = port
        self.ssl = ssl

    def setup_serve(self, endpoints):
        self.app = Flask(__name__)
        for endpoint in endpoints:
            self.app.add_url_rule(**self.create_rule(endpoint))

    def create_rule(self, endpoint):
        return {
            'endpoint': endpoint.name,
            'rule': '/' + endpoint.name,
            'view_func': endpoint,
            'methods': ['POST'],
        }

    def request(self, endpoint, **kwargs):
        schema = 'https' if self.ssl else 'http'
        address = self.host + ':' + str(self.port)
        url = '{}://{}/{}'.format(schema, address, endpoint)
        return requests.post(url, json=kwargs).json()

    def process_request(self, endpoint):
        return request.get_json()

    def process_response(self, payload):
        return jsonify(payload)

    def run(self):
        self.app.run(
            host=self.host,
            port=self.port
        )