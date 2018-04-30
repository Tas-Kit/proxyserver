#!/bin/bash

./wait_for_it.sh neo4jdb:7687 -- echo "Neo4j db is up."
./wait_for_it.sh neo4jdb:7474 -- echo "Neo4j service is up."
./wait_for_it.sh memcached:11211 -- echo "Memcached is up."
./wait_for_it.sh psqldb:5432 -- echo "Postgres is up."

# Start server
echo "Starting server"

if [[ $DJANGO_SETTINGS_MODULE = *"dev" ]]; then
    echo "Starting HTTP Server"
    python manage.py runserver 0.0.0.0:8000
else
    echo "Starting HTTPS Server"
    python manage.py runsslserver 0.0.0.0:8000
fi