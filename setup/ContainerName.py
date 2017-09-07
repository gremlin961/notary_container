import json
import socket
import docker

def getName():
    # Get the container hostname
    hostname = socket.gethostname()

    # Connect to the local docker API and collect the json data for the running container
    localengine = docker.APIClient(base_url='unix://var/run/docker.sock')
    dockerinfo = localengine.inspect_container(hostname)

    # Parse the json data and get the name of the container, removing the " and / characters
    myname_raw = json.dumps(dockerinfo['Name'])
    myname = myname_raw.translate({ord(i): None for i in '"/'})
    return myname


if __name__ == '__main__':
    print(getName())
