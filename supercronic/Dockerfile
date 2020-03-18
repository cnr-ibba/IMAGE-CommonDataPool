
#
# VERSION 0.2
# DOCKER-VERSION  19.03.6
# AUTHOR:         Paolo Cozzi <paolo.cozzi@ibba.cnr.it>
# DESCRIPTION:    A supercronic container to execute cron stuff
#
FROM python:3.8

# MAINTAINER is deprecated. Use LABEL instead
LABEL maintainer="paolo.cozzi@ibba.cnr.it"

# install supercronic v0.1.9
# https://github.com/aptible/supercronic/
ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.1.9/supercronic-linux-amd64 \
    SUPERCRONIC=supercronic-linux-amd64 \
    SUPERCRONIC_SHA1SUM=5ddf8ea26b56d4a7ff6faecdd8966610d5cb9d85

RUN curl -fsSLO "$SUPERCRONIC_URL" \
 && echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
 && chmod +x "$SUPERCRONIC" \
 && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
 && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic

# create directory recursively
RUN mkdir -p /code/scripts/
RUN mkdir -p /code/data/

# set working dir
WORKDIR /code/data

# install required packages
COPY ./requirements.txt /code
RUN pip install -r /code/requirements.txt

# define a volume in which I could find scripts
VOLUME /code/scripts/

# install import-scripts jobs
COPY data-import-scripts /etc/cron.d/data-import-scripts

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/data-import-scripts

# execute cron job
CMD ["supercronic", "/etc/cron.d/data-import-scripts"]
