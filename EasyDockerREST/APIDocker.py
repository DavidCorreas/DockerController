import docker
from flask import Flask, jsonify, request
import json

client = docker.from_env()


app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/build', methods=['POST'])
def build():
    if request.method == 'POST':
        decoded_data = request.data.decode('utf-8')
        params = json.loads(decoded_data)
        with open("tmp-dockerfile", "rw") as file:
            file.write(params["dockerfile"])

        client.images.build("tmp-dockerfile")

        return jsonify({'PRUEBA NOMBER': params['name'], 'PRUEBA ARRS': params['tag']})


@app.route('/tag', methods=['GET'])
def tag():
    if request.method == 'POST':
        decoded_data = request.data.decode('utf-8')
        params = json.loads(decoded_data)

        client.images.tag("localhost:5000/" + params['name'], params['tag'])

        return jsonify({'PRUEBA NOMBER': params['name'], 'PRUEBA ARRS': params['tag']})


@app.route('/push', methods=['GET'])
def push():
    if request.method == 'POST':
        decoded_data = request.data.decode('utf-8')
        params = json.loads(decoded_data)

        client.images.push("localhost:5000/" + params['name'], params['tag'])

        return jsonify({'PRUEBA NOMBER': params['name'], 'PRUEBA ARRS': params['tag']})


@app.route('/pull', methods=['POST'])
def pull():
    if request.method == 'POST':
        decoded_data = request.data.decode('utf-8')
        params = json.loads(decoded_data)

        client.images.pull(params['name'], params['tag'])

        return jsonify({'PRUEBA NOMBER': params['name'], 'PRUEBA ARRS': params['tag']})


app.run(host='0.0.0.0')
