from pymicro.services import Service
from pymicro.protocols.http import HTTP
import time
import datetime

Service.setup(
    name='vm-spawner',
    protocol=HTTP(port=5001),
)

@Service.endpoint
def pong(delay):
    time.sleep(delay)
    return {
        'time': datetime.datetime.now(),
    }

if __name__ == '__main__':
    Service.run()
