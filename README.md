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
$ python /code/scripts/get_all_etags.py && \
  python /code/scripts/fetch_biosamples.py && \
  python /code/scripts/import_data.py && \
  python /code/scripts/process_fao_metadata.py

$ python /code/scripts/import_files.py
```

# Utilities

Connect to python interactive shell or database shell:

```
$ docker-compose run --rm djangoapp python manage.py shell

$ docker-compose run --rm djangoapp python manage.py dbshell
```

# Special notes about links to dad-is interface

Dadis links were derived from DADIS data relying on breed, species and country.
Download all data [from dadis](http://www.fao.org/dad-is/dataexport/en/), and place
the download data as `Report_Export_Data.csv` file into the `data` folder of
this project. Dad-is species uses the common names, while we track record with
scientific names. In CDP there's an endpoint to track the relationship between
common_name and scientific_name conversion. This is used in `process_fao_metadata.py`
scripts to construct the dad-is url and relate the organism models by patching
them using the `API`
