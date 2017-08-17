#!/bin/sh
# Main entrypoint for the notary client container.

# Check to see if setup has run and if it has enter the shell
if [ ! -f /setup/.done ]; then
  /setup/setup.sh
else
  /bin/sh
fi
