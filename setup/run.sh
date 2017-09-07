#!/bin/sh
# Main entrypoint for the notary client container.

# Check to see if setup has run and if it has enter the shell
if [ ! -f /setup/.done ]; then
  python3 /setup
else
  echo "For detailed information on how to use this container please read the /setup/README file."
  /bin/sh
fi
