import json
import requests
import getpass
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class GetToken:
    '''Request and authentication token from a UCP controller'''

    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password

        # Hide the insecure request warning message
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        # Define the credentials that will be used to access the UCP and request a token
        ucpcreds = '{"username":"' + self.user + '","password":"' + self.password + '"}'
        tokenrequest = requests.post('https://' + self.url + '/auth/login', data=ucpcreds, verify=False)
        tokendata = json.loads(tokenrequest.content)
        self.data = tokendata["auth_token"]


if __name__ == '__main__':
    UCP_URL = input("Enter the FQDN of your UCP (i.e. ucp.myorg.net):  ")
    UCP_PORT = input("Enter the port of your UCP (Optional, default is 443:  ") or 443
    USERNAME = input("Enter your UCP username:  ")
    PASSWORD = getpass.getpass('Enter your UCP password:  ')
    token = GetToken(UCP_URL, USERNAME, PASSWORD)
    print(token.data)
