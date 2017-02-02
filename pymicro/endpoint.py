import inspect

class EndPoint:
    def __init__(self, protocol, function):
        self.protocol = protocol
        self.function = function
        self.name = function.__name__
        self.args = inspect.getargspec(function)[0]

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)
