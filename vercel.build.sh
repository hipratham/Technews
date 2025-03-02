#!/bin/bash
cd "$VERCEL_BUILD_OUTPUT"

# Install dependencies
python3 -m pip install -r requirements-prod.txt

# Collect static files
python3 manage.py collectstatic --noinput

# Run migrations
python3 manage.py migrate
