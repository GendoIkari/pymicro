import json
import inspect

def serializable(self, obj):
    try:
        json.dumps(obj)
        return True
    except TypeError:
        return False

class EndPoint:
    def __init__(self, protocol, function):
        self.protocol = protocol
        self.function = function
        self.name = function.__name__
        self.args = inspect.getargspec(function)[0]

    def __call__(self, *args, **kwargs):
        request_args = self.protocol.request_args(self, *args, **kwargs)
        response_args = self.function(**request_args)
        assert serializable(response_args, 'An endpoint must return a serializable object')

        return self.protocol.process_response(response_args, *args, **kwargs)
