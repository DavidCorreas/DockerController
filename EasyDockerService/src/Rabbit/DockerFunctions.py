import json

from docker.errors import APIError

from DockerHandler import DockerHandler
from RabbitHandler import RabbitHandler


class DockerFunctions:
    def __init__(self):
        self.docker = DockerHandler()
        queue = "app.docker.request"
        self.connection = RabbitHandler('rabbitmq')
        self.connection.declare_queue(queue)
        self.connection.start_consumig(queue, self.on_request)

    def build(self, channel, method, props, msg_body):
        print("build method")
        try:
            streamer = self.docker.build(msg_body["tag"], msg_body["dockerfile"])
            print("end build")

            for logline in streamer:
                print(str(logline))
                if "stream" in logline:
                    response = {'response': logline["stream"]}
                    self.connection.send_message(response=json.dumps(response),
                                                 channel=channel,
                                                 routing_key=props.reply_to,
                                                 correlation_id=props.correlation_id)
        except APIError as e:
            print("error de api:" + str(e))
        self.connection.ack(channel, delivery_tag=method.delivery_tag)

    def on_request(self, channel, method, props, body):
        message = json.loads(body)
        function = message["function"]
        msg_body = message["body"]

        if function == "build":
            self.build(channel, method, props, msg_body)


# EntryPoint
DockerFunctions()
