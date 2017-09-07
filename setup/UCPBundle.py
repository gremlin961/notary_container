import UCPToken
import requests
import zipfile
import io
import getpass


class GetBundle:
    '''Generate and download a new UCP client bundle'''

    def __init__(self, url, token):

        self.url = url
        self.token = token

        # Create a dictionary of the token data to use with the request header
        headerauth = {"Authorization":"Bearer " + self.token + ""}
        bundleurl='https://' + self.url + '/api/clientbundle'

        # Generate and download the UCP Client Bundle
        self.bundle = requests.get(bundleurl,headers=headerauth, verify=False)


    def extractBundle(self, path):

        self.path = path

        # Extract the UCP Client Bundle zip file to the defined path
        ucpzip = zipfile.ZipFile(io.BytesIO(self.bundle.content))
        ucpzip.extractall(path=self.path)

if __name__ == '__main__':
        UCP_URL = input("Enter the FQDN of your UCP (i.e. ucp.myorg.net):  ")
        UCP_PORT = input("Enter the port of your UCP (Optional, default is 443:  ") or 443
        USERNAME = input("Enter your UCP username:  ")
        PASSWORD = getpass.getpass('Enter your UCP password:  ')
        CERT_PATH = input("Enter the path to extract the client bundle to:  ")
        token = UCPToken.GetToken(UCP_URL, USERNAME, PASSWORD)
        bundle = GetBundle(UCP_URL, token.data)
        bundle.extractBundle(CERT_PATH)
