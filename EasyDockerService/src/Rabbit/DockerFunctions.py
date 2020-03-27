import json

from DockerHandler import DockerHandler
from Rabbit.RabbitHandler import RabbitHandler


class DockerFunctions:
    def __init__(self):
        self.docker = DockerHandler()
        queue = "rpc_queue"
        self.connection = RabbitHandler('localhost')
        self.connection.declare_queue(queue)
        self.connection.start_consumig(queue, self.on_request)

    def build(self, channel, method, props, msg_body):
        print("build method")
        image, logs = self.docker.build(msg_body["dockerfile"])

        for logline in logs:
            self.connection.send_message(response=logline["stream"],
                                         channel=channel,
                                         routing_key=props.reply_to,
                                         correlation_id=props.correlation_id,
                                         delivery_tag=method.delivery_tag)

    def on_request(self, channel, method, props, body):
        message = json.loads(body)
        function = message["function"]
        msg_body = message["body"]

        if function == "build":
            self.build(channel, method, props, msg_body)

