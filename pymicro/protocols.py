from flask import Flask, jsonify

class HTTP:
    def __init__(self, host=None, port=None):
        self.host = host
        self.port = port
        self.app = Flask(__name__)

    def setup(self, endpoints):
        for endpoint in endpoints:
            self.app.add_url_rule(**self.create_rule(endpoint))

    def create_rule(self, endpoint):
        rule = '/' + '/'.join([
            endpoint.name,
            *['<' + arg + '>' for arg in endpoint.args],
        ])
        return {
            'endpoint': endpoint.name,
            'rule': rule,
            'view_func': endpoint,
        }

    def process_response(self, payload):
        return jsonify(payload)

    def run(self):
        self.app.run(
            host=self.host,
            port=self.port
        )
