# notary_container
<<<<<<< HEAD
Docker Notary Container Build Script

This image can be used to assist developers and operators with setting up their local environment to digitally sign docker images. Please note that this image uses the latest edge release of Docker-in-Docker

To setup and run this image use the following command:
docker run -it --privileged -v /var/run/docker.sock:/var/run/docker.sock gremlin961/notary-container

You can access this image on Docker Hub at the following location:
https://hub.docker.com/r/gremlin961/notary-container/

You can manually build the image by cloning this repo and issuing the following build command:
docker build -t notary-container:latest .
=======
Docker Notary Container Build Instructions
>>>>>>> 0d2b24ad708dc53f66d188bc0df5182e3275b194
