#!/bin/sh

set -e

python.py manage.py collectstatic --noinput
python.py manage.py migrate

uwsgi --socket :9000 --workers 4 --master-threads --module ecommerce.wsgi