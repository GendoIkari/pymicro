import pika
import uuid
import json

class RabbitMQ:
    MAGIC_RESPONSE_PARM = '_pymicro_response_queue'
    def __init__(self, url):
        parms = pika.URLParameters(url)
        self.url = url
        self.temporary_response_queue = None
        self.mq_connection = pika.BlockingConnection(parms)
        self.mq_channel = self.mq_connection.channel()

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

        self.mq_channel.basic_publish(
            exchange='',
            routing_key=endpoint,
            body=json.dumps(kwargs),
        )

        response = WaitResponse()
        self.mq_channel.basic_consume(response, queue=response_queue)
        self.mq_channel.start_consuming()
        return json.loads(response.body.decode("utf-8"))

    def process_request(self, endpoint, channel, method, properties, body):
        data = json.loads(body.decode("utf-8"))
        self.temporary_response_queue = data[RabbitMQ.MAGIC_RESPONSE_PARM]
        del data[RabbitMQ.MAGIC_RESPONSE_PARM]
        channel.basic_ack(delivery_tag=method.delivery_tag)
        return data

    def process_response(self, payload, channel, method, properties, body):
        self.mq_channel.basic_publish(
            exchange='',
            routing_key=self.temporary_response_queue,
            body=json.dumps(payload),
        )

    def run(self):
        self.mq_channel.start_consuming()

    def close(self):
        self.mq_connection.close()
