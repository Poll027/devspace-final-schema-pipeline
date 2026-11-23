#!/bin/sh
# TODO: set --limit-concurrency from fixtures.json (limit_concurrency).
exec uvicorn application:app --host 127.0.0.1 --port 8000
