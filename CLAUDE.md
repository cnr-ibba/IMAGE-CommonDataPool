# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

IMAGE Common Data Pool (CDP): a Django REST API over a PostGIS database holding IMAGE livestock metadata (organisms, specimens, files) harvested from EBI BioSamples. Everything runs through `docker-compose`; there is no local virtualenv setup. Configuration comes from an untracked `.env` file (`SECRET_KEY`, `DEBUG`, `DATABASE_*`, `POSTGRES_*`, `IMPORT_PASSWORD`, ...). `postgis-data/` must exist as an empty dir before first `docker-compose up` (bind-mounted DB storage).

## Services (docker-compose.yml)

- `djangoapp` – gunicorn serving `image_backend/` (mounted as `/code`)
- `nginx` – reverse proxy / static+media, exposed on port 26081
- `db` – PostGIS (built from `postgis/`), exposed on 35432
- `supercronic` – cron container running the import scripts in `supercronic/scripts/` (mounted as `/code/scripts`), schedule in `supercronic/data-import-scripts`

## Commands

Setup/migrations/admin steps are documented in README.md (`migrate`, `collectstatic`, `fillDAD-IS`, `createsuperuser`, dump/restore). Tests (Django `APITestCase`, fixtures in `backend/fixtures/backend/`):

```bash
docker-compose run --rm djangoapp python manage.py test                              # all
docker-compose run --rm djangoapp python manage.py test backend.tests.test_organism  # one module
docker-compose run --rm djangoapp python manage.py test backend.tests.test_organism.<Class>.<method>  # one test
```

Run the data pipeline manually inside the container (`docker-compose exec supercronic /bin/bash`):

```bash
python /code/scripts/fetch_image_data.py && python /code/scripts/process_fao_metadata.py
python /code/scripts/import_files.py
```

## Architecture

**Two halves communicating only over HTTP:**

1. `image_backend/` – Django project `api_service` + single app `backend`. Models (`backend/models.py`): `Organism` and `Specimen` share the abstract `BioSampleAbstract` (IMAGE metadata rules; many `ArrayField`s; `data_source_id` = BioSample accession is the PK), plus `Files`, `Species2CommonName`, `DADISLink`. `Etag` is a **DB view** (`django-db-views`, `managed = False`) unioning etags of organisms and specimens; changes to its definition go through a migration. `views.py` provides list/detail DRF views, `*_short` variants, summary/graphical_summary/download endpoints, and GeoJSON viewsets (`organism.geojson`, `specimen.geojson`). Routes in `backend/urls.py`.

2. `supercronic/scripts/` – async (aiohttp) ETL clients that talk to the CDP API (not the DB directly; authenticated with `IMPORT_PASSWORD`):
   - `fetch_image_data.py`: lists BioSample IDs from EBI, compares etags (`/etag/` endpoint) against CDP and creates/updates/ignores records. Conversion is in `helpers/backend.py` (`parse_biosample`, `CDPConverter`, ruleset-driven), EBI access in `helpers/biosamples.py`.
   - `process_fao_metadata.py`: builds DAD-IS URLs for organisms by matching breed/species/country from `data/Report_Export_Data.csv` (manual FAO download, see README) and `DADISLink` records, then PATCHes organisms via the API.
   - `import_files.py`: imports file metadata (ENA/EVA) into `Files`.

DAD-IS custom links: add rows to `backend/management/commands/custom_dad-is.csv`, re-run `manage.py fillDAD-IS` (idempotent), then `process_fao_metadata.py`.

Note that the Django code is old-style (e.g. `django.utils.http.urlquote`); check `djangoapp/requirements.txt` for pinned versions before upgrading anything. Commits in this repo use gitmoji shortcodes; work happens on `devel`, merged to `master` via PR.
