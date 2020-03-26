import docker
from REST.TCPHandler import TCPConnection
import tempfile

client = docker.from_env()

with tempfile.NamedTemporaryFile(mode='rb+') as f:
    f.file.write(b'FROM hello-world')
    f.file.flush()
    f.file.seek(0)
    image, logs = client.images.build(fileobj=f.file)

connection = TCPConnection('0.0.0.0', 9090)
for logline in logs:
    if 'stream' in logline:
        connection.send(logline["stream"].encode())
connection.close()
