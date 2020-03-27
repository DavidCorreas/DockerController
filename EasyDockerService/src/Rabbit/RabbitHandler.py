import pika


class RabbitHandler:
    def __init__(self, host):
        credentials = pika.PlainCredentials('rabbituser', '1234')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, credentials=credentials,
                                      connection_attempts=5, retry_delay=5.0))
        self.channel = connection.channel()

    def declare_queue(self, name):
        self.channel.queue_declare(name)

    def start_consumig(self, queue, on_message_callback):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queue, on_message_callback=on_message_callback)
        print(" [x] Awaiting RPC requests")
        self.channel.start_consuming()

    def send_message(self, response, routing_key, correlation_id, delivery_tag):
        self.channel.basic_publish(exchange='',
                                   routing_key=routing_key,
                                   properties=pika.BasicProperties(correlation_id=correlation_id),
                                   body=response)

        self.channel.basic_ack(delivery_tag=delivery_tag)

