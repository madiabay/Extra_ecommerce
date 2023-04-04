#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python /proj/code/manage.py makemigrations
python /proj/code/manage.py migrate
python /proj/code/manage.py collectstatic --noinput

cd /proj/code

daphne -b 0.0.0.0 -p 8000 src.asgi:application