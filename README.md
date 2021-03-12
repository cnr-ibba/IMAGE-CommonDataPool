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

Fix permissions:

```
$ docker-compose run --rm djangoapp chgrp -R www-data .
```

Populate DAD-IS table with custom links:

```
$ docker-compose run --rm djangoapp python manage.py fillDAD-IS
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
$ python /code/scripts/fetch_image_data.py && \
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

Dadis links were derived from DAD-IS data relying on breed, species and country.
Download all data [from dadis](http://www.fao.org/dad-is/dataexport/en/), and place
the download data as `Report_Export_Data.csv` file into the `data` folder of
this project. Dad-is species uses the *common names*, while we track record with
*scientific names*. In CDP there's an endpoint to track the relationship between
`common_name` and `scientific_name` conversion. This is used in `process_fao_metadata.py`
scripts to construct the dad-is url and relate the organism models by patching
them using the `API`

## Add a custom dad-is link

To add a custom dad-is link (A supplied breed that is known having an entry in DAD-IS
database, but that doesn't match any of the `most_common_name`, `transboundary_name`
and `other_name` column names of DAD-IS table), add a row in
`image_backend/backend/management/commands/custom_dad-is.csv` and provide data for
`species`,`supplied_breed`,`country`,`most_common_name`,`transboundary_name`,`other_name`
and `dadis_url` columns. After that, call again:

```
$ docker-compose run --rm djangoapp python manage.py fillDAD-IS
```

(this script can be called many times, it will add only new records to the database).
Next, you need to call the `process_fao_metadata.py` script to update CDP records
(or wait for `supercronic` to call this script for you)
