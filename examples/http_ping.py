from pymicro.services import Service, RemoteService
from pymicro.protocols.http import HTTP
import datetime

service = Service(
    name='ping',
    protocol=HTTP(port=5000)
)

@service.endpoint
def ping(delay):
    pong = RemoteService(
        protocol=HTTP(host='localhost', port=5001)
    )

    now = datetime.datetime.now().isoformat()
    then = pong.pong(delay=delay)['time']

    return {
        'now': now,
        'then': then,
    }

if __name__ == '__main__':
    service.run()
