import json

from docker.errors import APIError

from DockerHandler import DockerHandler
from RabbitHandler import RabbitHandler


class DockerFunctions:
    def __init__(self):
        self.docker = DockerHandler()
        queue = "app.docker.request"
        self.connection = RabbitHandler('localhost')
        self.connection.declare_queue(queue)
        self.connection.start_consumig(queue, self.on_request)

    def build(self, channel, method, props, msg_body):
        print("build method")
        # try:
        image, logs = self.docker.build(msg_body["dockerfile"])

        for logline in logs:
            print(str(logline))
            if "stream" in logline:
                response = {'response': logline["stream"]}
                self.connection.send_message(response=json.dumps(response),
                                             channel=channel,
                                             routing_key=props.reply_to,
                                             correlation_id=props.correlation_id)
        # except APIError:
        #     print("error de api")
        self.connection.ack(channel, delivery_tag=method.delivery_tag)

    def on_request(self, channel, method, props, body):
        message = json.loads(body)
        function = message["function"]
        msg_body = message["body"]

        if function == "build":
            self.build(channel, method, props, msg_body)


# EntryPoint
DockerFunctions()
