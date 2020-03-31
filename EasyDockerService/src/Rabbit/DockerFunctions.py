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
        print("Build Method")
        try:
            streamer = self.docker.build(msg_body["tag"], msg_body["dockerfile"])
            print("End build")

            for logline in streamer:
                print(str(logline))
                if "stream" in logline:
                    response = {'response': logline["stream"]}
                    self.connection.send_message(response=json.dumps(response),
                                                 channel=channel,
                                                 routing_key=props.reply_to,
                                                 correlation_id=props.correlation_id)
        except APIError as e:
            error = "ERROR: DockerApi error: \n" + str(e)
            print(error)
            response = {'response': error}
            self.connection.send_message(response=json.dumps(response),
                                         channel=channel,
                                         routing_key=props.reply_to,
                                         correlation_id=props.correlation_id)

        self.connection.ack(channel, delivery_tag=method.delivery_tag)

    def tag(self, channel, method, props, msg_body):
        print("Tag Method")
        tag = msg_body["tag"] if "tag" in msg_body else None
        try:
            boolean = self.docker.tag(msg_body["img_name"], msg_body["repository"],
                                      tag)
            print("End tag")
            response = {'response': str(boolean)}
            self.connection.send_message(response=json.dumps(response),
                                         channel=channel,
                                         routing_key=props.reply_to,
                                         correlation_id=props.correlation_id)
        except APIError as e:
            error = "ERROR: DockerApi error: \n" + str(e)
            print(error)
            self.connection.send_message(response=json.dumps(error),
                                         channel=channel,
                                         routing_key=props.reply_to,
                                         correlation_id=props.correlation_id)

        self.connection.ack(channel, delivery_tag=method.delivery_tag)

    def push(self, channel, method, props, msg_body):
        print("Push Method")
        tag = msg_body["tag"] if "tag" in msg_body else None
        try:
            streamer = self.docker.push(msg_body["repository"], tag)
            print("End push")

            for logline in streamer:
                print(str(logline))
                response = {'response': logline.decode()}
                self.connection.send_message(response=json.dumps(response),
                                             channel=channel,
                                             routing_key=props.reply_to,
                                             correlation_id=props.correlation_id)
        except APIError as e:
            error = "ERROR: DockerApi error: \n" + str(e)
            print(error)
            response = {'response': error}
            self.connection.send_message(response=json.dumps(response),
                                         channel=channel,
                                         routing_key=props.reply_to,
                                         correlation_id=props.correlation_id)

        self.connection.ack(channel, delivery_tag=method.delivery_tag)

    def list(self, channel, method, props, msg_body):
        print("List Method")
        name = msg_body["name"] if "name" in msg_body else None
        all_layers = msg_body["all_layers"] if "all_layers" in msg_body else None
        filters = msg_body["filters"] if "filters" in msg_body else None
        try:
            images = self.docker.list(name, all_layers, filters)
            print("End list")

            tags_image = ""
            for image in images:
                print(str(image))
                if image.tags:
                    tags_image = tags_image + str(image.tags) + "\n"
            response = {'response': tags_image}
            self.connection.send_message(response=json.dumps(response),
                                         channel=channel,
                                         routing_key=props.reply_to,
                                         correlation_id=props.correlation_id)
        except APIError as e:
            error = "ERROR: DockerApi error: \n" + str(e)
            print(error)
            response = {'response': error}
            self.connection.send_message(response=json.dumps(response),
                                         channel=channel,
                                         routing_key=props.reply_to,
                                         correlation_id=props.correlation_id)

        self.connection.ack(channel, delivery_tag=method.delivery_tag)

    def check_compose(self, channel, method, props, msg_body):
        print("Check Method")
        try:
            log = self.docker.check_compose(msg_body["compose"])
            print("End Check")

            response = {'response': log.decode()}
            self.connection.send_message(response=json.dumps(response),
                                         channel=channel,
                                         routing_key=props.reply_to,
                                         correlation_id=props.correlation_id)
        except APIError as e:
            error = "ERROR: DockerApi error: \n" + str(e)
            print(error)
            response = {'response': error}
            self.connection.send_message(response=json.dumps(response),
                                         channel=channel,
                                         routing_key=props.reply_to,
                                         correlation_id=props.correlation_id)

        self.connection.ack(channel, delivery_tag=method.delivery_tag)

    def on_request(self, channel, method, props, body):
        message = json.loads(body)
        function = message["function"]
        msg_body = message["body"]

        if function == "build":
            self.build(channel, method, props, msg_body)
        elif function == "tag":
            self.tag(channel, method, props, msg_body)
        elif function == "push":
            self.push(channel, method, props, msg_body)
        elif function == "list":
            self.list(channel, method, props, msg_body)
        elif function == "check_compose":
            self.check_compose(channel, method, props, msg_body)


# EntryPoint
DockerFunctions()
