import pika
import uuid
import traceback
from pymicro.message import Message

class RabbitMQ:
    MAGIC_RESPONSE_PARM = '_pymicro_response_queue'
    def __init__(self, url, secret=None):
        parms = pika.URLParameters(url)
        self.url = url
        self.temporary_response_queue = None
        self.mq_connection = pika.BlockingConnection(parms)
        self.mq_channel = self.mq_connection.channel()
        self.secret = secret

    def setup_serve(self, endpoints):
        for endpoint in endpoints:
            self.mq_channel.queue_declare(queue=endpoint.name)
            self.mq_channel.basic_consume(endpoint, queue=endpoint.name)

    def request(self, endpoint, **kwargs):
        class WaitResponse:
            def __call__(self, channel, method, properties, body):
                self.body = body
                channel.stop_consuming()
                channel.queue_delete(queue=method.routing_key)
                channel.basic_ack(delivery_tag=method.delivery_tag)

        response_queue = uuid.uuid4().hex
        kwargs[RabbitMQ.MAGIC_RESPONSE_PARM] = response_queue
        self.mq_channel.queue_declare(queue=response_queue)
        self.mq_channel.queue_declare(queue=endpoint)

        message = Message.pack(kwargs, self.secret)
        self.mq_channel.basic_publish(
            exchange='',
            routing_key=endpoint,
            body=message,
        )

        response = WaitResponse()
        self.mq_channel.basic_consume(response, queue=response_queue)
        self.mq_channel.start_consuming()
        return Message.unpack(response.body, self.secret)

    def request_args(self, endpoint, channel, method, properties, body):
        data = Message.unpack(body, self.secret)
        self.temporary_response_queue = data[RabbitMQ.MAGIC_RESPONSE_PARM]
        del data[RabbitMQ.MAGIC_RESPONSE_PARM]
        channel.basic_ack(delivery_tag=method.delivery_tag)
        return data

    def process_response(self, payload, channel, method, properties, body):
        self.mq_channel.basic_publish(
            exchange='',
            routing_key=self.temporary_response_queue,
            body=Message.pack(payload, self.secret),
        )

    def run(self):
        while 1:
            try:
                self.mq_channel.start_consuming()
            except Exception as err:
                if isinstance(err, KeyboardInterrupt):
                    raise
                traceback.print_exc()


    def close(self):
        self.mq_connection.close()
