from flask import Flask

class HTTP:
    def __init__(self, host=None, port=None):
        self.host = host
        self.port = port
        self.app = Flask(__name__)

    def setup(self, endpoints):
        for endpoint in endpoints:
            self.app.add_url_rule(**endpoint.rule())

    def run(self):
        self.app.run(
            host=self.host,
            port=self.port
        )
