import subprocess
import json

from docker.errors import APIError
from flask import Flask, request, Response, jsonify
from DockerHandler import DockerHandler

app = Flask(__name__)
app.config["DEBUG"] = True
docker = DockerHandler()


@app.route('/build', methods=['POST'])
def build():
    if request.method == 'POST':
        decoded_data = request.data.decode('utf-8')
        params = json.loads(decoded_data)
        if "tag" not in params or "dockerfile" not in params:
            return "Bad api request: Not tag or dockerfile found", 400
        try:
            image, logs = docker.build(params["tag"], params["dockerfile"])
            return Response(logs, mimetype='application/json')
        except APIError as e:
            return "Bad api request:\n" + str(e), 400


@app.route('/tag', methods=['POST'])
def tag():
    if request.method == 'POST':
        decoded_data = request.data.decode('utf-8')
        params = json.loads(decoded_data)

        docker.tag(params['name'], params['tag'])

        return jsonify({'Nombre': params['name'], 'Tag': params['tag']})


# @app.route('/push', methods=['POST'])
# def push():
#     if request.method == 'POST':
#         decoded_data = request.data.decode('utf-8')
#         params = json.loads(decoded_data)
#
#         client.images.push("localhost:5000/" + params['name'], params['tag'])
#
#         return jsonify({'PRUEBA NOMBER': params['name'], 'PRUEBA ARRS': params['tag']})
#
#
# @app.route('/check-compose', methods=['POST'])
# def check_compose():
#     if request.method == 'POST':
#         decoded_data = request.data.decode('utf-8')
#         params = json.loads(decoded_data)
#
#         f = tempfile.NamedTemporaryFile()
#         f.write(params['docker-composeFile'])
#         with subprocess.Popen(["docker-compose"], stdout=subprocess.PIPE) as proc:
#             print(jsonify({'PRUEBA': proc.stdout.read(), 'PRUEBA ARRS': "params['tag']"}))


Flask.run(app, host='0.0.0.0', port=9090)
