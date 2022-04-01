
#
# VERSION 0.2
# DOCKER-VERSION  20.10.14
# AUTHOR:         Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
# DESCRIPTION:    A postgis derived image
# TO_BUILD:       docker build --rm -t image-commondatapool_djangoapp .
# TO_RUN:         docker run -d -P image-commondatapool_djangoapp
# TO_TAG:         docker tag image-commondatapool_djangoapp:latest image-commondatapool_djangoapp:0.2
#

# FROM <image>[:<tag>|@<digest]
FROM python:3.8

# The mainteiner of this image
LABEL maintainer="Paolo Cozzi <paolo.cozzi@ibba.cnr.it"

# synchronize timezone for container
# https://forums.docker.com/t/synchronize-timezone-from-host-to-container/39116
RUN echo "Europe/Rome" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

# install postgres 12 client libraries on debian
# https://computingforgeeks.com/install-postgresql-12-on-debian/
RUN apt-get update && apt-get install -y gnupg2 && \
  wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
  echo "deb http://apt.postgresql.org/pub/repos/apt/ buster-pgdg main" | tee  /etc/apt/sources.list.d/pgdg.list

# add PostgreSQL repository
RUN curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | \
    gpg --dearmor -o /usr/share/keyrings/postgresql-keyring.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/postgresql-keyring.gpg] http://apt.postgresql.org/pub/repos/apt/ bullseye-pgdg main" | \
    tee /etc/apt/sources.list.d/postgresql.list

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    binutils \
    libproj-dev \
    gdal-bin && \
    apt-get clean && \
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /code
WORKDIR /code

COPY ./requirements.txt /root/
RUN pip install -r /root/requirements.txt

EXPOSE 8000
CMD ["gunicorn", "--bind", ":8000", "--access-logfile", "-", "--workers", "2", "api_service.wsgi:application"]
