#! /usr/bin/env bash

# set env

source ../../dev.env

echo $POSTGRES_DB
echo $POSTGRES_HOST
echo $POSTGRES_PORT

# DB start
python ./app/backend_pre_start.py


# Run migrations
alembic upgrade head

# Create initial data in DB
python ./app/initial_data.py