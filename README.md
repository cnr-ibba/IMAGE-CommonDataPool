# IMAGE-CommonDataPool

IMAGE Common Data Pool - PostgreSQL, metadata structure and data loading scripts

## Runing app


Make migrations and copy static files into media dir:

```
$ docker-compose run --rm djangoapp python manage.py check

$ docker-compose run --rm djangoapp python manage.py migrate

$ docker-compose run --rm djangoapp python manage.py makemigrations

$ docker-compose run --rm djangoapp python manage.py migrate

$ docker-compose run --rm djangoapp python manage.py collectstatic
```

Create superuser:

```
$ docker-compose run --rm djangoapp python manage.py createsuperuser --email {your email} --username admin
```

Start app:

```
$ docker-compose up -d
```

Stop app:

```
$ docker-compose down
```

# Upload BioSamples data

first enter into supercronic container with:

```
$ docker-compose exec supercronic /bin/bash
```

Then, inside the container execute:

```
$ python /code/scripts/get_all_etags.py && python /code/scripts/fetch_biosamples.py && python /code/scripts/import_data.py

$ python /code/scripts/import_files.py
```

# Utilities

Connect to python interactive shell or database shell:

```
$ docker-compose run --rm djangoapp python manage.py shell

$ docker-compose run --rm djangoapp python manage.py dbshell
```

# Special notes about links to dad-is interface

Is not always possible to set a correct dad-is link. First of all, dad-is species
uses the common names, while we track record with scientific names. In CDP there's
and endpoint to track the common_name -> scientific_name conversion. This is
used in import_data to construct the dad-is url which could be the same for all
the organism with the same breed-specie-country. Not all dadis links are valid,
maybe breeds are missing or not named in the same way. The callback for the dadis
link will return a default page for species list.
