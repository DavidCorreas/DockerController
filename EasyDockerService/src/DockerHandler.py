import docker
import tempfile


class DockerHandler:
    def __init__(self):
        self.client = docker.from_env()

    def build(self, dockerfile: str):
        with tempfile.NamedTemporaryFile(mode='rb+') as f:
            f.file.write(dockerfile.encode())
            f.file.flush()
            f.file.seek(0)
            return self.client.images.build(fileobj=f.file)



