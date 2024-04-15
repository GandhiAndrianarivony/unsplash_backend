#!/bin/bash

function create_superuser() {
    echo '[INFO] Create django admin user ...'
    python3 manage.py createsuperuser --gender Male --noinput --username infinix
}

function run_db_migration() {
    echo '[INFO] Running migration ...'
    python3 manage.py makemigrations
    python3 manage.py migrate
    echo
}

function run_server() {
    python3 manage.py runserver "0.0.0.0:$1"
}

run_db_migration
create_superuser

run_server 8000