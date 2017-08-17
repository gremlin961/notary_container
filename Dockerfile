# This docker file will create a container using the latest Docker-in-Docker image and configure it to be a notary client
#
# When building the image, make sure to include the following arguments
# docker build --build-arg DTR_URL=fqdn.of.your.dtr -t notary:latest .
#
# To run the container, use:
# docker run -it notary:latest
#
# Created by rkiles on 05/17/2017
#

#docker build --build-arg DTR_URL=dtr.richard.dtcntr.net --build-arg UCP_URL=ucp.richard.dtcntr.net --build-arg USERNAME=admin --build-arg PASSWORD=domino14 -t test:latest .
#docker build -t test:latest .

#docker run -it --privileged -v /var/run/docker.sock:/var/run/docker.sock test:latest

FROM docker:edge-dind
MAINTAINER Richard D Kiles <richard.kiles@docker.com>
#ARG DTR_URL
#ARG UCP_URL
#ARG USERNAME
#ARG PASSWORD
WORKDIR /tmp
ADD ./setup/ /tmp/
ADD ./ucp-bundle/ /bundle/
RUN apk update && apk add ca-certificates openssl curl jq && update-ca-certificates
RUN wget https://github.com/docker/notary/releases/download/v0.4.3/notary-Linux-amd64 -O notary && chmod +x notary && mv notary /usr/bin/
RUN mkdir -p ~/.docker/trust && mkdir -p ~/.notary
RUN chmod +x /tmp/setup.sh
#RUN /bin/sh ./setup.sh && rm ./setup.sh
WORKDIR /
ENV DOCKER_CONTENT_TRUST 1
#CMD /bin/sh
CMD /tmp/setup.sh
