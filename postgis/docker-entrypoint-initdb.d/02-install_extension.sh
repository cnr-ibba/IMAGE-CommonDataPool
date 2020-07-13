#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" cdp <<-EOSQL
  -- Install GIS extension
  CREATE EXTENSION postgis;
  CREATE EXTENSION postgis_raster;
EOSQL
