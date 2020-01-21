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

# Special notes about links to dad-is interface

Currently it seems to be impossible to generate links to dad-is automatically, 
as dad-is is using common names for species and not official names, also some
breeds might have different naming. So we should keep all dad-is names that
are currently in data portal in DAD_IS_BREEDS constant inside fetch_biosamples
script. Script will daily generate log file with all links that couldn't be
generated automatically.

 
