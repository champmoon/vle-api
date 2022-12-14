#!/bin/sh

set -e

# Activate our virtual environment here
. /opt/pysetup/.venv/bin/activate

# Run backend_pre_start.py
PYTHONPATH=. python app/backend_pre_start.py

# Run migrations
alembic upgrade head

# Run initial_data.py
PYTHONPATH=. python app/initial_data.py

# Evaluating passed command:
exec "$@"
