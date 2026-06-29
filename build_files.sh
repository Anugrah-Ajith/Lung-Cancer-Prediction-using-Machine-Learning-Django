#!/bin/bash

# Install dependencies
pip install --break-system-packages -r requirements.txt

# Run database migrations (creates auth tables in /tmp/db.sqlite3 on Vercel)
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Create the output directory for Vercel static build
mkdir -p staticfiles_build/static
cp -r staticfiles/* staticfiles_build/static/
