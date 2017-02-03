from pymicro.endpoint import EndPoint

class Service:
    def __init__(self, name, protocol):
        self.name = name
        self.protocol = protocol
        self.endpoints = []

    def run(self):
        self.protocol.setup_serve(self.endpoints)
        self.protocol.run()

    def endpoint(self, f):
        endpoint = EndPoint(self.protocol, f)
        self.endpoints.append(endpoint)
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
