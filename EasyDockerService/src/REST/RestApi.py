import subprocess
import json
from flask import Flask, request, Response, jsonify
from flask_socketio import SocketIO, send, emit
from DockerHandler import DockerHandler

app = Flask(__name__)
app.config["DEBUG"] = True
socketio = SocketIO(app)
docker = DockerHandler()


@socketio.on('build')
def handle_message(dockerfile):
    print(dockerfile)
    emit("recive", dockerfile)
    send(dockerfile, )
    image, logs = docker.build(dockerfile)
    for logline in logs:
        print(logline)
        send(logline)


@app.route('/build', methods=['POST'])
def build():
    if request.method == 'POST':
        decoded_data = request.data.decode('utf-8')
        params = json.loads(decoded_data)
        image, logs = docker.build(params["dockerfile"])

        def generate():
            for logline in logs:
                yield logline["stream"]
        return Response(generate(), mimetype='text/plain')


# @app.route('/tag', methods=['POST'])
# def tag():
#     if request.method == 'POST':
#         decoded_data = request.data.decode('utf-8')
#         params = json.loads(decoded_data)
#
#         client.images.tag("localhost:5000/" + params['name'], params['tag'])
#
#         return jsonify({'PRUEBA NOMBER': params['name'], 'PRUEBA ARRS': params['tag']})
#
#
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
# @app.route('/pull', methods=['POST'])
# def pull():
#     if request.method == 'POST':
#         decoded_data = request.data.decode('utf-8')
#         params = json.loads(decoded_data)
#
#         client.images.pull(params['name'], params['tag'])
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


socketio.run(app, host='0.0.0.0', port=9090)
