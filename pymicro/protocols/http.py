from flask import Flask, jsonify, request
import umsgpack
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
        return umsgpack.unpackb(requests.post(
            url,
            data=umsgpack.packb(kwargs),
            headers={'Content-Type': 'application/octet-stream'}
        ).content)

    def request_args(self, endpoint):
        return umsgpack.unpackb(request.data)

    def process_response(self, payload):
        return umsgpack.packb(payload)

    def run(self):
        self.app.run(
            host=self.host,
            port=self.port
        )

    def close(self):
        pass
