from pymicro.services import Service
from pymicro.protocols.http import HTTP
import time
import datetime

service = Service(
    name='pong',
    protocol=HTTP(port=5001),
)

@service.endpoint
def pong(delay):
    time.sleep(delay)
    return {
        'time': datetime.datetime.now(),
    }

if __name__ == '__main__':
    service.run()
