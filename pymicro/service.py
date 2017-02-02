from pymicro.endpoint import EndPoint

class Service:
    name = ''
    protocol = None
    endpoints = []

    @staticmethod
    def setup(name, protocol):
        Service.name = name
        Service.protocol = protocol

    @staticmethod
    def run():
        Service.protocol.setup(Service.endpoints)
        Service.protocol.run()

    @staticmethod
    def endpoint(f):
        endpoint = EndPoint(Service.protocol, f)
        Service.endpoints.append(endpoint)
        return endpoint
