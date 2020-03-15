import subprocess
import docker
import json
import tempfile
from flask import Flask, request, Response, stream_with_context, jsonify

client = docker.from_env()


app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/build', methods=['POST'])
def build():
    if request.method == 'POST':
        decoded_data = request.data.decode('utf-8')
        params = json.loads(decoded_data)

        with tempfile.NamedTemporaryFile(mode='rb+') as f:
            f.file.write(params["dockerfile"])
            f.file.flush()
            f.file.seek(0)
            image, logs = client.images.build(fileobj=f.file)

            def generate():
                for logline in logs:
                    yield logline["stream"]

            return Response(generate(), mimetype='text/plain')


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


@app.route('/check-compose', methods=['POST'])
def check_compose():
    if request.method == 'POST':
        decoded_data = request.data.decode('utf-8')
        params = json.loads(decoded_data)

        f = tempfile.NamedTemporaryFile()
        f.write(params['docker-composeFile'])
        with subprocess.Popen(["docker-compose"], stdout=subprocess.PIPE) as proc:
            print(jsonify({'PRUEBA': proc.stdout.read(), 'PRUEBA ARRS': "params['tag']"}))


app.run(host='0.0.0.0')
