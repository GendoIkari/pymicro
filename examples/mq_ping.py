from pymicro.services import Service, RemoteService
from pymicro.protocols.http import HTTP
from pymicro.protocols.rabbitmq import RabbitMQ
import datetime

service = Service(
    name='ping',
    protocol=HTTP(port=5000)
)

@service.endpoint
def ping(delay):
    pong = RemoteService(
        protocol=RabbitMQ(
            url='amqp://',
            secret='123',
        ),
    )

    now = datetime.datetime.now().isoformat()
    then = pong.pong(delay=delay)['time']

    return {
        'now': now,
        'then': then,
    }

if __name__ == '__main__':
    service.run()
