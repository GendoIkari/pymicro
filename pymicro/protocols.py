from flask import Flask, jsonify, request
import requests

class HTTP:
    def __init__(self, host=None, port=None):
        self.host = host
        self.port = port

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
        return requests.post('http://' + self.host + ':' + str(self.port) + '/' + endpoint, json=kwargs).json()

    def process_request(self, endpoint):
        return request.get_json()

    def process_response(self, payload):
        return jsonify(payload)

    def run(self):
        self.app.run(
            host=self.host,
            port=self.port
        )
