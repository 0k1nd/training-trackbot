#!/bin/sh
set -e

if [ ! -x /opt/venv/bin/python ]; then
  uv sync --locked
fi

exec uv run celery -A _project.celery beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
