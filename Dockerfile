# This docker file will create a container using the latest Docker-in-Docker image and configure it to be a notary client
#
# To run the container, use:
# docker run -it --privileged -v /var/run/docker.sock:/var/run/docker.sock notary:latest
#
# Created by rkiles on 08/17/2017


FROM docker:edge-dind
MAINTAINER Richard D Kiles <richard.kiles@docker.com>
WORKDIR /tmp
ADD ./setup/ /setup/
ADD ./ucp-bundle/ /bundle/
RUN apk update && apk add ca-certificates openssl curl jq && update-ca-certificates
RUN wget https://github.com/docker/notary/releases/download/v0.4.3/notary-Linux-amd64 -O notary && chmod +x notary && mv notary /usr/bin/
RUN mkdir -p ~/.docker/trust && mkdir -p ~/.notary
RUN chmod +x /setup/setup.sh && chmod +x /setup/run.sh
WORKDIR /
ENV DOCKER_CONTENT_TRUST 1
CMD /setup/run.sh
