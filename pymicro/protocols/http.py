from flask import Flask, jsonify, request
from pymicro.message import Message
import requests

class HTTP:
    def __init__(self, host=None, port=None, ssl=False, secret=None):
        self.host = host
        self.port = port
        self.ssl = ssl
        self.secret = secret

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
        message = Message.pack(kwargs, self.secret)
        return Message.unpack(requests.post(
            url,
            data=message,
            headers={'Content-Type': 'application/octet-stream'}
        ).content, self.secret)

    def request_args(self, endpoint):
        return Message.unpack(request.data, self.secret)

    def process_response(self, payload):
        return Message.pack(payload, self.secret)

    def run(self):
        self.app.run(
            host=self.host,
            port=self.port
        )

    def close(self):
        pass
