from flask import Flask, jsonify, request

class HTTP:
    def __init__(self, host=None, port=None):
        self.host = host
        self.port = port
        self.app = Flask(__name__)

    def setup(self, endpoints):
        for endpoint in endpoints:
            self.app.add_url_rule(**self.create_rule(endpoint))

    def create_rule(self, endpoint):
        return {
            'endpoint': endpoint.name,
            'rule': '/' + endpoint.name,
            'view_func': endpoint,
            'methods': ['POST'],
        }

    def process_request(self, endpoint):
        return request.get_json()

    def process_response(self, payload):
        return jsonify(payload)

    def run(self):
        self.app.run(
            host=self.host,
            port=self.port
        )
