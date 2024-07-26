#!/bin/bash

# Run Alembic migrations
alembic upgrade head

# Execute the Python application
source .venv/bin/activate
exec uvicorn --app-dir src/zypl_interview main:app --host 0.0.0.0 --port 8000 --reload