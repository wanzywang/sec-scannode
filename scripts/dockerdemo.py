import docker


if __name__ == "__main__":
    c = docker.DockerClient(base_url='unix:///var/run/docker.sock')
    print(c.info())

