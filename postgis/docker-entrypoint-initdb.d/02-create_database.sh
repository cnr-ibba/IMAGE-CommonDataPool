#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
  -- Create a GIS database
  CREATE DATABASE $DATABASE_NAME TEMPLATE template_postgis;
EOSQL
