FROM python:3

RUN apt-get update && apt-get -y install cron

RUN mkdir /code
WORKDIR /code

COPY ./requirements.txt /code
RUN pip install -r requirements.txt

COPY ./get_all_etags.py /code
COPY ./fetch_biosamples.py /code
COPY ./import_data.py /code
COPY ./import_files.py /code
COPY data-import-scripts /etc/cron.d/data-import-scripts

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/data-import-scripts

# Apply cron job
RUN crontab /etc/cron.d/data-import-scripts

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log