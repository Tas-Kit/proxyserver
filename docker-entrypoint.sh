#!/bin/bash

./wait_for_it.sh psqldb:5432 -- echo "Postgres is up."

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000