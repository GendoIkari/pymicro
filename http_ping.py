from pymicro.services import Service, RemoteService
from pymicro.protocols.http import HTTP
import datetime

Service.setup(
    name='ping',
    protocol=HTTP(port=5000)
)

@Service.endpoint
def ping(delay):
    pong = RemoteService(
        protocol=HTTP(host='localhost', port=5001)
    )

    now = datetime.datetime.now()
    then = pong.pong(delay=delay)['time']

    return {
        'now': now,
        'then': then,
    }

if __name__ == '__main__':
    Service.run()
