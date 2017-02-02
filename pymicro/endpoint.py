import inspect

class EndPoint:
    def __init__(self, protocol, function):
        self.protocol = protocol
        self.function = function
        self.name = function.__name__

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

    def rule(self):
        rule = '/' + '/'.join([
            self.name,
            *['<' + arg + '>' for arg in inspect.getargspec(self.function)[0]],
        ])
        return {
            'endpoint': self.name,
            'rule': rule,
            'view_func': self,
        }
