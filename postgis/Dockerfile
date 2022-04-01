
#
# VERSION 0.2
# DOCKER-VERSION  19.03.11
# AUTHOR:         Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
# DESCRIPTION:    A postgis derived image
# TO_BUILD:       docker build --rm -t image-commondatapool_postgis .
# TO_RUN:         docker run -d -P image-commondatapool_postgis
# TO_TAG:         docker tag image-commondatapool_postgis:latest image-commondatapool_postgis:0.2
#

# FROM <image>[:<tag>|@<digest]
FROM postgis/postgis:12-3.2

# MAINTAINER is deprecated. Use LABEL instead
LABEL maintainer="paolo.cozzi@ibba.cnr.it"

# synchronize timezone for container
# https://forums.docker.com/t/synchronize-timezone-from-host-to-container/39116
RUN echo "Europe/Rome" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    unzip && \
    apt-get clean && \
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/*

# using the base ENV and CMD from base image
