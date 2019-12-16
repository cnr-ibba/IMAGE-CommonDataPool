# IMAGE-CommonDataPool
IMAGE Common Data Pool - PostgreSQL, metadata structure and data loading scripts

# Runing app


Make migrations:

```sudo docker-compose run --rm djangoapp /bin/bash -c "./manage.py check"```

```sudo docker-compose run --rm djangoapp /bin/bash -c "./manage.py migrate"```

```sudo docker-compose run --rm djangoapp /bin/bash -c "./manage.py makemigrations"```

```sudo docker-compose run --rm djangoapp /bin/bash -c "./manage.py migrate"```

Create superuser:

```sudo docker-compose run --rm djangoapp /bin/bash -c "./manage.py createsuperuser --email {your email} --username admin"```

Start app:

```sudo docker-compose up -d```

Upload BioSamples data:

```python ./api-service/fetch_biosamples.py```

```python ./api-service/import_data.py {admin password}```

Stop app:

```docker-compose down```

 
