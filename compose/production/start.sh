#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset


python3 manage.py collectstatic --noinput --clear --no-post-process
gunicorn config.wsgi:application --bind 0.0.0.0:8000