#!/bin/sh
set -e

if [ ! -x /opt/venv/bin/python ]; then
  uv sync --locked
fi

exec uv run celery -A _project.celery worker -l info
