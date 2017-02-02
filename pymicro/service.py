class EndPoint:
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        print('endpoint')
        return self.function(*args, **kwargs)

class Service:
    name = ''
    protocol = None
    endpoints = []

    @staticmethod
    def setup(**config):
        assert 'name' in config, '"name" key is mandatory to setup Service'
        assert 'protocol' in config, '"protocol" key is mandatory to setup Service'
        Service.name = config['name']
        Service.protocol = config['protocol']()

    @staticmethod
    def run():
        Service.protocol.setup(Service.endpoints)
        Service.protocol.run()

    @staticmethod
    def endpoint(f):
        endpoint = EndPoint(f)
        Service.endpoints.append(endpoint)
        return endpoint
