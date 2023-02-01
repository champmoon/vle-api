#!/bin/sh

set -e

# Activate our virtual environment here
. /opt/pysetup/.venv/bin/activate

export PYTHONPATH=.

# Run pre_start script: check health for db
python app/scripts/pre_start/check_health.py

# Run migrations
alembic upgrade head

# Run other pre start scripts, order matters!!!
python app/scripts/pre_start/create_roles.py
python app/scripts/pre_start/create_super_user.py

# Evaluating passed command:
exec "$@"
