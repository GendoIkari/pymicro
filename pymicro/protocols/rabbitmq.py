import pika
import uuid
import json

class RabbitMQ:
    def __init__(self, url):
        parms = pika.URLParameters(url)
        self.url = url
        self.uuid = uuid.uuid4()
        self.temporary_response_queue = None
        self.mq_connection = pika.BlockingConnection(parms)
        self.mq_channel = self.mq_connection.channel()

    def setup_serve(self, endpoints):
        for endpoint in endpoints:
            self.mq_channel.queue_declare(queue=endpoint.name)
            self.mq_channel.basic_consume(endpoint, queue=endpoint.name)

    def response_queue(self, endpoint_name):
        return '{}-{}'.format(endpoint_name, self.uuid)

    def request(self, endpoint, **kwargs):
        class WaitResponse:
            def __call__(self, channel, method, properties, body):
                self.body = body
                channel.stop_consuming()
                channel.queue_delete(queue=method.routing_key)
                channel.basic_ack(delivery_tag=method.delivery_tag)

        self.mq_channel.queue_declare(queue=endpoint)
        self.mq_channel.queue_declare(queue=self.response_queue(endpoint))
        kwargs['_pymicro_response_queue'] = self.response_queue(endpoint)

        self.mq_channel.basic_publish(
            exchange='',
            routing_key=endpoint,
            body=json.dumps(kwargs),
        )

        response = WaitResponse()
        self.mq_channel.basic_consume(response, queue=self.response_queue(endpoint))
        self.mq_channel.start_consuming()
        return json.loads(response.body.decode("utf-8"))

    def process_request(self, endpoint, channel, method, properties, body):
        data = json.loads(body.decode("utf-8"))
        self.temporary_response_queue = data['_pymicro_response_queue']
        del data['_pymicro_response_queue']
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
