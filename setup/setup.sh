#!/bin/sh

# Prompt for the username, password, UCP_URL and DTR_URL
echo "Enter the FQDN of your UCP (i.e. ucp.myorg.net):"
read UCP_URL
echo "Enter the FQDN of your DTR (i.e. dtr.myorg.net):"
read DTR_URL
echo "Enter your username:"
read USERNAME
echo "Enter your password:"
read -s PASSWORD

AUTHTOKEN=$(curl -sk -d '{"username":"'$USERNAME'","password":"'$PASSWORD'"}' https://$UCP_URL/auth/login | jq -r .auth_token)
curl -k -H "Authorization: Bearer $AUTHTOKEN" https://$UCP_URL/api/clientbundle -o bundle.zip
unzip bundle.zip -d /bundle/

# Get the DTR cert and save it to /certs/dtr-ca.pem
mkdir -p /certs
echo -n | openssl s_client -connect $DTR_URL:443 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > /certs/dtr-ca.pem
echo -n | openssl s_client -connect $UCP_URL:443 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > /certs/ucp-ca.pem

cp /certs/* /usr/local/share/ca-certificates/
update-ca-certificates

cat <<EOT >  ~/.notary/config.json
{
  "trust_dir" : "~/.docker/trust",
  "remote_server": {
    "url": "https://$DTR_URL",
    "root_ca": "/certs/dtr-ca.pem"
  }
}
EOT

echo "Setup is complete. Please review /setup/README for more information."
