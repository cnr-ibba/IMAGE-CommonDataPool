#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
  -- Create a GIS database template
  CREATE DATABASE template_postgis WITH owner = postgres ENCODING = 'UTF8' CONNECTION LIMIT = -1;
  UPDATE pg_database SET datistemplate = TRUE WHERE datname = 'template_postgis' ;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" template_postgis <<-EOSQL
  -- Install GIS extension
  CREATE EXTENSION postgis;
  CREATE EXTENSION postgis_raster;
EOSQL
