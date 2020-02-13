import docker
import flask

client = docker.from_env()
client.images.pull("alpine", "latest")


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    print(client.containers.run("alpine", ["echo", "hello", "world"]))
    return "hecho"


app.run(host='0.0.0.0')
