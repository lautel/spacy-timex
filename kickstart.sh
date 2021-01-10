#!/bin/bash
gunicorn -b $API_HOST:$API_PORT --timeout 30 --workers=2 --threads=2 --worker-class=gthread --preload app.api:app