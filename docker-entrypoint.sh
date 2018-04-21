#!/bin/bash

./wait_for_it.sh neo4jdb:7687 -- echo "Neo4j db is up."
./wait_for_it.sh neo4jdb:7474 -- echo "Neo4j service is up."
./wait_for_it.sh psqldb:5432 -- echo "Postgres is up."

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000