import subprocess

import docker
import tempfile


class DockerHandler:
    def __init__(self):
        self.client = docker.from_env()
        self.buildclient = docker.APIClient(base_url='unix://var/run/docker.sock')

    def build(self, tag, dockerfile: str):
        """
        Build a image from a dockerfile type string and tag it with tag.
        :param tag: Name for the image.
        :param dockerfile: String that contains the dockerfile. Example: FROM hello-world
        :return: Generator with de build log in real time. JSON format.
        """
        with tempfile.NamedTemporaryFile(mode='rb+') as f:
            f.file.write(dockerfile.encode())
            f.file.flush()
            f.file.seek(0)
            return self.buildclient.build(decode=True, fileobj=f.file, tag=tag)

    def tag(self, img_name, repository, tag=None):
        """
        Tag a image identify with img_name with repository and tag.
        :param img_name: Image to tag
        :param repository: Name of repo. Example: localhost:5000/test
        :param tag: (Optional). Tag of the image.
        :return: Bool, true if tagged.
        """
        return self.client.images.get(img_name)\
            .tag(repository, tag)

    def push(self, repository, tag=None):
        """
        Push image to registry or dockerhub.
        :param repository: Repository to push. This has to be locally in this instance.
        :param tag: Tag to push. This has to be locally in this instance.
        :return: Generator of logs of the remote.
        """
        return self.client.images.push(repository, tag=tag, stream=True)

    def list(self, name=None, all_layers=False, filters=None):
        """
        List existing images in instance.
        :param name: Only show images belonging to the repository name
        :param all_layers: Show intermediate image layers. By default, these are filtered out.
        :param filters: Filters to be processed on the image list. Available filters: -
        dangling (bool) - label (str|list): format either "key", "key=value"
        :return: List of Image
        """
        return self.client.images.list(name=name, all=all_layers, filters=filters)

    @staticmethod
    def check_compose(compose):
        with tempfile.NamedTemporaryFile(mode='rb+') as f:
            f.file.write(compose.encode())
            f.file.flush()
            f.file.seek(0)
            with subprocess.Popen(["docker-compose", "-f", f.name, "config"], stdout=subprocess.PIPE) as proc:
                print(proc.stdout.read())
