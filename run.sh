#!/bin/sh
alembic upgrade head

cd src

sh -c "uvicorn --host 0.0.0.0 --port 8000 main:app --workers ${APP_WORKERS}"
