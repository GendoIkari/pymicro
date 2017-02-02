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
        Service.protocol.setup_serve(Service.endpoints)
        Service.protocol.run()

    @staticmethod
    def endpoint(f):
        endpoint = EndPoint(Service.protocol, f)
        Service.endpoints.append(endpoint)
        return endpoint

class RemoteService:
    class RequestedFunction:
        def __init__(self, endpoint, protocol):
            self.endpoint = endpoint
            self.protocol = protocol

        def __call__(self, **kwargs):
            return self.protocol.request(self.endpoint, **kwargs)

    def __init__(self, protocol):
        self.protocol = protocol

    def __getattr__(self, function):
        return RemoteService.RequestedFunction(function, self.protocol)
