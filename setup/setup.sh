#!/bin/sh

# Prompt for the username, password, UCP_URL and DTR_URL
read -p "Enter the FQDN of your UCP (i.e. ucp.myorg.net): " UCP_URL
read -p "Enter the FQDN of your DTR (i.e. dtr.myorg.net): " DTR_URL
read -p "Enter your username: " USERNAME
read -s -p "Enter your password: " PASSWORD

# Begin container customization
echo "Starting container customization"

# Get access token to the UCP and generate/download the client bundle
AUTHTOKEN=$(curl -sk -d '{"username":"'$USERNAME'","password":"'$PASSWORD'"}' https://$UCP_URL/auth/login | jq -r .auth_token)
echo AUTHTOKEN=$(curl -sk -d '{"username":"'$USERNAME'","password":"'$PASSWORD'"}' https://$UCP_URL/auth/login | jq -r .auth_token)
curl -k -H "Authorization: Bearer $AUTHTOKEN" https://$UCP_URL/api/clientbundle -o bundle.zip
echo curl -k -H "Authorization: Bearer $AUTHTOKEN" https://$UCP_URL/api/clientbundle -o bundle.zip

# Extract the client bundle to the local /bundle directory
unzip bundle.zip -d /bundle/

# When using self signed certs, get the DTR and UCP certificates and save them to /certs directory
mkdir -p /certs
echo -n | openssl s_client -connect $DTR_URL:443 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > /certs/dtr-ca.pem
echo -n | openssl s_client -connect $UCP_URL:443 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > /certs/ucp-ca.pem

# Copy the self signed certs and add them to the local trust
cp /certs/* /usr/local/share/ca-certificates/
update-ca-certificates

# Create the config.json file to configure the notary client
cat <<EOT >  ~/.notary/config.json
{
  "trust_dir" : "~/.docker/trust",
  "remote_server": {
    "url": "https://$DTR_URL",
    "root_ca": "/certs/dtr-ca.pem"
  }
}
EOT

# Get the name of the running docker container and remove the leading "/"
SYSNAME="$(docker inspect -f '{{.Name}}' $HOSTNAME | awk '{print substr($1,2); }')"

# Update the README file with the correct container name and DTR url
sed -i -e 's/SYSNAME/'$SYSNAME'/g' /setup/README
sed -i -e 's/DTR_URL/'$DTR_URL'/g' /setup/README

# Display the completion message
echo "Setup is complete. Please review /setup/README for more information and to learn how to get started using the notary client."
echo "You can launch your notary client by using:"
echo "docker start -i" $SYSNAME

# Complete the customization and create the /setup/.done file used by /setup/run.sh entrypoint script to detmine if the setup comppleted successfully.
touch /setup/.done
