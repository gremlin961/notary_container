import socket
import ssl
import subprocess

class GetCert:
    '''Retrieve TLS certificates from web servers. This is usefull for saving self signed certificates from non-trusted sources'''

    # Access the remote server and store the TLS public key in buffer
    def __init__(self, hostname, port, cert_file):
        self.hostname = hostname
        self.port = port
        self.cert_file = cert_file

        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_sock = context.wrap_socket(s, server_hostname=self.hostname)
        ssl_sock.connect((hostname, port))
        ssl_sock.close()

        self.cert = ssl.get_server_certificate((self.hostname, self.port))

    # Function to save the public key certificate to a file
    def saveCert(self):
        fo = open(self.cert_file, "w")
        fo.write(self.cert)
        fo.close()

    def updateTrust(self, os):
        self.os = os
        if self.os == "windows":
            subprocess.call(['certmgr.exe', '-add', self.cert_file, '-s', '-r', 'localMachine', 'root'])
        else:
            if self.os == "ubuntu":
                self.trustfile = "/etc/ssl/certs/ca-certificates.crt"
            elif self.os == "rhel":
                self.trustfile = "/etc/pki/tls/certs/ca-bundle.crt"
            else:
                pass
            fo = open(self.trustfile, "a")
            fo.write(self.cert)
            fo.close()



# Main method when executed outside of another script. Prompts the user for the FQDN, port, and output location
if __name__ == '__main__':
    SERVER_FQDN = input("Enter the FQDN of the server (i.e. www.myorg.net):  ")
    SERVER_PORT = input("Enter the port to connect to (default is 443):  ") or 443
    CERT_FILE = input("Enter the output file path and name (default is cert.pem located in the current directory):  ") or "./cert.pem"
    cert = GetCert(SERVER_FQDN, SERVER_PORT, CERT_FILE)
    cert.saveCert()
    trust = input("Would you like to trust this certificate? yes or no:  ") or "no"
    if trust == "no":
        pass
    else:
        os = input("Enter the OS type of ""windows"", ""ubuntu"", or ""rhel"":  ")
        cert.updateTrust(os)
