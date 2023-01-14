#!/bin/sh

#uvicorn main:app --host 0.0.0.0 --port 8000

python src/main.py

exec "$@"