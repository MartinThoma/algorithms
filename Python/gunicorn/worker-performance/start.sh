#!/usr/bin/env bash
gunicorn --worker-class=sync --workers=4  --worker-connections 1000 app:app -b 0.0.0.0:5000
