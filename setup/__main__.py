# Import needed python modules
import getpass
#import requests
import json
#import zipfile
#import io
#import urllib
import UCPCert
import UCPToken
import UCPBundle
import os
import pathlib
import subprocess
import socket
from ContainerName import getName
import fileinput

def updateReadme(readmefile, old, new):
    readmefile = readmefile
    old = old
    new = new
    for word in fileinput.input([readmefile], inplace=True):
        print(word.replace(old, new), end='')



if __name__=='__main__':

    # Prompt for the username, password, UCP_URL and DTR_URL
    UCP_URL = input("Enter the FQDN of your UCP (i.e. ucp.myorg.net):  ")
    UCP_PORT = input("Enter the port of your UCP (Optional, default is 443):  ") or 443
    DTR_URL = input("Enter the port of your DTR (i.e. dtr.myorg.net):  ")
    DTR_PORT = input("Enter the FQDN of your DTR (Optional, default is 443):  ") or 443
    USERNAME = input("Enter your UCP username:  ")
    PASSWORD = getpass.getpass('Enter your UCP password:  ')
    print("")

    # Begin container customization
    print("Starting container customization")

    # Get access token to the UCP and generate/download the client bundle
    print("Downloading UCP Client Bundle for " + USERNAME)

    # Define the path to extract the client bundle to
    CERT_PATH = "/bundle/"

    # Request the UCP Auth token using the UCPToken module
    token = UCPToken.GetToken(UCP_URL, USERNAME, PASSWORD)
    # Download and extract the UCP Client Bundle
    bundle = UCPBundle.GetBundle(UCP_URL, token.data)
    bundle.extractBundle(CERT_PATH)


    print("Adding TLS certificates for UCP and DTR to the trusted store")
    # When using self signed certs, get the DTR and UCP certificates and save them to /certs directory

    # Get the UCP certifcate
    ucpcert = UCPCert.GetCert(UCP_URL, UCP_PORT, "/certs/ucp-ca.pem")
    ucpcert.saveCert()
    ucpcert.updateTrust("ubuntu")

    # Get the DTR certifcate
    dtrcert = UCPCert.GetCert(DTR_URL, DTR_PORT, "/certs/dtr-ca.pem")
    dtrcert.saveCert()
    dtrcert.updateTrust("ubuntu")


    print("Updating the Notary configuration file")
    # Read the content of notry_config.json template and replace the remote server url with the correct DTR url
    with open("/setup/notary_config.json", "r") as data_file:
        json_data = json.load(data_file)
        json_data["remote_server"]["url"] = 'https://' + DTR_URL

    # Create the .notary hidden directory in the user's home dir and write the config.json file
    home = str(pathlib.Path.home())
    if not os.path.exists(home + "/.notary"):
        os.makedirs(home + "/.notary")
    with open(home + "/.notary/config.json", "w") as notary_config:
        json.dump(json_data, notary_config)
        notary_config.close


    print("Generating User Documents")
    # Get the name of the running docker container and update the README
    container = getName()
    updateReadme("/setup/README", "SYSNAME", container)
    updateReadme("/setup/README", "DTR_URL", DTR_URL)

    print("")
    print("")
    print("Setup is complete. Please review /setup/README for more information and to learn how to get started using the notary client.")
    print("You can launch your notary client by using:")
    print("docker start -i " + container)

    # Write the completion file
    open("/setup/.done", "w+").close()
