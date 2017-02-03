from pymicro.services import Service
from pymicro.protocols.rabbitmq import RabbitMQ
import time
import datetime

service = Service(
    name='pong',
    protocol=RabbitMQ(url='amqp://kpoqhwjx:zvPltTNyxErzdnsxGMMYyGe0EerdNcGC@antelope.rmq.cloudamqp.com/kpoqhwjx'),
)

@service.endpoint
def pong(delay):
    time.sleep(delay)
    return {
        'time': datetime.datetime.now().isoformat(),
    }

if __name__ == '__main__':
    service.run()
