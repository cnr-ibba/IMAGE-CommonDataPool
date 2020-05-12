 FROM python:3.8

 # Install dependencies
 RUN apt-get update && apt-get install -y --no-install-recommends \
     postgresql-client && \
     apt-get clean && \
     apt-get autoclean && \
     rm -rf /var/lib/apt/lists/*

 RUN mkdir /code
 WORKDIR /code

 COPY ./requirements.txt /code
 RUN pip install -r requirements.txt

 EXPOSE 8000
 CMD ["gunicorn", "--bind", ":8000", "--access-logfile", "-", "--workers", "2", "api_service.wsgi:application"]
